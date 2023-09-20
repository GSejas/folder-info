import os
import json
from .ast_analyzer import AstAnalyzer


class FileProcessor:
    def __init__(self, config):
        self.lines_to_read = int(config["Main"]["LinesToRead"])
        self.file_types = config["Main"]["FileTypes"].split(",")
        self.ast_analyzer = AstAnalyzer()  # Create an instance of AstAnalyzer
        self.ignored_dirs = ["venv"]  # add any other directories you want to ignore

    def generate_file_list(self, directory: str, output_file="file_list.json"):
        """Generate a list of files based on the directory and config data."""
        file_list = []

        for root, _, files in os.walk(directory):
            if any(ignored_dir in root for ignored_dir in self.ignored_dirs):
                continue
            for file_name in files:
                if file_name.endswith(tuple(self.file_types)):
                    file_list.append(os.path.join(root, file_name))

        with open(output_file, "w") as f:
            json.dump(file_list, f)

        return output_file

    def analyze_from_list(self, file_list_path: str):
        """Analyze and output specific lines from the files in the provided list."""
        with open(file_list_path, "r") as f:
            files = json.load(f)

        results = {}
        for file_path in files:
            ast_analysis, lines = self._process_file(file_path)
            results[file_path] = {"ast_analysis": ast_analysis, "lines": lines}

        return results

    def _process_file(self, file_path: str):
        """Private method to process individual file."""
        ast_analysis = ""
        lines = []

        with open(file_path, "r") as file:
            content = file.readlines()

            if file_path.endswith(".py"):
                source_code = "".join(content)
                ast_analysis = self.ast_analyzer.analyze(
                    source_code
                )  # Use AstAnalyzer for .py files

            for i, line in enumerate(content):
                if i < self.lines_to_read and not line.strip().startswith("#"):
                    lines.append(line.strip())
                elif i >= self.lines_to_read:
                    break

        return ast_analysis, lines
