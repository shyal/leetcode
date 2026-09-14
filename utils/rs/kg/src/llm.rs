// kg_lib.claude_json: one non-interactive `claude -p` call, the JSON object
// in its result. A reply that is not JSON (haiku, now and then) is asked
// again, up to `retries` more times: the detached judge has no operator to
// re-run it.
//
// A model named `deepseek` or `deepseek-<x>` goes to DeepSeek's chat
// completions endpoint instead (OpenAI-compatible JSON, key in
// DEEPSEEK_API_KEY); one named `gpt-<x>` goes to OpenAI's (key in
// ~/.openai_key_leet, else OPENAI_API_KEY). `deepseek` alone means deepseek-chat. The judge reads
// its default model from JUDGE_MODEL, so `export JUDGE_MODEL=deepseek` in
// .envrc switches every verdict over; the claude aliases still work.

use std::process::Command;

use serde_json::Value;

#[derive(Debug)]
pub enum LlmError {
    /// claude exited non-zero: (code, stderr head)
    Exit(i32, String),
    /// the result carried no JSON object
    NotJson(String),
    Spawn(String),
}

impl std::fmt::Display for LlmError {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            LlmError::Exit(c, e) => write!(f, "claude exited {c}: {e}"),
            LlmError::NotJson(t) => write!(f, "no JSON object in result: {t:?}"),
            LlmError::Spawn(e) => write!(f, "claude: {e}"),
        }
    }
}

/// The name a verdict is filed under: the model as the API knows it
/// (`deepseek` is the alias for deepseek-chat; claude aliases stay as typed).
pub fn judge_name(model: &str) -> String {
    if model == "deepseek" {
        "deepseek-chat".to_string()
    } else {
        model.to_string()
    }
}

/// The judge's model: JUDGE_MODEL from the environment, else `fallback`.
pub fn judge_model(fallback: &str) -> String {
    std::env::var("JUDGE_MODEL")
        .ok()
        .filter(|m| !m.trim().is_empty())
        .unwrap_or_else(|| fallback.to_string())
}

/// ~/.openai_key_leet first, OPENAI_API_KEY second: the shell's variable
/// has been a dead key more than once (2026-09-13: a 429 on it while the
/// file's key answered).
fn openai_key() -> Option<String> {
    let from_file = std::env::var("HOME").ok().and_then(|home| {
        std::fs::read_to_string(format!("{home}/.openai_key_leet"))
            .ok()
            .map(|k| k.trim().to_string())
            .filter(|k| !k.is_empty())
    });
    from_file.or_else(|| {
        std::env::var("OPENAI_API_KEY")
            .ok()
            .filter(|k| !k.is_empty())
    })
}

/// One OpenAI-compatible chat completion, JSON object answer.
fn chat_once(url: &str, key: &str, body: Value) -> Result<Value, LlmError> {
    // a dead connection must fail, not hang a worker forever (the 2026-09-13
    // full re-judge sat 18 minutes on a dropped network)
    let agent: ureq::Agent = ureq::Agent::config_builder()
        .timeout_global(Some(std::time::Duration::from_secs(180)))
        .build()
        .into();
    let mut resp = agent
        .post(url)
        .header("Authorization", &format!("Bearer {key}"))
        .header("Content-Type", "application/json")
        .send_json(&body)
        .map_err(|e| LlmError::Exit(1, e.to_string().chars().take(500).collect()))?;
    let envelope: Value = resp
        .body_mut()
        .read_json()
        .map_err(|e| LlmError::NotJson(e.to_string().chars().take(200).collect()))?;
    if std::env::var("KG_LLM_USAGE").is_ok() {
        eprintln!("usage: {}", envelope["usage"]);
    }
    let result = envelope["choices"][0]["message"]["content"]
        .as_str()
        .unwrap_or("");
    first_object(result)
}

fn openai_once(prompt: &str, system_prompt: &str, model: &str) -> Result<Value, LlmError> {
    let key = openai_key().ok_or_else(|| {
        LlmError::Spawn("OPENAI_API_KEY is not set and ~/.openai_key_leet is missing".into())
    })?;
    // gpt-5 models take no temperature; reasoning stays at the default
    let body = serde_json::json!({
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt},
        ],
        "response_format": {"type": "json_object"},
    });
    chat_once("https://api.openai.com/v1/chat/completions", &key, body)
}

fn deepseek_once(prompt: &str, system_prompt: &str, model: &str) -> Result<Value, LlmError> {
    let key = std::env::var("DEEPSEEK_API_KEY")
        .ok()
        .filter(|k| !k.is_empty())
        .ok_or_else(|| LlmError::Spawn("DEEPSEEK_API_KEY is not set".into()))?;
    let model = judge_name(model);
    let body = serde_json::json!({
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt},
        ],
        "temperature": 0,
        "response_format": {"type": "json_object"},
    });
    chat_once("https://api.deepseek.com/chat/completions", &key, body)
}

