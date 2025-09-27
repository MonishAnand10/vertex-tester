# Vertex Tester

AI-Powered unit test generation extension that leverages Google Gemini to create comprehensive test cases for your codebase.

## Features

- **Multiple File Selection**: Select multiple Python, JavaScript, or TypeScript files for analysis
- **Function Extraction**: Automatically analyzes code structure and extracts function metadata
- **Class Context Detection**: Identifies functions within classes vs standalone functions  
- **Structured Output**: Generates detailed JSON with function signatures, code, and line numbers
- **Ready for AI Integration**: Output format designed for Gemini AI unit test generation

## How to Use

1. Open VS Code
2. Press `Ctrl+Shift+P` (or `Cmd+Shift+P` on Mac)
3. Type "Generate Unit Tests with Gemini"
4. Select multiple files you want to analyze
5. Extension will process each file and generate `summary.json` with function metadata

## Current Status

**Phase 1 Complete**: Code analysis and function extraction  
**Phase 2 Pending**: Gemini AI integration for actual unit test generation

## Requirements

- Python installed on your system
- VS Code 1.104.0 or higher

## Installation

1. Clone this repository
2. Install dependencies: `npm install`
3. Compile: `npm run compile`
4. Press F5 to test in Extension Development Host

## Output Format

The extension generates JSON files with the following structure:

```json
{
  "block_id": "filename.py_0",
  "function_name": "function_name",
  "class_context": "ClassName" || null,
  "start_line": 10,
  "end_line": 15,
  "signature": "def function_name(params):",
  "code": "complete function code"
}