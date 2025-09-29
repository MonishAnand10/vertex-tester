# Change Log

All notable changes to the "vertex-tester" extension will be documented in this file.

Check [Keep a Changelog](http://keepachangelog.com/) for recommendations on how to structure this file.

## [1.0.0] - 2025-01-28

### Added
- **Complete Gemini AI Integration** with Google Gemini 2.5 Flash
- **AI-Powered Test Generation**: Generates actual pytest-based unit test files
- **API Key Management**: Secure API key reading from `GOOGLE_CLOUD_API_KEY.txt`
- **Real-time AI Generation**: Streaming output with progress indicators
- **Smart Test File Naming**: Automatically creates `test_Calculator.py`, `test_module.py` etc.
- **Comprehensive Test Coverage**:
  - Normal operation test cases
  - Edge case and boundary testing
  - Error handling and exception testing
  - Parameterized tests where appropriate
- **Enhanced User Experience**:
  - AI generation progress messages
  - Unicode/emoji compatibility fixes
  - Improved error handling and notifications

### Technical Enhancements
- Google Generative AI library integration
- Command-line API key passing to Python script
- Streaming AI response handling
- Enhanced error detection and user feedback
- Cross-platform compatibility improvements

### Bug Fixes
- Fixed Unicode encoding issues in Windows Command Prompt
- Resolved Python package import dependencies
- Corrected API key file reading and validation
- Enhanced error messages for better debugging

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

### Limitations in v0.0.1
- Analysis only - no actual test generation
- Required manual Gemini AI integration
- Basic error handling

---

## [Unreleased]

Future enhancements planned:
- Configuration options for different test frameworks (unittest, nose2)
- Support for additional programming languages (JavaScript, TypeScript)
- Custom test template configurations
- Integration with popular testing libraries
- Batch processing optimization for large codebases
- Test coverage analysis and reporting

---

## Project Status

**✅ Phase 1 Complete**: Code analysis and function extraction  
**✅ Phase 2 Complete**: Gemini AI integration for unit test generation  
**🎯 Current Status**: Fully functional AI-powered unit test generator

**Authors**: Dhulipala Siva Tejaswi, Kaushal Girish & Monish Anand  
**Publisher**: nuggets-vertex-tester-team
