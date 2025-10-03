"""
Vertex Tester - Multi-Language AI-Powered Unit Test Generation

This script analyzes Python and Java source code using language-specific parsers
to extract function/method metadata for AI-powered unit test generation.

Usage:
    python main.py <file_path> <output_dir> <api_key>

Input:
    - file_path: Path to Python (.py) or Java (.java) file to analyze
    - output_dir: Directory where test files will be saved
    - api_key: Google Cloud API key for Gemini AI

Output:
    - summary.json: Function/method metadata (for debugging)
    - test_<module>.py/java: AI-generated unit test files

Features:
    - Multi-language support (Python & Java)
    - Automatic language detection based on file extension
    - Python: AST parsing for functions, methods, and async functions
    - Java: Full method and constructor extraction with package context
    - Intelligent token management for large codebases
    - Batch processing for enterprise-scale projects
    - AI-powered test generation with language-specific frameworks
    - Comprehensive error handling and progress tracking

Authors: Dhulipala Siva Tejaswi, Kaushal Girish & Monish Anand
Version: 1.0.0
Date: 2025-01-28
"""

import ast
import os
import json
import sys
import tiktoken
from google import genai
from google.genai import types
import javalang

# Command line argument validation and extraction
if len(sys.argv) < 4:
    print("Usage: python main.py <file_path> <output_dir> <api_key>")
    sys.exit(1)

# Get arguments from command line
file_path = sys.argv[1]
out_dir = sys.argv[2] 
api_key = sys.argv[3]

