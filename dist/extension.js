"use strict";
var __create = Object.create;
var __defProp = Object.defineProperty;
var __getOwnPropDesc = Object.getOwnPropertyDescriptor;
var __getOwnPropNames = Object.getOwnPropertyNames;
var __getProtoOf = Object.getPrototypeOf;
var __hasOwnProp = Object.prototype.hasOwnProperty;
var __export = (target, all) => {
  for (var name in all)
    __defProp(target, name, { get: all[name], enumerable: true });
};
var __copyProps = (to, from, except, desc) => {
  if (from && typeof from === "object" || typeof from === "function") {
    for (let key of __getOwnPropNames(from))
      if (!__hasOwnProp.call(to, key) && key !== except)
        __defProp(to, key, { get: () => from[key], enumerable: !(desc = __getOwnPropDesc(from, key)) || desc.enumerable });
  }
  return to;
};
var __toESM = (mod, isNodeMode, target) => (target = mod != null ? __create(__getProtoOf(mod)) : {}, __copyProps(
  // If the importer is in node compatibility mode or this is not an ESM
  // file that has been converted to a CommonJS file using a Babel-
  // compatible transform (i.e. "__esModule" has not been set), then set
  // "default" to the CommonJS "module.exports" for node compatibility.
  isNodeMode || !mod || !mod.__esModule ? __defProp(target, "default", { value: mod, enumerable: true }) : target,
  mod
));
var __toCommonJS = (mod) => __copyProps(__defProp({}, "__esModule", { value: true }), mod);

// src/extension.ts
var extension_exports = {};
__export(extension_exports, {
  activate: () => activate,
  deactivate: () => deactivate
});
module.exports = __toCommonJS(extension_exports);
var vscode = __toESM(require("vscode"));
var import_child_process = require("child_process");
var path = __toESM(require("path"));
var fs = __toESM(require("fs"));
function activate(context) {
  console.log('Congratulations, your extension "vertex-tester" is now active!');
  const disposable = vscode.commands.registerCommand("vertex-tester.generateTests", async () => {
    const fileUris = await vscode.window.showOpenDialog({
      canSelectMany: true,
      filters: {
        "Python Files": ["py"],
        "JavaScript Files": ["js"],
        "TypeScript Files": ["ts"]
      },
      openLabel: "Select Files to Generate Tests"
    });
    if (!fileUris || fileUris.length === 0) {
      vscode.window.showWarningMessage("No files selected.");
      return;
    }
    const apiKeyPath = path.join(context.extensionPath, "GOOGLE_CLOUD_API_KEY.txt");
    let apiKey;
    try {
      apiKey = fs.readFileSync(apiKeyPath, "utf8").trim();
      if (!apiKey) {
        vscode.window.showErrorMessage("API key file is empty. Please add your Google Cloud API key to GOOGLE_CLOUD_API_KEY.txt");
        return;
      }
    } catch (error) {
      vscode.window.showErrorMessage("Could not read API key file. Please ensure GOOGLE_CLOUD_API_KEY.txt exists in the extension folder.");
      return;
    }
    vscode.window.showInformationMessage(`Selected ${fileUris.length} file(s) for AI test generation.`);
    const outputDir = path.dirname(fileUris[0].fsPath);
    const pythonScriptPath = path.join(context.extensionPath, "main.py");
    for (let i = 0; i < fileUris.length; i++) {
      const filePath = fileUris[i].fsPath;
      const fileName = path.basename(filePath);
      vscode.window.showInformationMessage(`\u{1F916} AI generating tests for file ${i + 1} of ${fileUris.length}: ${fileName}`);
      const command = `python "${pythonScriptPath}" "${filePath}" "${outputDir}" "${apiKey}"`;
      (0, import_child_process.exec)(command, (error, stdout, stderr) => {
        if (error) {
          vscode.window.showErrorMessage(`Error generating tests for ${fileName}: ${error.message}`);
          return;
        }
        if (stderr) {
          console.error(`stderr for ${fileName}:`, stderr);
        }
        vscode.window.showInformationMessage(`SUCCESS: AI test file generated for ${fileName}`);
        console.log(`AI generation results for ${fileName}:`, stdout);
      });
    }
  });
  context.subscriptions.push(disposable);
}
function deactivate() {
}
// Annotate the CommonJS export names for ESM import in node:
0 && (module.exports = {
  activate,
  deactivate
});
//# sourceMappingURL=extension.js.map
