import ast


class AstAnalyzer:
    def __init__(self):
        """Initialize the AstAnalyzer."""
        # No specific initialization required for now
        pass

    def analyze(self, source_code: str) -> dict:
        """
        Analyze Python source code.

        Args:
            source_code (str): Python source code as a string.

        Returns:
            dict: Analysis results.
        """
        tree = ast.parse(source_code)

        results = {
            "header": "",
            "functions": [],
            "classes": [],
            "imports": [],
            # More fields can be added as required
        }

        # Capture the first few lines of the top header
        lines = source_code.splitlines()
        results["header"] = "\n".join(lines[:5])

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                func_info = {
                    "name": node.name,
                    "line": node.lineno,
                    "returns": str(node.returns) if node.returns else None,
                    "docstring": ast.get_docstring(node, clean=True),
                }
                results["functions"].append(func_info)

            elif isinstance(node, ast.ClassDef):
                class_info = {
                    "name": node.name,
                    "line": node.lineno,
                    "docstring": ast.get_docstring(node, clean=True),
                }
                results["classes"].append(class_info)

            elif isinstance(node, ast.Import):
                for n in node.names:
                    results["imports"].append({"name": n.name, "alias": n.asname})

            elif isinstance(node, ast.ImportFrom):
                for n in node.names:
                    results["imports"].append(
                        {"name": n.name, "alias": n.asname, "module": node.module}
                    )

        return results
