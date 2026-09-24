// Formats .mu files by piping the document through `mu.py --fmt -`.
const vscode = require("vscode");
const path = require("path");
const { execFile } = require("child_process");

const MU = path.join(__dirname, "..", "mu.py");

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

function activate(context) {
  context.subscriptions.push(
    vscode.languages.registerDocumentFormattingEditProvider("mu", { provideDocumentFormattingEdits: format })
  );
}

module.exports = { activate };
