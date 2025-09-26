// The module 'vscode' contains the VS Code extensibility API
// Import the module and reference it with the alias vscode in your code below
import * as vscode from 'vscode';

// This method is called when your extension is activated
// Your extension is activated the very first time the command is executed
export function activate(context: vscode.ExtensionContext) {

	// Use the console to output diagnostic information (console.log) and errors (console.error)
	// This line of code will only be executed once when your extension is activated
	console.log('Congratulations, your extension "vertex-tester" is now active!');

	// The command has been defined in the package.json file
	// Now provide the implementation of the command with registerCommand
	// The commandId parameter must match the command field in package.json
	const disposable = vscode.commands.registerCommand('vertex-tester.generateTests', () => {
		// Get the current active editor
		const activeEditor = vscode.window.activeTextEditor;
		
		if (!activeEditor) {
			vscode.window.showErrorMessage('No file is currently open. Please open a file to generate tests.');
			return;
		}

		// Get the file path
		const filePath = activeEditor.document.uri.fsPath;
		const fileName = activeEditor.document.fileName;

		// For now, just show the file path (we'll add Python script call later)
		vscode.window.showInformationMessage(`Generating tests for: ${fileName}`);
		
		// TODO: Call Python script here with filePath
		console.log('File path to process:', filePath);
	});

	context.subscriptions.push(disposable);
}

// This method is called when your extension is deactivated
export function deactivate() {}
