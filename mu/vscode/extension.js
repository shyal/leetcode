// Formats .mu files by piping the document through `mu.py --fmt -`, and
// debugs current.mu: `session.py debug` writes .mu_current.py with a line
// map, and the `mu` debug type runs debugpy on the Python behind a proxy
// (adapter.js) that keeps the editor on the mu file.
const vscode = require("vscode");
const path = require("path");
const fs = require("fs");
const { execFile, spawn } = require("child_process");
const { Rewriter, Framer } = require("./adapter");

const MU = path.join(__dirname, "..", "mu.py");
const SESSION = path.join(__dirname, "..", "session.py");

function format(document) {
  const python = vscode.workspace.getConfiguration("mu").get("python");
  return new Promise((resolve) => {
    const child = execFile(python, ["-S", MU, "--fmt", "-"], (err, stdout, stderr) => {
      if (err) {
        vscode.window.showErrorMessage(`mu fmt: ${(stderr || err.message).trim()}`);
        return resolve([]);
      }
      const text = document.getText();
      if (stdout === text) return resolve([]);
      const all = new vscode.Range(document.positionAt(0), document.positionAt(text.length));
      resolve([vscode.TextEdit.replace(all, stdout)]);
    });
    child.stdin.end(document.getText());
  });
}

// The workspace folder holding current.mu: the folder of the active file
// when it is a .mu or current.py, else the first workspace folder.
function workspaceRoot() {
  const doc = vscode.window.activeTextEditor && vscode.window.activeTextEditor.document;
  const folder = doc && vscode.workspace.getWorkspaceFolder(doc.uri);
  const first = vscode.workspace.workspaceFolders && vscode.workspace.workspaceFolders[0];
  const f = folder || first;
  return f ? f.uri.fsPath : null;
}

// The interpreter that runs the solve: the repo's .venv, whose sitecustomize
// preloads the harness, else the configured python.
function solvePython(root) {
  const venv = path.join(root, ".venv", "bin", "python3");
  if (fs.existsSync(venv)) return venv;
  return vscode.workspace.getConfiguration("mu").get("python");
}

function run(cmd, args, cwd) {
  return new Promise((resolve, reject) => {
    execFile(cmd, args, { cwd }, (err, stdout, stderr) => {
      if (err) return reject(new Error((stderr || err.message).trim()));
      resolve(stdout);
    });
  });
}

// The debugpy the Python Debugger extension ships; the venv python runs it.
function debugpyLibs() {
  const ext = vscode.extensions.getExtension("ms-python.debugpy");
  if (!ext) return null;
  const libs = path.join(ext.extensionPath, "bundled", "libs");
  return fs.existsSync(path.join(libs, "debugpy")) ? libs : null;
}

// Fills in a `mu` launch config: builds .mu_current.py and its map, and
// names the program, the mu file and the interpreter.
class MuConfigurationProvider {
  async resolveDebugConfiguration(folder, config) {
    const root = (folder && folder.uri.fsPath) || workspaceRoot();
    if (!root) {
      vscode.window.showErrorMessage("mu debug: open the repo as a workspace folder");
      return undefined;
    }
    const python = solvePython(root);
    await vscode.workspace.saveAll();
    // the mu file in the editor, else current.mu
    const doc = vscode.window.activeTextEditor && vscode.window.activeTextEditor.document;
    const active = doc && doc.languageId === "mu" ? doc.uri.fsPath : path.join(root, "current.mu");
    const args = [SESSION, "debug"];
    if (path.relative(root, active) !== "current.mu") args.push(active);
    let target;
    try {
      target = (await run(python, args, root)).trim();
    } catch (err) {
      vscode.window.showErrorMessage(`mu debug: ${err.message}`);
      return undefined;
    }
    const mapPath = path.join(root, ".mu_current.map.json");
    const mapped = target !== "current.py" && fs.existsSync(mapPath);
    const map = mapped ? JSON.parse(fs.readFileSync(mapPath, "utf8")) : null;
    return {
      ...config,
      type: "mu",
      request: "launch",
      name: config.name || `mu: ${path.basename(active)}`,
      program: path.join(root, target),
      muFile: map ? path.resolve(root, map.file) : active,
      mapFile: mapped ? mapPath : null,
      python: [python],
      cwd: root,
      console: config.console || "internalConsole",
      justMyCode: false,
    };
  }
}

