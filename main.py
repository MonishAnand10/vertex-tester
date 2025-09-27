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

Author: Dhulipala Siva Tejaswi, Kaushal Girish & Monish Anand
Version: 0.0.1
Date: 2025-01-28
"""

import ast
import os
import json
import sys

# Command line argument validation and extraction
if len(sys.argv) < 3:
    print("Usage: python main.py <file_path> <output_dir>")
    sys.exit(1)

# Get file path and output directory from command line arguments
file_path = sys.argv[1]
out_dir = sys.argv[2]

class unittester:
    """
    Main class for analyzing Python code and extracting function metadata.
    
    This class uses Python's AST (Abstract Syntax Tree) module to parse
    source code and extract detailed information about functions and methods.
    """
    
    @staticmethod
    def mainProcessor():
        """
        Main processing method that analyzes a Python file and extracts function metadata.
        
        Returns:
            list: Array of dictionaries containing function metadata
            
        Raises:
            ValueError: If file has syntax errors
            FileNotFoundError: If input file doesn't exist
        """
        
        with open(file_path, 'r', encoding='utf-8') as file:
            src = file.read()
        try:
            tree = ast.parse(src)
        except SyntaxError as e:
            raise ValueError(f"SyntaxError while parsing")
        
        # Build parent-child relationship map for AST nodes
        # This helps us determine class context for methods
        parent_map = {}
        for parent in ast.walk(tree):
            for child in ast.iter_child_nodes(parent):
                parent_map[child] = parent
        
        # Debug: Print parent map (can be removed in production)
        print(parent_map)
        idx = 0 # Block counter for unique IDs
        blocks = [] # List to store function metadata

        # Walk through all AST nodes to find function definitions
        for node in ast.walk(tree):
            # Check if current node is a function definition (regular or async)
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                name = node.name

                # Determine nearest class context, if any
                # Walk up the parent chain to find containing class
                class_ctx = None
                cur = node
                while cur in parent_map:
                    cur = parent_map[cur]
                    if isinstance(cur, ast.ClassDef):
                        class_ctx = cur.name
                        break

                # Extract exact source code segment for this function
                # This includes decorators and the complete function body
                code_segment = ast.get_source_segment(src, node)
                if code_segment is None:
                    # Fallback: reconstruct from line numbers if get_source_segment fails
                    start = getattr(node, 'lineno', None)
                    end = getattr(node, 'end_lineno', None) or (start or 0)
                    code_segment = "\n".join(src.splitlines()[start-1:end])

                # Extract function signature (def line only)
                signature_line = ""
                for line in code_segment.splitlines():
                    if line.strip().startswith("def "):
                        signature_line = line.strip()
                        break
                # Fallback to first non-empty line if def line not found
                if not signature_line:
                    # Fallback to first non-empty line
                    for line in code_segment.splitlines():
                        if line.strip():
                            signature_line = line.strip()
                            break

                # Get line number information for precise location tracking
                start_line = getattr(node, 'lineno', None)
                end_line = getattr(node, 'end_lineno', None)


                # Build structured metadata object for this function
                block = {
                    "block_id": f"{os.path.basename(file_path)}_{idx}",  # Unique identifier
                    "function_name": name,                               # Function name
                    "class_context": class_ctx,                          # Parent class (if any)
                    "start_line": start_line,                            # Starting line number
                    "end_line": end_line,                                # Ending line number
                    "signature": signature_line,                         # Function signature
                    "code": code_segment                                 # Complete source code
                }
                blocks.append(block)
                idx += 1

        # Save results to JSON file in specified output directory
        summary_path = os.path.join(out_dir, "summary.json")
        with open(summary_path, 'w', encoding='utf-8') as f:
            json.dump(blocks, f, indent=2)

        return blocks   

# Main execution entry point
if __name__ == "__main__":
    # Process the file and get function metadata                        
    obj = unittester.mainProcessor()

    # Output results to console (for VS Code extension to capture)
    print(obj)                    
