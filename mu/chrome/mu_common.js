// What mu_page.js (LeetCode) and mu_aced.js (aced.io) share. Runs in the
// page itself, before them, and leaves `window.__mu`: `ask`, the way to the
// extension through mu_bridge.js (the page has no chrome.* APIs, so each
// request is a window message answered by one); `register`, mu as a
// language in the page's Monaco; and OPENS_BLOCK, the mu line that opens a
// block, for the editors' Enter.

(() => {
  // a line that opens a block: a statement header, a fold or a `first` with no
  // one-line body after `:`, a `{n ->` or a `{` alone at the end of the line
  const OPENS_BLOCK = /^\s*(def|memo|class|for|if|elif|else|while|try|except|finally|with|async)\b|\b(sum|max|min|count)\s+(for|from)\b[^:]*$|^\s*first\s+\w+\s+in\b[^:]*$|(->|\{)\s*$/;

  let seq = 0;
  const pending = new Map();
  window.addEventListener("message", (e) => {
    if (e.source !== window || e.data?.muRes === undefined) return;
    pending.get(e.data.muRes)?.(e.data.result);
    pending.delete(e.data.muRes);
  });
  const ask = (op, args = {}) =>
    new Promise((resolve) => {
      const id = ++seq;
      pending.set(id, resolve);
      window.postMessage({ muReq: id, op, ...args }, "*");
    });

  function register() {
    const { languages } = window.monaco;
    if (languages.getLanguages().some((l) => l.id === "mu")) return;
    languages.register({ id: "mu" });
    languages.setMonarchTokensProvider("mu", {
      // mulang/ide.py KEYWORDS, plus class
      keywords: ["def", "memo", "class", "ret", "for", "in", "if", "elif", "else", "while", "return", "break",
        "continue", "pass", "del", "assert", "yield", "from", "first", "import", "extends", "and", "or", "not",
        "is", "true", "false", "none", "inf", "lambda", "mu", "with", "as", "try", "except", "finally", "raise",
        "global", "nonlocal", "async", "await", "by"],
      builtins: ["len", "max", "min", "sum", "count", "abs", "sort", "scan", "counter", "ceil", "floor",
        "cells", "nbrs", "components", "graph", "dijkstra"],
      types: ["int", "str", "char", "bool", "float"],
      tokenizer: {
        root: [
          [/#.*$/, "comment"],
          [/[fFrRbB]{0,2}"""/, "string", "@double"],
          [/[fFrRbB]{0,2}'''/, "string", "@single"],
          [/[fFrRbB]{0,2}"[^"\n]*"/, "string"],
          [/[fFrRbB]{0,2}'[^'\n]*'/, "string"],
          [/\d+(\.\d+)?/, "number"],
          [/[A-Za-z_]\w*/, { cases: { "@keywords": "keyword", "@builtins": "predefined", "@types": "type", "@default": "identifier" } }],
          [/\.\.<|\.\.|->|<-/, "keyword"],
        ],
        double: [[/"""/, "string", "@pop"], [/./, "string"]],
        single: [[/'''/, "string", "@pop"], [/./, "string"]],
      },
    });
    languages.setLanguageConfiguration("mu", {
      comments: { lineComment: "#" },
      brackets: [["(", ")"], ["[", "]"], ["{", "}"]],
      autoClosingPairs: [
        { open: "(", close: ")" }, { open: "[", close: "]" }, { open: "{", close: "}" },
        { open: '"', close: '"' }, { open: "'", close: "'" },
      ],
      onEnterRules: [{ beforeText: OPENS_BLOCK, action: { indentAction: languages.IndentAction.Indent } }],
    });
  }

  window.__mu = { OPENS_BLOCK, ask, register };
})();