// The adapter VS Code talks to: debugpy's own adapter over stdio, with
// every message passing through the Rewriter.
class MuDebugAdapter {
  constructor(session) {
    const cfg = session.configuration;
    const map = cfg.mapFile ? JSON.parse(fs.readFileSync(cfg.mapFile, "utf8")) : { lines: {} };
    this.rw = new Rewriter(map, cfg.program, cfg.muFile);
    this.emitter = new vscode.EventEmitter();
    this.onDidSendMessage = this.emitter.event;
    this.framer = new Framer();
    const libs = debugpyLibs();
    const python = cfg.python[0];
    const logDir = vscode.workspace.getConfiguration("mu").get("debugLogDir");
    const args = ["-m", "debugpy.adapter"];
    if (logDir) args.push("--log-dir", logDir, "--log-stderr");
    this.child = spawn(python, args, {
      cwd: cfg.cwd,
      env: { ...process.env, PYTHONPATH: libs ? libs : process.env.PYTHONPATH || "" },
    });
    this.child.stdout.on("data", (chunk) => {
      for (const msg of this.framer.decode(chunk)) this.fromAdapter(msg);
    });
    this.child.stderr.on("data", (d) => console.error(`mu debug: ${d}`));
    this.child.on("exit", (code) => {
      if (code) vscode.window.showErrorMessage(`mu debug: debugpy adapter exited with ${code}`);
      this.emitter.fire({ type: "event", event: "terminated", seq: 0 });
    });
    if (!libs) vscode.window.showErrorMessage("mu debug: the Python Debugger extension (ms-python.debugpy) is not installed");
  }

  // VS Code -> debugpy
  handleMessage(msg) {
    if (msg.type === "request" && msg.command === "launch") {
      const a = { ...msg.arguments };
      delete a.muFile;
      delete a.mapFile;
      msg = { ...msg, arguments: { ...a, type: "python" } };
    }
    this.send(this.rw.toAdapter(msg));
  }

  // debugpy -> VS Code, with the proxy's own follow-up requests
  fromAdapter(msg) {
    const { messages, requests } = this.rw.toClient(msg);
    for (const m of messages) this.emitter.fire(m);
    for (const r of requests) this.send(r);
  }

  send(msg) {
    if (this.child.stdin.writable) this.child.stdin.write(this.framer.encode(msg));
  }

  dispose() {
    if (this.child && !this.child.killed) this.child.kill();
    this.emitter.dispose();
  }
}

async function debug() {
  const root = workspaceRoot();
  if (!root) return vscode.window.showErrorMessage("mu debug: open the repo as a workspace folder");
  const folder = vscode.workspace.getWorkspaceFolder(vscode.Uri.file(root));
  await vscode.debug.startDebugging(folder, { type: "mu", request: "launch", name: "mu: current.mu" });
}

function activate(context) {
  context.subscriptions.push(
    vscode.languages.registerDocumentFormattingEditProvider("mu", { provideDocumentFormattingEdits: format }),
    vscode.commands.registerCommand("mu.debug", debug),
    vscode.debug.registerDebugConfigurationProvider("mu", new MuConfigurationProvider()),
    vscode.debug.registerDebugAdapterDescriptorFactory("mu", {
      createDebugAdapterDescriptor: (session) => new vscode.DebugAdapterInlineImplementation(new MuDebugAdapter(session)),
    })
  );
}

module.exports = { activate };
