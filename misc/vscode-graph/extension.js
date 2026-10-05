// The graph explorer: a webview that draws the technique graph around the
// problem or drill in current.py. Everything it shows comes from
// `kg_explore` (utils/rs/kg_explore): `graph` for the picture, `show <id>`
// for the side panel, `disable` and `enable` for the drill switch. Nothing
// about status, due dates or holds is computed here.
const vscode = require("vscode");
const path = require("path");
const fs = require("fs");
const { execFile } = require("child_process");

const SCHEME = "leet-graph";
const WATCHED = "{current.py,current.mu,current.ts,graph/drills.json,graph/evidence.json}";

function workspaceRoot() {
  const folders = vscode.workspace.workspaceFolders || [];
  const hit = folders.find((f) => fs.existsSync(path.join(f.uri.fsPath, "graph", "drills.json")));
  return hit && hit.uri.fsPath;
}

// Run kg_explore in the repo; resolves to stdout, rejects with the
// sentence the tool printed.
function explore(root, args) {
  const bin = path.join(root, "utils", "rs", "target", "release", "kg_explore");
  return new Promise((resolve, reject) => {
    if (!fs.existsSync(bin)) {
      return reject(new Error("kg_explore is not built. Run `make graph-vscode` in the repo."));
    }
    execFile(bin, args, { cwd: root, maxBuffer: 64 * 1024 * 1024 }, (err, stdout, stderr) => {
      if (err) return reject(new Error((stderr || err.message).trim()));
      resolve(stdout);
    });
  });
}

// The statement and stub, or the reference solution, of a cached problem,
// as a read-only document: leet-graph:/799. Champagne Tower (stub).py?{...}
class CacheDocs {
  constructor(root) {
    this.root = root;
  }
  provideTextDocumentContent(uri) {
    const { id, field } = JSON.parse(uri.query);
    const file = path.join(this.root, ".prepare_cache", `${id}.json`);
    const entry = JSON.parse(fs.readFileSync(file, "utf8"));
    return entry[field] || `The cache holds no ${field} for ${id}.`;
  }
}

function html(webview, media) {
  const uri = (name) => webview.asWebviewUri(vscode.Uri.joinPath(media, name));
  const nonce = [...Array(32)].map(() => Math.floor(Math.random() * 36).toString(36)).join("");
  return `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta http-equiv="Content-Security-Policy" content="default-src 'none'; style-src ${webview.cspSource}; script-src 'nonce-${nonce}';">
<link rel="stylesheet" href="${uri("main.css")}">
</head>
<body>
<header>
  <input id="search" type="search" placeholder="Number, drill id, node id or title" autocomplete="off">
  <button id="current">Current</button>
  <span id="message"></span>
</header>
<main>
  <div id="canvas"><svg id="svg" xmlns="http://www.w3.org/2000/svg"></svg></div>
  <aside id="detail"></aside>
</main>
<script nonce="${nonce}" src="${uri("layout.js")}"></script>
<script nonce="${nonce}" src="${uri("main.js")}"></script>
</body>
</html>`;
}

function activate(context) {
  let panel;
  let timer;

  const open = () => {
    const root = workspaceRoot();
    if (!root) {
      vscode.window.showErrorMessage("The graph explorer needs the leet repo open as a workspace folder.");
      return;
    }
    if (panel) return panel.reveal();
    const media = vscode.Uri.joinPath(context.extensionUri, "media");
    panel = vscode.window.createWebviewPanel("leetGraph", "Graph", vscode.ViewColumn.Beside, {
      enableScripts: true,
      retainContextWhenHidden: true,
      localResourceRoots: [media],
    });
    panel.webview.html = html(panel.webview, media);

    const post = (m) => panel && panel.webview.postMessage(m);
    const fail = (e) => post({ type: "error", text: e.message });
    const sendGraph = () =>
      explore(root, ["graph"]).then((out) => post({ type: "graph", data: JSON.parse(out) }), fail);
    const sendDetail = (id) =>
      explore(root, ["show", id]).then((out) => post({ type: "detail", data: JSON.parse(out) }), fail);
    const showFile = (rel) =>
      vscode.window.showTextDocument(vscode.Uri.file(path.join(root, rel)), {
        viewColumn: vscode.ViewColumn.One,
        preview: true,
      });

    panel.webview.onDidReceiveMessage((m) => {
      if (m.type === "ready") sendGraph();
      if (m.type === "show") sendDetail(m.id);
      if (m.type === "open") showFile(m.path).then(undefined, (e) => fail(e));
      if (m.type === "cache") {
        const uri = vscode.Uri.from({
          scheme: SCHEME,
          path: `/${m.title} (${m.field === "code" ? "stub" : "reference"}).py`,
          query: JSON.stringify({ id: m.id, field: m.field }),
        });
        vscode.window
          .showTextDocument(uri, { viewColumn: vscode.ViewColumn.One, preview: true })
          .then(undefined, (e) => fail(e));
      }
      if (m.type === "flag") {
        explore(root, [m.on ? "disable" : "enable", m.id])
          .then(sendGraph, fail)
          .then(() => sendDetail(m.id));
      }
    });

    // current.* changes on prepare and solved, evidence.json on a judged
    // rep, drills.json on a flag: draw again, and follow current.py.
    const watcher = vscode.workspace.createFileSystemWatcher(new vscode.RelativePattern(root, WATCHED));
    const changed = () => {
      clearTimeout(timer);
      timer = setTimeout(sendGraph, 400);
    };
    watcher.onDidChange(changed);
    watcher.onDidCreate(changed);
    watcher.onDidDelete(changed);
    const docs = vscode.workspace.registerTextDocumentContentProvider(SCHEME, new CacheDocs(root));
    panel.onDidDispose(() => {
      watcher.dispose();
      docs.dispose();
      clearTimeout(timer);
      panel = undefined;
    });
  };

  context.subscriptions.push(vscode.commands.registerCommand("leetGraph.open", open));
}

function deactivate() {}

module.exports = { activate, deactivate };
