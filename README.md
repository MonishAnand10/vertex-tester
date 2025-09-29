## Authors

**Dhulipala Siva Tejaswi, Kaushal Girish & Monish Anand**

## Version

**1.0.0** - Complete AI-powered unit test generation with Google Gemini

# Vertex Tester

AI-Powered unit test generation extension that leverages Google Gemini to create comprehensive test cases for your codebase.

## Features

- **Multiple File Selection**: Select multiple Python, JavaScript, or TypeScript files for analysis
- **AI-Powered Test Generation**: Uses Google Gemini 2.5 Flash to generate comprehensive unit tests
- **Function Extraction**: Automatically analyzes code structure and extracts function metadata
- **Class Context Detection**: Identifies functions within classes vs standalone functions  
- **Intelligent Test Creation**: Generates pytest-based tests with normal cases, edge cases, and error handling
- **Real-time Progress**: Shows AI generation progress with streaming output
- **Smart File Naming**: Automatically creates appropriately named test files (test_Calculator.py, test_module.py)

## How to Use

1. **Setup**: Place your Google Cloud API key in `GOOGLE_CLOUD_API_KEY.txt` in the extension folder
2. Open VS Code
3. Press `Ctrl+Shift+P` (or `Cmd+Shift+P` on Mac)
4. Type "Generate Unit Tests with Gemini"
5. Select multiple files you want to generate tests for
6. Extension will process each file and generate comprehensive test files using AI

## Current Status

**Phase 1 Complete**: Code analysis and function extraction  
**Phase 2 Complete**: Gemini AI integration for actual unit test generation  
**Status**: ✅ **Fully Functional AI-Powered Unit Test Generator**

## Requirements

- Python installed on your system
- VS Code 1.104.0 or higher
- Google Cloud API key with Gemini API access
- Required Python packages: `google-generativeai`, `google-genai`

## Installation

1. Clone this repository
2. Install dependencies: `npm install`
3. Install Python packages: `pip install google-generativeai google-genai`
4. Create `GOOGLE_CLOUD_API_KEY.txt` in the root folder with your API key
5. Compile: `npm run compile`
6. Press F5 to test in Extension Development Host

## Output Files

The extension generates two types of files:

### **AI-Generated Test Files** (Primary Output)
- **test_Calculator.py** - Complete pytest-based unit tests
- **test_module.py** - Tests for module-level functions
- Contains normal cases, edge cases, and error handling tests

### **Analysis Metadata** (Debug Output)
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
