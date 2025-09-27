/**
 * Vertex Tester VS Code Extension
 * 
 * AI-Powered unit test generation extension that leverages Google Gemini 
 * to create comprehensive test cases for your codebase.
 * 
 * Phase 1: Code analysis and function extraction (COMPLETE)
 * Phase 2: Gemini AI integration for test generation (PENDING)
 * 
 * @author Your Name
 * @version 0.0.1
 */

// The module 'vscode' contains the VS Code extensibility API
// Import the module and reference it with the alias vscode in your code below
import * as vscode from 'vscode';
import { exec } from 'child_process';
import * as path from 'path';
/**
 * This method is called when your extension is activated
 * Your extension is activated the very first time the command is executed
 */
export function activate(context: vscode.ExtensionContext) {

	/// Use the console to output diagnostic information (console.log) and errors (console.error)
	// This line of code will only be executed once when your extension is activated
	console.log('Congratulations, your extension "vertex-tester" is now active!');

	/**
	 * Main command: Generate Unit Tests with Gemini
	 * 
	 * Workflow:
	 * 1. Show file picker for multiple file selection
	 * 2. Validate selected files
	 * 3. Process each file with Python script (main.py)
	 * 4. Generate structured JSON output with function metadata
	 * 5. Display progress and results to user
	 */
	const disposable = vscode.commands.registerCommand('vertex-tester.generateTests', async () => {
		// Show file picker for multiple file selection
		const fileUris = await vscode.window.showOpenDialog({
			canSelectMany: true,
			filters: {
				'Python Files': ['py'],
				'JavaScript Files': ['js'],
				'TypeScript Files': ['ts']
			},
			openLabel: 'Select Files to Generate Tests'
		});

		if (!fileUris || fileUris.length === 0) {
			vscode.window.showWarningMessage('No files selected.');
			return;
		}

		// Show selected files count
		vscode.window.showInformationMessage(`Selected ${fileUris.length} file(s) for test generation.`);
		
		// Process each file with Python script
		const outputDir = path.dirname(fileUris[0].fsPath); // Use first file's directory for output
		const pythonScriptPath = path.join(context.extensionPath, 'main.py');

		for (let i = 0; i < fileUris.length; i++) {
			const filePath = fileUris[i].fsPath;
			const fileName = path.basename(filePath);
			
			vscode.window.showInformationMessage(`Processing file ${i + 1} of ${fileUris.length}: ${fileName}`);
			
			const command = `python "${pythonScriptPath}" "${filePath}" "${outputDir}"`;
			
			exec(command, (error, stdout, stderr) => {
				if (error) {
					vscode.window.showErrorMessage(`Error processing ${fileName}: ${error.message}`);
					return;
				}
				if (stderr) {
					console.error(`stderr for ${fileName}:`, stderr);
				}
				
				vscode.window.showInformationMessage(`✅ Generated tests for ${fileName}`);
				console.log(`Results for ${fileName}:`, stdout);
			});
		}
	});

	context.subscriptions.push(disposable);
}

/**
 * This method is called when your extension is deactivated
 * Cleanup code can be added here if needed
 */
export function deactivate() {}
// Currently no cleanup required
