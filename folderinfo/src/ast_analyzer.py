import ast
from typing import List, Dict, Union, Optional


class AstAnalyzer:
    AVAILABLE_METHODS = [
        "get_function_names",
        "get_global_variables",
        "get_import",
        "get_import_from",
        "get_module_docstring",
    ]

    def __init__(self):
        """Initialize the AstAnalyzer."""
        self.tree = None
        self.header = None
        self.docstring = None
        self.functions = None
        self.classes = None
        self.global_variables = None
        self.imports = None

    def _parse_code(self, source_code: str):
        self.tree = ast.parse(source_code)

    def get_class_names(self) -> List[Dict[str, Union[str, int, Optional[str]]]]:
        results = []
        for node in ast.walk(self.tree):
            if isinstance(node, ast.ClassDef):
                methods = [n.name for n in node.body if isinstance(n, ast.FunctionDef)]
                class_info = {
                    "name": node.name,
                    "line": node.lineno,
                    "docstring": (ast.get_docstring(node, clean=True) or "").split(
                        "\n"
                    )[0]
                    if ast.get_docstring(node, clean=True)
                    else None,
                    "methods": methods,
                }
                results.append(class_info)
        return results

    def get_function_calls(self, node: ast.FunctionDef) -> List[str]:
        calls = [
            n.func.id
            for n in ast.walk(node)
            if isinstance(n, ast.Call) and isinstance(n.func, ast.Name)
        ]
        return calls

    def get_function_names(self) -> List[Dict[str, Union[str, int, Optional[str]]]]:
        results = []
        for node in ast.walk(self.tree):
            if isinstance(node, ast.FunctionDef):
                args = [arg.arg for arg in node.args.args]
                calls = self.get_function_calls(node)
                func_info = {
                    "name": node.name,
                    "line": node.lineno,
                    "returns": str(node.returns) if node.returns else None,
                    "docstring": (ast.get_docstring(node, clean=True) or "").split(
                        "\n"
                    )[0]
                    if ast.get_docstring(node, clean=True)
                    else None,
                    "arguments": args,
                    "calls": calls,
                }
                results.append(func_info)
        return results

    def _get_target_name(self, target: ast.AST) -> Optional[str]:
        if isinstance(target, ast.Name):
            return target.id
        elif isinstance(target, ast.Attribute):
            # This will give a name like 'obj.x' for an assignment 'obj.x = 5'
            return f"{self._get_target_name(target.value)}.{target.attr}"
        # For simplicity, ignoring other potential types like ast.Subscript
        return None

    def get_global_variables(self) -> List[Dict[str, str]]:
        results = []
        for node in ast.walk(self.tree):
            if isinstance(node, ast.Global):
                results.append({"name": node.names[0]})
            elif isinstance(node, ast.Assign):
                target_name = self._get_target_name(node.targets[0])
                if target_name:  # Ignore cases where name is None (like list[0] = 5)
                    results.append({"name": target_name})
        return results

    def get_import(self) -> list:
        results = []
        for node in ast.walk(self.tree):
            if isinstance(node, ast.Import):
                for n in node.names:
                    results.append({"name": n.name, "alias": n.asname})
        return results

    def get_import_from(self) -> list:
        results = []
        for node in ast.walk(self.tree):
            if isinstance(node, ast.ImportFrom):
                for n in node.names:
                    results.append(
                        {"name": n.name, "alias": n.asname, "module": node.module}
                    )
        return results

    def get_module_docstring(self, source_code) -> str:
        tree = ast.parse(source_code)
        return ast.get_docstring(tree, clean=True)

    def analyze(
        self, source_code: str
    ) -> Dict[str, Union[str, List[Dict[str, Union[str, int, Optional[str]]]]]]:
        """
        Analyze Python source code.

        Args:
            source_code (str): Python source code as a string.

        Returns:
            dict: Analysis results.
        """
        self._parse_code(source_code)
        self.results = {
            "header": "",
            "docstring": self.get_module_docstring(source_code),
            "functions": self.get_function_names(),
            "classes": self.get_class_names(),
            "global_variables": self.get_global_variables(),
            "imports": self.get_import() + self.get_import_from(),
        }

        self.header = ""
        self.docstring = self.get_module_docstring(source_code)
        self.functions = self.get_function_names()
        self.classes = self.get_class_names()
        self.global_variables = self.get_global_variables()
        self.imports = self.get_import() + self.get_import_from()

        return self.results
