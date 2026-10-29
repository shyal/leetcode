// The transport to leetcode.com: every request runs inside the browser at
// LC_CDP_ENDPOINT (misc/lc_fetch.mjs), so it carries the browser's login
// and passes Cloudflare; a copied cookie does not (the WAF 403s "(a or b)
// or (c or d)" from anything but a real browser, 2026-09-17). When nothing
// answers there and LC_BROWSER_APP names an application, it is opened with
// --remote-debugging-port=<the endpoint's port> first (ensure_browser).
// lc_submit and lc_sync run on it; it was lc_submit's own until 2026-10-11.

use std::io::Write;
use std::process::{Command, Stdio};
use std::time::Duration;

use serde_json::{json, Value};

pub fn no_browser() -> bool {
    std::env::var("LC_CDP_ENDPOINT").map_or(true, |v| v.is_empty())
}

/// host:port of the devtools endpoint, for a TCP probe.
fn endpoint_addr(endpoint: &str) -> Option<(String, u16)> {
    let rest = endpoint.split("://").nth(1).unwrap_or(endpoint);
    let authority = rest.split('/').next()?;
    let (host, port) = authority.rsplit_once(':')?;
    Some((host.to_string(), port.parse().ok()?))
}

/// True when something answers on the endpoint's port.
fn browser_up(endpoint: &str) -> bool {
    let Some((host, port)) = endpoint_addr(endpoint) else {
        return false;
    };
    use std::net::{TcpStream, ToSocketAddrs};
    let Ok(mut addrs) = (host.as_str(), port).to_socket_addrs() else {
        return false;
    };
    addrs.any(|a| TcpStream::connect_timeout(&a, Duration::from_millis(500)).is_ok())
}

/// Make sure a browser is listening at LC_CDP_ENDPOINT. When nothing is,
/// and LC_BROWSER_APP names an application, open it with the devtools port
/// and wait for it to answer. An app already running without the port
/// ignores the flag, so the error names that case.
pub fn ensure_browser() -> Result<(), String> {
    if no_browser() {
        return Err("no browser: set LC_CDP_ENDPOINT to its devtools endpoint".into());
    }
    let endpoint = std::env::var("LC_CDP_ENDPOINT").unwrap_or_default();
    if browser_up(&endpoint) {
        return Ok(());
    }
    let app = std::env::var("LC_BROWSER_APP").unwrap_or_default();
    if app.is_empty() {
        return Err(format!(
            "no browser at {endpoint}; start one with its devtools port, or set LC_BROWSER_APP to the app to open"
        ));
    }
    let (_, port) =
        endpoint_addr(&endpoint).ok_or_else(|| format!("LC_CDP_ENDPOINT {endpoint}: no port"))?;
    eprintln!("opening {app} with its devtools port...");
    let status = Command::new("open")
        .args([
            "-a",
            &app,
            "--args",
            &format!("--remote-debugging-port={port}"),
        ])
        .status()
        .map_err(|e| format!("open: {e}"))?;
    if !status.success() {
        return Err(format!("open {app}: exit {status}"));
    }
    for _ in 0..40 {
        std::thread::sleep(Duration::from_millis(500));
        if browser_up(&endpoint) {
            return Ok(());
        }
    }
    Err(format!(
        "{app} did not answer at {endpoint} in 20s; if it was already running without the devtools port, quit it and run again"
    ))
}

/// One request to leetcode.com through the browser: (status, body).
pub fn fetch(method: &str, path: &str, body: Option<&Value>) -> Result<(u16, String), String> {
    if no_browser() {
        return Err("no browser: set LC_CDP_ENDPOINT to its devtools endpoint".into());
    }
    let script = crate::data::repo_root().join("misc/lc_fetch.mjs");
    let mut child = Command::new("node")
        .arg(script)
        .arg(method)
        .arg(path)
        .stdin(if body.is_some() {
            Stdio::piped()
        } else {
            Stdio::null()
        })
        .stdout(Stdio::piped())
        .stderr(Stdio::piped())
        .spawn()
        .map_err(|e| format!("node: {e}"))?;
    if let Some(b) = body {
        let mut stdin = child.stdin.take().ok_or("node: no stdin")?;
        stdin
            .write_all(b.to_string().as_bytes())
            .map_err(|e| format!("node: {e}"))?;
    }
    let out = child.wait_with_output().map_err(|e| format!("node: {e}"))?;
    if !out.status.success() {
        return Err(String::from_utf8_lossy(&out.stderr).trim().to_string());
    }
    let text = String::from_utf8_lossy(&out.stdout).into_owned();
    let (status, rest) = text.split_once('\n').unwrap_or((&text, ""));
    let status = status
        .parse()
        .map_err(|_| format!("lc_fetch: no status in {text:?}"))?;
    Ok((status, rest.to_string()))
}

/// The problem slug from a solve file's
/// `URL: https://leetcode.com/problems/<slug>/...` line.
pub fn slug_of(code: &str) -> Option<String> {
    let line = code.lines().find(|l| l.trim_start().starts_with("URL:"))?;
    let rest = line.split("/problems/").nth(1)?;
    let slug = rest.split(['/', '?']).next()?;
    (!slug.is_empty()).then(|| slug.to_string())
}

pub fn json_of(body: &str) -> Result<Value, String> {
    serde_json::from_str(body).map_err(|_| format!("leetcode sent no json: {body:.200}"))
}

/// One GraphQL query: (http status, the reply as json). A 200 whose reply
/// carries `errors` is an Err naming them; the `data` comes back otherwise.
/// A status other than 200 is Ok((status, body)) for the caller to wait
/// out (429) or report.
pub fn graphql(query: &str, variables: Value) -> Result<(u16, Value), String> {
    let (status, body) = fetch(
        "POST",
        "/graphql/",
        Some(&json!({"query": query, "variables": variables})),
    )?;
    if status != 200 {
        return Ok((status, Value::String(body)));
    }
    let v = json_of(&body)?;
    if let Some(errs) = v.get("errors").filter(|e| !e.is_null()) {
        return Err(format!("graphql: {errs}"));
    }
    match v.get("data") {
        Some(d) => Ok((status, d.clone())),
        None => Err(format!("graphql: no data in {body:.200}")),
    }
}