fn once(prompt: &str, system_prompt: &str, model: &str) -> Result<Value, LlmError> {
    if model.starts_with("deepseek") {
        return deepseek_once(prompt, system_prompt, model);
    }
    if model.starts_with("gpt-") {
        return openai_once(prompt, system_prompt, model);
    }
    let out = Command::new("claude")
        .args([
            "-p",
            prompt,
            "--system-prompt",
            system_prompt,
            "--model",
            model,
            "--output-format",
            "json",
        ])
        .output()
        .map_err(|e| LlmError::Spawn(e.to_string()))?;
    if !out.status.success() {
        let err = String::from_utf8_lossy(&out.stderr);
        return Err(LlmError::Exit(
            out.status.code().unwrap_or(1),
            err.chars().take(500).collect(),
        ));
    }
    let envelope: Value = serde_json::from_slice(&out.stdout).map_err(|_| {
        LlmError::NotJson(
            String::from_utf8_lossy(&out.stdout)
                .chars()
                .take(200)
                .collect(),
        )
    })?;
    let result = envelope.get("result").and_then(Value::as_str).unwrap_or("");
    first_object(result)
}

/// The FIRST valid {...} in the text, fences, preamble and trailing junk
/// ignored (json.JSONDecoder().raw_decode from the first brace).
pub fn first_object(text: &str) -> Result<Value, LlmError> {
    let text = text.trim();
    let Some(start) = text.find('{') else {
        return Err(LlmError::NotJson(text.chars().take(200).collect()));
    };
    let mut de = serde_json::Deserializer::from_str(&text[start..]).into_iter::<Value>();
    match de.next() {
        Some(Ok(v)) if v.is_object() => Ok(v),
        _ => Err(LlmError::NotJson(text.chars().take(200).collect())),
    }
}

pub fn claude_json(
    prompt: &str,
    system_prompt: &str,
    model: &str,
    retries: usize,
) -> Result<Value, LlmError> {
    let mut attempt = 0;
    loop {
        match once(prompt, system_prompt, model) {
            Err(LlmError::NotJson(t)) if attempt < retries => {
                let _ = t;
                attempt += 1;
            }
            other => return other,
        }
    }
}

// ---- plain-text completions (prepare, asserts) ---------------------------

/// prepare.llm / asserts.claude: one completion whose answer is raw text
/// (Python source), fences and all. A `gpt-*`, `o3*` or `o4*` model goes to
/// OpenAI (temperature 0.2 on gpt-4, the reasoning models take only the
/// default); anything else, or no model at all, is `claude -p` with the
/// file-writing tools disallowed, its stdout returned whatever its exit
/// code, exactly as the Python did.
pub fn text(prompt: &str, system_prompt: &str, model: Option<&str>) -> Result<String, LlmError> {
    if let Some(m) = model {
        if m.starts_with("gpt-") || m.starts_with("o3") || m.starts_with("o4") {
            return openai_text(prompt, system_prompt, m);
        }
    }
    let mut args: Vec<&str> = vec!["-p", prompt];
    if let Some(m) = model {
        args.extend(["--model", m]);
    }
    args.extend([
        "--system-prompt",
        system_prompt,
        "--disallowedTools",
        "Write,Edit,Read,Bash,NotebookEdit",
        "--output-format",
        "text",
    ]);
    let out = Command::new("claude")
        .args(&args)
        .output()
        .map_err(|e| LlmError::Spawn(e.to_string()))?;
    Ok(String::from_utf8_lossy(&out.stdout).trim().to_string())
}

fn openai_text(prompt: &str, system_prompt: &str, model: &str) -> Result<String, LlmError> {
    let key = openai_key().ok_or_else(|| {
        LlmError::Spawn("OPENAI_API_KEY is not set and ~/.openai_key_leet is missing".into())
    })?;
    let mut body = serde_json::json!({
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt},
        ],
    });
    if model.starts_with("gpt-4") {
        body["temperature"] = serde_json::json!(0.2);
    }
    let agent: ureq::Agent = ureq::Agent::config_builder()
        .timeout_global(Some(std::time::Duration::from_secs(600)))
        .build()
        .into();
    let mut resp = agent
        .post("https://api.openai.com/v1/chat/completions")
        .header("Authorization", &format!("Bearer {key}"))
        .header("Content-Type", "application/json")
        .send_json(&body)
        .map_err(|e| LlmError::Exit(1, e.to_string().chars().take(500).collect()))?;
    let envelope: Value = resp
        .body_mut()
        .read_json()
        .map_err(|e| LlmError::NotJson(e.to_string().chars().take(200).collect()))?;
    Ok(envelope["choices"][0]["message"]["content"]
        .as_str()
        .unwrap_or("")
        .trim()
        .to_string())
}

#[cfg(test)]
mod tests {
    #[test]
    fn first_object_tolerates_junk() {
        let v = super::first_object("```json\n{\"a\": 1} {\"a\": 2}\n```").unwrap();
        assert_eq!(v["a"], 1);
        assert!(super::first_object("no braces").is_err());
    }
}
