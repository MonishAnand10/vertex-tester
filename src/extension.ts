/**
 * Vertex Tester VS Code Extension
 * 
 * AI-Powered unit test generation extension that leverages Google Gemini 
 * to create comprehensive test cases for your codebase.
 * 
 * Phase 1: Code analysis and function extraction (COMPLETE)
 * Phase 2: Gemini AI integration for test generation (COMPLETE)
 * Phase 3: Multi-language support (Python & Java) (COMPLETE)
 * 
 * @author Dhulipala Siva Tejaswi, Kaushal Girish & Monish Anand
 * @version 1.1.0
 */

// The module 'vscode' contains the VS Code extensibility API
// Import the module and reference it with the alias vscode in your code below
import * as vscode from 'vscode';
import { exec } from 'child_process';
import * as path from 'path';
import * as fs from 'fs';

/**
 * This method is called when your extension is activated
 * Your extension is activated the very first time the command is executed
 */
export function activate(context: vscode.ExtensionContext) {

	// Use the console to output diagnostic information (console.log) and errors (console.error)
	// This line of code will only be executed once when your extension is activated
	console.log('Congratulations, your extension "vertex-tester" is now active!');

	/**
	 * Main command: Generate Unit Tests with Gemini
	 * 
	 * Workflow:
	 * 1. Show file picker for multiple file selection (Python, Java, JavaScript, TypeScript)
	 * 2. Validate selected files and detect programming language
	 * 3. Read API key from GOOGLE_CLOUD_API_KEY.txt
	 * 4. Process each file with Python script (main.py) + AI generation
	 * 5. Generate appropriate unit test files using Gemini AI (pytest/JUnit)
	 * 6. Display progress and results to user
	 */
	const disposable = vscode.commands.registerCommand('vertex-tester.generateTests', async () => {
		
		// Show file picker for multiple file selection with multi-language support
		const fileUris = await vscode.window.showOpenDialog({
			canSelectMany: true,
			filters: {
				'All Supported Files': ['py', 'java', 'js', 'ts'],
				'Python Files': ['py'],
				'Java Files': ['java'],
				'JavaScript Files': ['js'],
				'TypeScript Files': ['ts']
			},
			openLabel: 'Select Files to Generate Tests'
		});

		if (!fileUris || fileUris.length === 0) {
			vscode.window.showWarningMessage('No files selected.');
			return;
		}

		// Read API key from file
		const apiKeyPath = path.join(context.extensionPath, 'GOOGLE_CLOUD_API_KEY.txt');
		let apiKey: string;
		
		try {
			apiKey = fs.readFileSync(apiKeyPath, 'utf8').trim();
			if (!apiKey) {
				vscode.window.showErrorMessage('API key file is empty. Please add your Google Cloud API key to GOOGLE_CLOUD_API_KEY.txt');
				return;
			}
		} catch (error) {
			vscode.window.showErrorMessage('Could not read API key file. Please ensure GOOGLE_CLOUD_API_KEY.txt exists in the extension folder.');
			return;
		}

		// Show selected files count with multi-language support
		vscode.window.showInformationMessage(`Selected ${fileUris.length} file(s) for multi-language AI test generation.`);
		
		// Setup paths for Python script execution
		// Create organized tests folder structure
		const baseDir = path.dirname(fileUris[0].fsPath); // Get base directory where files were picked
		const testsDir = path.join(baseDir, 'tests'); // Create tests subdirectory path

		// Create tests directory if it doesn't exist
		try {
			if (!fs.existsSync(testsDir)) {
				fs.mkdirSync(testsDir, { recursive: true });
				console.log(`Created tests directory: ${testsDir}`);
			}
		} catch (error) {
			vscode.window.showErrorMessage(`Failed to create tests directory: ${error}`);
			return;
		}

		const outputDir = testsDir; // Use tests directory for all output files
		const pythonScriptPath = path.join(context.extensionPath, 'main.py');

		// Process each selected file individually with AI generation and language detection
		for (let i = 0; i < fileUris.length; i++) {
			const filePath = fileUris[i].fsPath;
			const fileName = path.basename(filePath);
			const fileExtension = path.extname(filePath).toLowerCase();
			
			// Determine language for user feedback
			let language = 'Unknown';
			if (fileExtension === '.py') {language = 'Python';}
			else if (fileExtension === '.java') {language = 'Java';}
			else if (fileExtension === '.js') {language = 'JavaScript';}
			else if (fileExtension === '.ts') {language = 'TypeScript';}
			
			// Show progress to user with language information
			vscode.window.showInformationMessage(`🤖 AI generating ${language} tests for file ${i + 1} of ${fileUris.length}: ${fileName}`);
			
			// Construct Python command with file path, output directory, and API key
			// The main.py script will automatically detect the programming language
			const command = `python "${pythonScriptPath}" "${filePath}" "${outputDir}" "${apiKey}"`;
			
			// Execute Python script with AI generation
			exec(command, (error, stdout, stderr) => {
				if (error) {
					// Handle Python script execution errors
					vscode.window.showErrorMessage(`ERROR: Error generating tests for ${fileName}: ${error.message}`);
					return;
				}
				if (stderr) {
					// Log any warnings or non-fatal errors
					console.error(`stderr for ${fileName}:`, stderr);
				}
				
				// Notify user of successful AI test generation with language context
				vscode.window.showInformationMessage(`SUCCESS: AI ${language} test file generated for ${fileName}`);
				
				// Log results for debugging (includes AI generation progress)
				console.log(`AI generation results for ${fileName}:`, stdout);
			});
		}
	});

	// Register the command with VS Code
	context.subscriptions.push(disposable);
}

/**
 * This method is called when your extension is deactivated
 * Cleanup code can be added here if needed
 */
export function deactivate() {
	// Currently no cleanup required
}
