import ast


class AstAnalyzer:
    def __init__(self):
        pass

    def analyze(self, source_code: str):
        """Analyze Python source code."""
        tree = ast.parse(source_code)
        contentlines = []

        # Capture the first few lines of the top header
        lines = source_code.splitlines()
        header_lines = "\n".join(lines[:5])
        contentlines.append(header_lines)

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                contentlines.append(f"Function: {node.name}")
            elif isinstance(node, ast.ClassDef):
                contentlines.append(f"Class: {node.name}")
            if hasattr(node, "returns") and node.returns:
                contentlines.append(f"rets: {node.returns}")
            if hasattr(node, "__doc__") and node.__doc__:
                contentlines.append(f"__doc__: {node.__doc__}")
        return "\n".join(contentlines)
