**Here's your updated README.md with full Java support:**

```markdown
# Vertex Tester

Multi-language AI-powered unit test generation extension that leverages Google Gemini to create comprehensive test cases for your Python and Java codebases.

## Features

- **Multi-Language Support**: Full support for Python and Java with automatic language detection
- **Multiple File Selection**: Select multiple Python, Java, JavaScript, or TypeScript files for analysis
- **AI-Powered Test Generation**: Uses Google Gemini 2.5 Flash to generate comprehensive unit tests
- **Language-Specific Frameworks**: Generates pytest tests for Python and JUnit-compatible tests for Java
- **Intelligent Code Analysis**: 
  - Python: AST parsing for functions, methods, and async functions
  - Java: Complete method and constructor extraction with package context
- **Class Context Detection**: Identifies functions within classes vs standalone functions  
- **Enterprise-Scale Processing**: Token management and batch processing for large codebases
- **Intelligent Test Creation**: Generates comprehensive tests with normal cases, edge cases, and error handling
- **Real-time Progress**: Shows AI generation progress with streaming output
- **Smart File Naming**: Automatically creates appropriately named test files (test_Calculator.py, test_Calculator.java)

## How to Use

1. **Setup**: Place your Google Cloud API key in `GOOGLE_CLOUD_API_KEY.txt` in the extension folder
2. Open VS Code
3. Press `Ctrl+Shift+P` (or `Cmd+Shift+P` on Mac)
4. Type "Generate Unit Tests with Gemini"
5. Select multiple Python (.py) and/or Java (.java) files you want to generate tests for
6. Extension will automatically detect the programming language and generate appropriate test files using AI

## Current Status

**Phase 1 Complete**: Code analysis and function extraction  
**Phase 2 Complete**: Gemini AI integration for actual unit test generation  
**Phase 3 Complete**: Multi-language support (Python & Java)  
**Status**: ✅ **Fully Functional Multi-Language AI-Powered Unit Test Generator**

## Requirements

- Python installed on your system
- VS Code 1.104.0 or higher
- Google Cloud API key with Gemini API access
- Required Python packages: `google-generativeai`, `google-genai`, `tiktoken`, `javalang`

## Installation

1. Clone this repository
2. Install dependencies: `npm install`
3. Install Python packages: `pip install google-generativeai google-genai tiktoken javalang`
4. Create `GOOGLE_CLOUD_API_KEY.txt` in the root folder with your API key
5. Compile: `npm run compile`
6. Press F5 to test in Extension Development Host

## Output Files

The extension generates language-specific test files:

### **AI-Generated Test Files** (Primary Output)

#### **Python Tests:**
- **test_Calculator.py** - Complete pytest-based unit tests
- **test_module.py** - Tests for module-level functions
- Contains normal cases, edge cases, and error handling tests

#### **Java Tests:**
- **test_Calculator.java** - Complete JUnit-compatible unit tests  
- **test_Module.java** - Tests for class methods and constructors
- Includes method testing, constructor validation, and exception handling

### **Analysis Metadata** (Debug Output)
```json
{
  "block_id": "filename.py_0",
  "function_name": "function_name",
  "class_context": "ClassName" || null,
  "package_context": "com.example" || null,
  "start_line": 10,
  "end_line": 15,
  "signature": "def function_name(params):",
  "code": "complete function code",
  "language": "python"
}
```

## Example Generated Tests

### **Python Test Example:**
```python
from calculator import Calculator
import pytest

def test_Calculator_divide_normal():
    calc = Calculator()
    assert calc.divide(10, 2) == 5

def test_Calculator_divide_zero_raises():
    calc = Calculator()
    with pytest.raises(ZeroDivisionError) as excinfo:
        calc.divide(5, 0)
    assert "Cannot divide by zero" in str(excinfo.value)
```

### **Java Test Example:**
```java
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class test_Calculator {
    
    @Test
    public void test_Calculator_divide_normal() {
        Calculator calc = new Calculator();
        assertEquals(5.0, calc.divide(10, 2), 0.001);
    }
    
    @Test
    public void test_Calculator_divide_zero_throws() {
        Calculator calc = new Calculator();
        assertThrows(ArithmeticException.class, () -> {
            calc.divide(5, 0);
        });
    }
}
```

## Supported Languages

| Language   | Parser      | Test Framework | File Extensions |
|------------|-------------|----------------|-----------------|
| Python     | AST         | pytest         | .py             |
| Java       | javalang    | JUnit          | .java           |
| JavaScript | Basic       | Coming Soon    | .js             |
| TypeScript | Basic       | Coming Soon    | .ts             |

## Architecture

- **Multi-Language Detection**: Automatic programming language identification
- **Language-Specific Parsers**: Python AST and Java javalang integration
- **Token Management**: Intelligent batching for large enterprise codebases
- **AI Integration**: Google Gemini 2.5 Flash with language-specific prompting
- **Scalable Processing**: Batch processing with real-time progress tracking

## Authors

**Dhulipala Siva Tejaswi, Kaushal Girish & Monish Anand**

## Version

**1.1.0** - Multi-language AI-powered unit test generation with Python and Java support
```

## **🎯 Key Updates Made:**

### **✅ Multi-Language Focus:**
- **Updated title and description** to highlight multi-language support
- **Added Java throughout** all relevant sections
- **Language-specific examples** for both Python and Java

### **✅ Enhanced Features:**
- **Language detection** and automatic processing
- **Framework-specific output** (pytest vs JUnit)
- **Enterprise processing** with token management

### **✅ Complete Requirements:**
- **Added new packages**: `tiktoken`, `javalang`
- **Updated version** to 1.1.0
- **Language support table** for clarity

### **✅ Professional Presentation:**
- **Example code blocks** for both languages
- **Architecture overview** of multi-language capabilities
- **Comprehensive feature list** with technical details
