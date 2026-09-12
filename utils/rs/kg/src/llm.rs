// kg_lib.claude_json: one non-interactive `claude -p` call, the JSON object
// in its result. A reply that is not JSON (haiku, now and then) is asked
// again, up to `retries` more times: the detached judge has no operator to
// re-run it.

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

fn once(prompt: &str, system_prompt: &str, model: &str) -> Result<Value, LlmError> {
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

#[cfg(test)]
mod tests {
    #[test]
    fn first_object_tolerates_junk() {
        let v = super::first_object("```json\n{\"a\": 1} {\"a\": 2}\n```").unwrap();
        assert_eq!(v["a"], 1);
        assert!(super::first_object("no braces").is_err());
    }
}
