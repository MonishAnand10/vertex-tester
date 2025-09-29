"""
Vertex Tester - Python Code Analysis Module

This script analyzes Python source code using Abstract Syntax Tree (AST) parsing
to extract function metadata for unit test generation.

Usage:
    python main.py <file_path> <output_dir>

Input:
    - file_path: Path to Python file to analyze
    - output_dir: Directory where summary.json will be saved

Output:
    - summary.json: Structured JSON with function metadata
    - Console: JSON array of extracted functions

Features:
    - Extracts all function definitions (regular and async)
    - Detects class context for methods
    - Captures function signatures and complete source code
    - Tracks line numbers for precise location mapping
    - Handles syntax errors gracefully

Authors: Dhulipala Siva Tejaswi, Kaushal Girish & Monish Anand
Version: 0.0.1
Date: 2025-01-28
"""

import ast
import os
import json
import sys
from google import genai
from google.genai import types

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
    AI-powered unit test generator using Google Gemini.
    
    Combines AST code analysis with AI to generate comprehensive
    pytest-based unit tests for Python functions and methods.
    """
    
    @staticmethod
    def mainProcessor():
        """
        Main processing method that analyzes code and generates AI-powered tests.
        
        Returns:
            str: Path to generated test file, or None if failed
        """
        
        # Read and parse the source file
        with open(file_path, 'r', encoding='utf-8') as file:
            src = file.read()
            
        try:
            tree = ast.parse(src)
        except SyntaxError as e:
            raise ValueError(f"SyntaxError while parsing {file_path}: {e}")

        # Build parent-child relationship map for AST nodes
        parent_map = {}
        for parent in ast.walk(tree):
            for child in ast.iter_child_nodes(parent):
                parent_map[child] = parent

        print("Processing AST nodes...")
        idx = 0
        blocks = []

        # Extract function metadata
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                name = node.name

                # Determine class context
                class_ctx = None
                cur = node
                while cur in parent_map:
                    cur = parent_map[cur]
                    if isinstance(cur, ast.ClassDef):
                        class_ctx = cur.name
                        break

                # Extract source code segment
                code_segment = ast.get_source_segment(src, node)
                if code_segment is None:
                    start = getattr(node, 'lineno', None)
                    end = getattr(node, 'end_lineno', None) or (start or 0)
                    code_segment = "\n".join(src.splitlines()[start-1:end])

                # Extract function signature
                signature_line = ""
                for line in code_segment.splitlines():
                    if line.strip().startswith("def "):
                        signature_line = line.strip()
                        break
                if not signature_line:
                    for line in code_segment.splitlines():
                        if line.strip():
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
                    "code": code_segment
                }
                blocks.append(block)
                idx += 1

        # Save analysis results for debugging
        summary_path = os.path.join(out_dir, "summary.json")
        with open(summary_path, 'w', encoding='utf-8') as f:
            json.dump(blocks, f, indent=2)

        print(f"Found {len(blocks)} functions/methods to test")
        
        # Generate AI-powered tests
        return unittester.generate_tests(blocks, api_key, out_dir)

    @staticmethod
    def generate_tests(blocks, api_key, output_dir):
        """
        Generate unit tests using Google Gemini AI.
        
        Args:
            blocks: List of function metadata dictionaries
            api_key: Google Cloud API key
            output_dir: Directory to save test files
            
        Returns:
            str: Path to generated test file, or None if failed
        """
        
        if not api_key:
            raise ValueError("API key is required for test generation")
        
        try:
            # Initialize Gemini client
            client = genai.Client(
                vertexai=True,
                api_key=api_key,
            )

            # Comprehensive system instructions for test generation
            si_text1 = """Purpose

            Produce a complete Python unit test file (pytest) for one or more code blocks described by JSON objects with fields like block_id, function_name, class_context, start_line, end_line, signature, and code.
            Input format your model will receive

            A JSON object (or an array of such objects), where each object (block) has:
            block_id: a string like \"calculator.py_7\" that identifies the module and block index
            function_name: the name of the function or method to test
            class_context: the class that contains the function, or null/empty if it is a module-level function
            start_line: the starting line number of the block in the source file
            end_line: the ending line number of the block in the source file
            signature: the function/method signature, e.g., \"def divide(self, a, b):\"
            code: the full code string for the block (may include exception raises, guards, etc.)
            Output format you should produce

            A single Python file containing pytest-based tests for all blocks described, or a separate test file per module if your workflow requires it. The instruction below focuses on a single test file per module, named test_<module>.py.
            Naming and organization rules

            Derive the module name from block_id by taking the portion before the underscore. Example: for \"calculator.py_7\", module_name is \"calculator.py\".
            Name the test file as test_<module_name_without_extension>.py. For example: test_calculator.py.
            If there are multiple blocks referring to the same module, generate all appropriate tests into that single test_<module_name>.py file.
            If there are blocks from different modules, produce separate test files for each module (e.g., test_another_module.py for another_module.py).
            Test generation guidelines per block

            If class_context is provided (i.e., testing a method of a class):
            Import the class from the corresponding module: from <module_name_without_py> import <ClassName>
            Instantiate the class in each test: obj = ClassName()
            Call the target method on the instance: obj.<function_name>(...)
            Use the provided signature to determine argument types and counts, but if the exact values are not provided in the JSON, choose representative, sensible test inputs that exercise normal operation and edge cases.
            Suggested normal case tests: pick common positive numbers (e.g., 10 and 2 for divide) or typical inputs based on the function purpose.
            Suggested edge cases:
            If the function raises a specific exception for certain input (for example, divide by zero), write a test that asserts the exception is raised with the expected message.
            If class_context is not provided (module-level function):
            Import the function from the module: from <module_name_without_py> import <function_name>
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

            Use pytest for tests; do not rely on unittest unless the project requires it.
            Keep tests simple, deterministic, and independent.
            Use clear assertions:
            assert result == expected
            with pytest.raises(ExpectedException) as excinfo: ... assert \"expected message\" in str(excinfo.value)
            Import paths:
            For module imports, use absolute imports based on the module name derived from block_id (e.g., from calculator import Calculator or from calculator import add)
            Do not include system prompts or explanations in the output; only the Python test code.
            Handling multiple blocks and conflicts

            If multiple blocks map to the same module and include different functions/methods, include all corresponding tests in the same test_<module>.py file.
            If a block cannot be tested fully with the information provided (e.g., missing concrete input values), include tests with sensible placeholder inputs and clearly marked TODOs in comments to guide future refinement.
            Example structure (illustrative, not literal output)

            For a block with block_id \"calculator.py_7\" and a class Calculator with a divide(self, a, b) method:
            Module: calculator.py
            Test file: test_calculator.py
            Tests (illustrative, in Python):
            from calculator import Calculator
            import pytest
            def test_Calculator_divide_normal(): calc = Calculator() assert calc.divide(10, 2) == 5
            def test_Calculator_divide_zero_raises(): calc = Calculator() with pytest.raises(ZeroDivisionError) as excinfo: calc.divide(5, 0) assert \"Cannot divide by zero.\" in str(excinfo.value)
            What to output in response

            The system should output only the generated test file content (no explanations or meta-text) when given a valid JSON block or blocks. If you cannot create tests for some blocks due to missing information, you can skip those blocks or insert TODO comments in the test file, but do not fail the entire test file generation.
            Optional enhancements you may implement if desired. do not add "``` python ```" in the start and end of the file.

            Support parameterized tests to cover multiple input scenarios per block.
            Infer simple test inputs from the function signature types when possible (e.g., numeric types for functions with a and b that look like numbers).
            Produce a concise header comment in the test file describing which blocks were used to generate the tests."""

            model = "gemini-2.5-flash"
            contents = [
                types.Content(
                role="user",
                parts=[
                    {
                    "text": json.dumps(blocks, indent=2)
                    }
                ]
                )
            ]

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
                system_instruction=[types.Part.from_text(text=si_text1)],
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
                    test_filename = f"test_{class_name}.py"
                else:
                    # Use module name without extension
                    base_module = os.path.splitext(module_name)[0]
                    test_filename = f"test_{base_module}.py"
            else:
                test_filename = "test_generated.py"
            
            test_path = os.path.join(output_dir, test_filename)

            # Generate tests with streaming output
            with open(test_path, "w", encoding='utf-8') as f:
                print("Generating AI tests: |", end=" ", flush=True)
                for chunk in client.models.generate_content_stream(
                    model = model,
                    contents = contents,
                    config = generate_content_config,
                    ):
                    if chunk.text:
                        f.write(chunk.text)
                        print('#', end="", flush=True)
                print(" done!")
                print(f"AI tests generated successfully: {test_path}")
                return test_path
                
        except Exception as e:
            print(f"Error generating AI tests: {e}")
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
