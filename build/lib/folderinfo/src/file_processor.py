import os
import json
import logging
from .ast_analyzer import AstAnalyzer


class FileProcessor:
    def __init__(self, config):
        self.config = config
        self.lines_to_read = int(config.get("Main", "LinesToRead"))
        self.file_types = config.get("Main", "FileTypes").split(",")
        self.ast_analyzer = AstAnalyzer()
        self.ignored_dirs = ["venv"]

    def set_lines_to_read(self, lines: int):
        """Set the number of lines to read for analysis."""
        self.lines_to_read = lines

    def set_file_types(self, types: list):
        """Set the file types to be considered for analysis."""
        self.file_types = types

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

        logging.info(f"Generated file list saved to {output_file}.")
        return output_file

    def analyze_from_list(self, file_list_path: str):
        """Analyze and output specific lines from the files in the provided list."""
        results = {}

        with open(file_list_path, "r", encoding="utf-8") as f:
            files = json.load(f)

        for file_path in files:
            file_result = self._process_file(file_path)
            results[file_path] = file_result

        logging.info(f"Analysis complete for {len(files)} files.")
        return results

    def _process_file(self, file_path: str):
        """Private method to process individual file."""
        result = {}
        lines = []

        if file_path.endswith(".py"):
            with open(file_path, "r") as file:
                source_code = file.read()
                ast_analysis = self.ast_analyzer.analyze(source_code)
                result["ast_analysis"] = ast_analysis

        with open(file_path, "r") as file:
            for i, line in enumerate(file):
                if i < self.lines_to_read:
                    if not line.strip().startswith("#"):
                        lines.append(line.strip())
                else:
                    break
        result["lines"] = lines
        result["file_path"] = file_path

        return result
