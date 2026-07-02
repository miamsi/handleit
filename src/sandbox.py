import ast
import pandas as pd
import duckdb
from typing import Dict, Any

class SafeExecutionEngine:
    """Validates and executes LLM-generated code safely within Streamlit Cloud."""
    
    # Explicitly allowed functions and nodes
    ALLOWED_NODES = {
        ast.Module, ast.Expr, ast.Assign, ast.Name, ast.Store, ast.Load,
        ast.BinOp, ast.UnaryOp, ast.Num, ast.Str, ast.Constant, ast.Compare,
        ast.Call, ast.Attribute, ast.Subscript, ast.Index, ast.List, ast.Dict,
        ast.keyword, ast.arg, ast.arguments, ast.FunctionDef, ast.Return,
        ast.For, ast.If, ast.AugAssign
    }
    
    BLOCKED_MODULES = {'os', 'sys', 'subprocess', 'requests', 'socket', 'shutil', 'builtins'}

    @classmethod
    def verify_code_safety(cls, code_str: str) -> bool:
        try:
            tree = ast.parse(code_str)
            for node in ast.walk(tree):
                # Rule 1: Check node types
                if type(node) not in cls.ALLOWED_NODES:
                    return False
                
                # Rule 2: Block malicious imports or calls disguised as attributes
                if isinstance(node, ast.Attribute) and node.attr in cls.BLOCKED_MODULES:
                    return False
                
                # Rule 3: Stop calls to dangerous builtins
                if isinstance(node, ast.Name) and node.id in ['eval', 'exec', 'open', 'compile', '__import__']:
                    return False
                    
            return True
        except SyntaxError:
            return False

    @classmethod
    def execute_safely(cls, code_str: str, context: Dict[str, Any]) -> Dict[str, Any]:
        if not cls.verify_code_safety(code_str):
            raise SecurityError("Execution blocked: Code contains unauthorized operations.")
        
        # Create an isolated environment containing only safely passed data/modules
        safe_globals = {
            "pd": pd,
            "duckdb": duckdb,
            "__builtins__": {
                "len": len, "range": range, "list": list, "dict": dict, 
                "int": int, "float": float, "str": str, "sum": sum, "max": max, "min": min
            }
        }
        # Merge working data copies (like DataFrames or DuckDB connections)
        safe_globals.update(context)
        
        exec(code_str, safe_globals)
        return safe_globals
