//! The prepare pipeline's library: the stub transforms (stub), the
//! reference-run assert generator (assert_gen), the script runner (pyrun)
//! and the .prepare_cache entries the `prepare` and `asserts` binaries
//! share. Ported from utils/kg/{prepare,asserts,stub_utils.py,assert_gen.py}
//! on 2026-09-14.

pub mod assert_gen;
pub mod pyrun;
pub mod stub;

use std::path::{Path, PathBuf};

use serde_json::Value;

pub use pyrun::CACHE_DIR;

pub fn cache_path(root: &Path, num: &str) -> PathBuf {
    root.join(CACHE_DIR).join(format!("{num}.json"))
}

/// The cached entry as json.load reads it, or None when unreadable.
pub fn cache_entry(root: &Path, num: &str) -> Option<Value> {
    kg::pyjson::load(&cache_path(root, num))
}

/// prepare.cache_load: (title, code, solution); "solution" is absent on
/// entries cached before it was kept.
pub fn cache_load(root: &Path, num: &str) -> Option<(String, String, Option<String>)> {
    let entry = cache_entry(root, num)?;
    let title = entry.get("title")?.as_str()?.to_string();
    let code = entry.get("code")?.as_str()?.to_string();
    let solution = entry
        .get("solution")
        .and_then(Value::as_str)
        .map(str::to_string);
    Some((title, code, solution))
}

/// json.dump of one entry, {title, code, solution}.
pub fn cache_save(root: &Path, num: &str, title: &str, code: &str, solution: &str) {
    let _ = std::fs::create_dir_all(root.join(CACHE_DIR));
    let entry = serde_json::json!({"title": title, "code": code, "solution": solution});
    write_entry(root, num, &entry);
}

pub fn write_entry(root: &Path, num: &str, entry: &Value) {
    std::fs::write(cache_path(root, num), kg::pyjson::dumps(entry, None)).expect("write cache");
}

/// A pool of `jobs` threads draining `items` in order; `work` runs on the
/// worker's thread and reports through its own prints.
pub fn pool<T: Send + 'static>(
    items: Vec<T>,
    jobs: usize,
    work: impl Fn(T) + Send + Sync + 'static,
) {
    use std::sync::{Arc, Mutex};
    let n = jobs.min(items.len()).max(1);
    let queue = Arc::new(Mutex::new(std::collections::VecDeque::from(items)));
    let work = Arc::new(work);
    let threads: Vec<_> = (0..n)
        .map(|_| {
            let queue = Arc::clone(&queue);
            let work = Arc::clone(&work);
            std::thread::spawn(move || loop {
                let next = queue.lock().unwrap().pop_front();
                match next {
                    Some(item) => work(item),
                    None => return,
                }
            })
        })
        .collect();
    for t in threads {
        let _ = t.join();
    }
}
