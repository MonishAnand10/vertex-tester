# Change Log

All notable changes to the "vertex-tester" extension will be documented in this file.

Check [Keep a Changelog](http://keepachangelog.com/) for recommendations on how to structure this file.

## [0.0.1] - 2025-01-28

### Added
- **Initial VS Code extension structure** with TypeScript
- **Multiple file selection dialog** for Python, JavaScript, and TypeScript files
- **Python script integration** for code analysis using AST (Abstract Syntax Tree)
- **Function extraction capabilities**:
  - Function names and signatures
  - Class context detection
  - Line number tracking (start/end)
  - Complete source code extraction
- **Structured JSON output** with function metadata
- **Progress notifications** for user feedback during processing
- **Command palette integration**: "Generate Unit Tests with Gemini"
- **Right-click context menus** for file explorer and editor
- **Error handling** for file processing and Python script execution

### Technical Details
- Built with TypeScript and esbuild
- Python AST parsing for accurate code analysis
- Command-line integration between VS Code and Python
- Supports multiple file processing in sequence
- Generates `summary.json` files with extracted function data

### Current Limitations
- **Analysis only**: Does not yet generate actual unit tests
- **Awaiting Gemini AI integration** for test generation phase
- **Python dependency**: Requires Python installation on user system

### Next Phase
- Integrate Google Vertex AI Gemini 2.5 Flash
- Generate actual unit test code from function metadata
- Save generated tests to appropriate test files
- Enhanced error handling and user experience improvements

---

## [Unreleased]

Future features planned:
- Complete Gemini AI integration
- Unit test file generation
- Configuration options for test frameworks
- Support for additional programming languages