class unittester:
    """
    Multi-language AI-powered unit test generator using Google Gemini.
    
    Combines language-specific code analysis with AI to generate comprehensive
    unit tests for Python (pytest) and Java (JUnit) functions and methods.
    """
    
    @staticmethod
    def detect_language(file_path):
        """
        Detect programming language based on file extension.
        
        Args:
            file_path: Path to the source file
            
        Returns:
            str: Detected language ('python' or 'java')
            
        Raises:
            ValueError: If file extension is not supported
        """
        _, ext = os.path.splitext(file_path.lower())
        if ext == '.py':
            return 'python'
        elif ext == '.java':
            return 'java'
        else:
            raise ValueError(f"Unsupported file type: {ext}")
    
    @staticmethod
    def parse_python_file(src, file_path):
        """
        Parse Python file using AST and extract function/method information.
        
        Args:
            src: Source code content
            file_path: Path to the source file
            
        Returns:
            list: Function metadata dictionaries
            
        Raises:
            ValueError: If Python syntax errors are encountered
        """
        try:
            tree = ast.parse(src)
        except SyntaxError as e:
            raise ValueError(f"SyntaxError while parsing Python: {e}")

        parent_map = {}
        for parent in ast.walk(tree):
            for child in ast.iter_child_nodes(parent):
                parent_map[child] = parent

        idx = 0
        blocks = []

        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                name = node.name

                # Determine nearest class context, if any
                class_ctx = None
                cur = node
                while cur in parent_map:
                    cur = parent_map[cur]
                    if isinstance(cur, ast.ClassDef):
                        class_ctx = cur.name
                        break

                # Get exact source segment for this function
                code_segment = ast.get_source_segment(src, node)
                if code_segment is None:
                    start = getattr(node, 'lineno', None)
                    end = getattr(node, 'end_lineno', None) or (start or 0)
                    code_segment = "\n".join(src.splitlines()[start-1:end])

                # Extract signature line
                signature_line = ""
                for line in code_segment.splitlines():
                    if line.strip().startswith("def "):
                        signature_line = line.strip()
                        break

                start_line = getattr(node, 'lineno', None)
                end_line = getattr(node, 'end_lineno', None)

                block = {
                    "block_id": f"{os.path.basename(file_path)}_{idx}",
                    "function_name": name,
                    "class_context": class_ctx,
                    "start_line": start_line,
                    "end_line": end_line,
                    "signature": signature_line,
                    "code": code_segment,
                    "language": "python"
                }
                blocks.append(block)
                idx += 1

        return blocks

    @staticmethod
    def parse_java_file(src, file_path):
        """
        Parse Java file using javalang and extract method/constructor information.
        
        Args:
            src: Source code content
            file_path: Path to the source file
            
        Returns:
            list: Method/constructor metadata dictionaries
            
        Raises:
            ImportError: If javalang library is not available
            ValueError: If Java parsing errors are encountered
        """
        if javalang is None:
            raise ImportError("javalang library is required for Java parsing")

        try:
            tree = javalang.parse.parse(src)
        except Exception as e:
            raise ValueError(f"Error parsing Java file: {e}")

        blocks = []
        idx = 0
        lines = src.splitlines()

        # Extract package name
        package_name = tree.package.name if tree.package else None

        for path, node in tree.filter(javalang.tree.ClassDeclaration):
            class_name = node.name
           
            # Get all methods in this class
            for method_path, method_node in node.filter(javalang.tree.MethodDeclaration):
                method_name = method_node.name
               
                # Extract method signature
                params = []
                if method_node.parameters:
                    for param in method_node.parameters:
                        param_type = param.type.name if hasattr(param.type, 'name') else str(param.type)
                        params.append(f"{param_type} {param.name}")
               
                return_type = method_node.return_type.name if method_node.return_type and hasattr(method_node.return_type, 'name') else 'void'
                signature = f"public {return_type} {method_name}({', '.join(params)})"
               
                # Get method source code (approximate)
                start_line = method_node.position.line if method_node.position else None
                end_line = start_line
               
                # Try to find method end (basic heuristic)
                if start_line:
                    brace_count = 0
                    method_started = False
                    method_lines = []
                   
                    for i, line in enumerate(lines[start_line-1:], start_line):
                        method_lines.append(line)
                        if '{' in line:
                            brace_count += line.count('{')
                            method_started = True
                        if '}' in line:
                            brace_count -= line.count('}')
                       
                        if method_started and brace_count == 0:
                            end_line = i
                            break
                   
                    code_segment = '\n'.join(method_lines)
                else:
                    code_segment = f"// Method {method_name} - source extraction failed"

                block = {
                    "block_id": f"{os.path.basename(file_path)}_{idx}",
                    "function_name": method_name,
                    "class_context": class_name,
                    "package_context": package_name,
                    "start_line": start_line,
                    "end_line": end_line,
                    "signature": signature,
                    "code": code_segment,
                    "language": "java"
                }
                blocks.append(block)
                idx += 1

            # Also get constructors
            for constructor_path, constructor_node in node.filter(javalang.tree.ConstructorDeclaration):
                constructor_name = constructor_node.name
               
                # Extract constructor signature
                params = []
                if constructor_node.parameters:
                    for param in constructor_node.parameters:
                        param_type = param.type.name if hasattr(param.type, 'name') else str(param.type)
                        params.append(f"{param_type} {param.name}")
               
                signature = f"public {constructor_name}({', '.join(params)})"
               
                # Get constructor source code (approximate)
                start_line = constructor_node.position.line if constructor_node.position else None
                end_line = start_line
               
                if start_line:
                    brace_count = 0
                    constructor_started = False
                    constructor_lines = []
                   
                    for i, line in enumerate(lines[start_line-1:], start_line):
                        constructor_lines.append(line)
                        if '{' in line:
                            brace_count += line.count('{')
                            constructor_started = True
                        if '}' in line:
                            brace_count -= line.count('}')
                       
                        if constructor_started and brace_count == 0:
                            end_line = i
                            break
                   
                    code_segment = '\n'.join(constructor_lines)
                else:
                    code_segment = f"// Constructor {constructor_name} - source extraction failed"

                block = {
                    "block_id": f"{os.path.basename(file_path)}_{idx}",
                    "function_name": constructor_name,
                    "class_context": class_name,
                    "package_context": package_name,
                    "start_line": start_line,
                    "end_line": end_line,
                    "signature": signature,
                    "code": code_segment,
                    "language": "java",
                    "is_constructor": True
                }
                blocks.append(block)
                idx += 1

        return blocks
    
    @staticmethod
    def mainProcessor():
        """
        Main processing method that analyzes code and generates AI-powered tests.
        
        Automatically detects language, parses source code, and generates
        appropriate unit tests using Google Gemini AI.
        
        Returns:
            str: Path to generated test file, or None if failed
        """
        
        # Read and parse the source file
        with open(file_path, 'r', encoding='utf-8') as file:
            src = file.read()
        
        # Detect language
        language = unittester.detect_language(file_path)
        print(f"Detected language: {language}")
        
        # Parse based on language
        if language == 'python':
            blocks = unittester.parse_python_file(src, file_path)
        elif language == 'java':
            blocks = unittester.parse_java_file(src, file_path)
        else:
            raise ValueError(f"Unsupported language: {language}")

        # Save analysis results for debugging
        summary_path = os.path.join(out_dir, "summary.json")
        with open(summary_path, 'w', encoding='utf-8') as f:
            json.dump(blocks, f, indent=2)

        print(f"Found {len(blocks)} functions/methods to test")
        
        # Generate AI-powered tests
        return unittester.generate_tests(blocks, language)

    @staticmethod
    def count_tokens(text: str) -> int:
        """
        Count tokens in text for batch processing optimization.
        
        Args:
            text: Text content to analyze
            
        Returns:
            int: Estimated token count
        """
        try:
            enc = tiktoken.encoding_for_model("cl100k_base")
            return len(enc.encode(text))
        except Exception:
            return max(1, len(text.split()))

    @staticmethod    
    def batch_blocks_by_tokens(blocks, max_tokens_per_batch: int):
        """
        Group code blocks into batches for efficient API processing.
        
        Args:
            blocks: List of function/method metadata
            max_tokens_per_batch: Maximum tokens allowed per batch
            
        Returns:
            list: List of batched block groups
        """
        if not blocks:
            return []

        batches = []
        current_batch = []
        current_tokens = 0

        for b in blocks:
            block_text = json.dumps(b, ensure_ascii=False)
            t = unittester.count_tokens(block_text)

            if t > max_tokens_per_batch:
                # This single block doesn't fit in the budget.
                if current_batch:
                    batches.append(current_batch)
                    current_batch = []
                    current_tokens = 0
                batches.append([b])
                continue

            if current_batch and (current_tokens + t) > max_tokens_per_batch:
                batches.append(current_batch)
                current_batch = []
                current_tokens = 0

            current_batch.append(b)
            current_tokens += t

        if current_batch:
            batches.append(current_batch)

        return batches    

    @staticmethod
    def generate_tests(blocks, language):
        """
        Generate unit tests using Google Gemini AI with language-specific optimization.
        
        Args:
            blocks: List of function/method metadata dictionaries
            language: Programming language ('python' or 'java')
            
        Returns:
            str: Path to generated test file, or None if failed
        """
        
        # Batch processing for large codebases
        per_batch_tokens = 195000
        batches = unittester.batch_blocks_by_tokens(blocks, per_batch_tokens)
        
        print(f"Processing {len(batches)} batch(es)...")
        
        if not api_key:
            raise ValueError("API key is required for test generation")
        
        # Determine file extension based on language
        if language == "python":
            ext = "py"
        else:
            ext = "java"    
        
        try:
            # Initialize Gemini client
            client = genai.Client(
                vertexai=True,
                api_key=api_key,
            )

            # Dynamic system instructions based on detected language
            si_text1 = """Purpose

            Produce a complete {language} unit test file for one or more code blocks described by JSON objects with fields like block_id, function_name, class_context, start_line, end_line, signature, and code.
            Input format your model will receive

            A JSON object (or an array of such objects), where each object (block) has:
            block_id: a string like \"calculator.{ext}_7\" that identifies the module and block index
            function_name: the name of the function or method to test
            class_context: the class that contains the function, or null/empty if it is a module-level function
            start_line: the starting line number of the block in the source file
            end_line: the ending line number of the block in the source file
            signature: the function/method signature, e.g., \"def divide(self, a, b):\"
            code: the full code string for the block (may include exception raises, guards, etc.)
            Output format you should produce

            A single file containing tests for all blocks described, or a separate test file per module if your workflow requires it. The instruction below focuses on a single test file per module, named test_<module>.{ext}.
            Naming and organization rules

            Derive the module name from block_id by taking the portion before the underscore. Example: for \"calculator.{ext}_7\", module_name is \"calculator.{ext}\".
            Name the test file as test_<module_name_without_extension>.{ext}. For example: test_calculator.{ext}.
            If there are multiple blocks referring to the same module, generate all appropriate tests into that single test_<module_name>.{ext} file.
            If there are blocks from different modules, produce separate test files for each module (e.g., test_another_module.{ext} for another_module.{ext}).
            Test generation guidelines per block

            If class_context is provided (i.e., testing a method of a class):
            Import the class from the corresponding module: from <module_name_without_{ext}> import <ClassName>
            Instantiate the class in each test: obj = ClassName()
            Call the target method on the instance: obj.<function_name>(...)
            Use the provided signature to determine argument types and counts, but if the exact values are not provided in the JSON, choose representative, sensible test inputs that exercise normal operation and edge cases.
            Suggested normal case tests: pick common positive numbers (e.g., 10 and 2 for divide) or typical inputs based on the function purpose.
            Suggested edge cases:
            If the function raises a specific exception for certain input (for example, divide by zero), write a test that asserts the exception is raised with the expected message.
            If class_context is not provided (module-level function):
            Import the function from the module: from <module_name_without_{ext}> import <function_name>
            Write tests calling the function directly with representative inputs.
            Recommended test cases to include per block (adjust as appropriate to the function's purpose implied by the code):
            Normal operation: verifies expected return value for typical inputs.
            Boundary/edge case: tests inputs that could reveal edge behavior (e.g., zero divisions, empty strings, very large numbers, etc., depending on the function's purpose).
            Error/exception path: tests that the function raises the correct exception type and message when given invalid input (as shown in the sample code with ZeroDivisionError and message \"Cannot divide by zero.\").
            Test naming conventions:
            For methods: test_<ClassName><functionName>normal, test<ClassName><functionName>edge, test<ClassName>_<functionName>_raises
            For module-level functions: test_<functionName>normal, test<functionName>_raises
            Include the module context in the test name when helpful to avoid ambiguity.
            Code quality and style

            Use appropriate testing framework for tests; do not rely on unittest unless the project requires it.
            Keep tests simple, deterministic, and independent.
            Use clear assertions:
            assert result == expected
            with pytest.raises(ExpectedException) as excinfo: ... assert \"expected message\" in str(excinfo.value)
            Import paths:
            For module imports, use absolute imports based on the module name derived from block_id (e.g., from calculator import Calculator or from calculator import add)
            Do not include system prompts or explanations in the output; only the {language} test code.
            Handling multiple blocks and conflicts

            If multiple blocks map to the same module and include different functions/methods, include all corresponding tests in the same test_<module>.{ext} file.
            If a block cannot be tested fully with the information provided (e.g., missing concrete input values), include tests with sensible placeholder inputs and clearly marked TODOs in comments to guide future refinement.
            Example structure (illustrative, not literal output)

            For a block with block_id \"calculator.{ext}_7\" and a class Calculator with a divide(self, a, b) method:
            Module: calculator.{ext}
            Test file: test_calculator.{ext}
            Tests (illustrative, in {language}):
            from calculator import Calculator
            import test-module
            def test_Calculator_divide_normal(): calc = Calculator() assert calc.divide(10, 2) == 5
            def test_Calculator_divide_zero_raises(): calc = Calculator() with pytest.raises(ZeroDivisionError) as excinfo: calc.divide(5, 0) assert \"Cannot divide by zero.\" in str(excinfo.value)
            What to output in response

            The system should output only the generated test file content (no explanations or meta-text) when given a valid JSON block or blocks. If you cannot create tests for some blocks due to missing information, you can skip those blocks or insert TODO comments in the test file, but do not fail the entire test file generation.
            Optional enhancements you may implement if desired. do not add "``` {language} ```" in the start and end of the file.

            Except for the tests and one line comment explaining each test nothing else should be there in the file.

            Support parameterized tests to cover multiple input scenarios per block.
            Infer simple test inputs from the function signature types when possible (e.g., numeric types for functions with a and b that look like numbers).
            Produce a concise header comment in the test file describing which blocks were used to generate the tests."""

            model = "gemini-2.5-flash"
            
            generate_content_config = types.GenerateContentConfig(
                temperature = 1,
                top_p = 1,
                max_output_tokens = 65535,
                safety_settings = [types.SafetySetting(
                category="HARM_CATEGORY_HATE_SPEECH",
                threshold="OFF"
                ),types.SafetySetting(
                category="HARM_CATEGORY_DANGEROUS_CONTENT",
                threshold="OFF"
                ),types.SafetySetting(
                category="HARM_CATEGORY_SEXUALLY_EXPLICIT",
                threshold="OFF"
                ),types.SafetySetting(
                category="HARM_CATEGORY_HARASSMENT",
                threshold="OFF"
                )],
                system_instruction=[types.Part.from_text(text=si_text1.format(language=language, ext=ext))],
                thinking_config=types.ThinkingConfig(
                thinking_budget=-1,
                ),
            )
            
            # Determine test file name
            if blocks:
                module_name = blocks[0]["block_id"].split("_")[0]
                class_name = None
                for block in blocks:
                    if block.get("class_context"):
                        class_name = block["class_context"]
                        break
                
                # Create test filename
                if class_name:
                    test_filename = f"test_{class_name}.{ext}"
                else:
                    # Use module name without extension
                    base_module = os.path.splitext(module_name)[0]
                    test_filename = f"test_{base_module}.{ext}"
            else:
                test_filename = f"test_generated.{ext}"
            
            test_path = os.path.join(out_dir, test_filename)

            # Process batches with streaming output
            for batch_idx, batch in enumerate(batches):
                print(f"\nProcessing batch {batch_idx + 1}/{len(batches)}: |", end=" ", flush=True)
                
                contents = [
                    types.Content(
                    role="user",
                    parts=[
                        {
                        "text": json.dumps(batch, indent=2)
                        }
                    ]
                    )
                ]
                
                # Open file in append mode for batches after the first
                mode = "w" if batch_idx == 0 else "a"
                
                with open(test_path, mode, encoding='utf-8') as f:
                    if batch_idx > 0:
                        f.write("\n\n")  # Add spacing between batches
                        
                    for chunk in client.models.generate_content_stream(
                        model = model,
                        contents = contents,
                        config = generate_content_config,
                        ):
                        if chunk.text:
                            f.write(chunk.text)
                            print('#', end="", flush=True)
                    print(" done!")
            
            print(f"\nAll AI tests generated successfully: {test_path}")
            return test_path
                
        except Exception as e:
            print(f"\nError generating AI tests: {e}")
            return None


if __name__ == "__main__":
    try:
        result = unittester.mainProcessor()
        if result:
            print(f"SUCCESS: Test file created: {result}")
        else:
            print("FAILED: Failed to generate test file")
    except Exception as e:
        print(f"ERROR: {e}")
        