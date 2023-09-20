import os
import json
import logging
from .ast_analyzer import AstAnalyzer
from . import utils

from pathlib import Path


class FileProcessor:
    def __init__(self, config):
        self.config = config
        self._initialize_settings_from_config()

        self.ast_analyzer = AstAnalyzer()
        self.analysis = None
        # Add more settings here as needed

    def _initialize_settings_from_config(self):
        """Extract settings from config and set as instance variables."""
        try:
            self.lines_to_read = int(self.config.get("Main", "LinesToRead"))
            self.file_types = tuple(self.config.get("Main", "FileTypes").split(","))
            self.ignored_dirs = set(self.config.get("Main", "Ignores").split(","))
            self.specified_files = set(
                self.config.get("Main", "SpecifiedFiles").split(",")
            )
            self.ignored_files = set(self.config.get("Main", "IgnoredFiles").split(","))
            self.analyze_function_names = self.config.get(
                "AST", "AnalyzeFunctionNames", fallback=False
            )
            self.analyze_global_variables = self.config.get(
                "AST", "AnalyzeGlobalVariables", fallback=False
            )
            self.analyze_docstring = self.config.get(
                "AST", "AnalyzeDocstring", fallback=False
            )
            self.analyze_header = self.config.get(
                "AST", "AnalyzeHeader", fallback=False
            )
            self.analyze_imports = self.config.get(
                "AST", "AnalyzeImports", fallback=False
            )
            self.analyze_class_names = self.config.get(
                "AST", "AnalyzeClasses", fallback=False
            )
        except Exception as e:
            logging.error(f"Error initializing settings from config: {e}")
            raise

    def set_lines_to_read(self, lines: int):
        """Set the number of lines to read for analysis."""
        self.lines_to_read = lines

    def set_file_types(self, types: list):
        """Set the file types to be considered for analysis."""
        self.file_types = types

    def generate_file_list(self, directory: str, output_file="file_list.json"):
        """
        The `generate_file_list` function takes a directory path as input, generates a list of files in that
        directory (excluding ignored files and directories), and saves the list to a JSON file.

        :param directory: The `directory` parameter is a string that represents the path to the directory
        from which you want to generate the file list
        :type directory: str
        :param output_file: The `output_file` parameter is a string that specifies the name of the file
        where the generated file list will be saved. By default, it is set to "file_list.json", defaults to
        file_list.json (optional)
        :return: the name of the output file that was generated.
        """
        directory_path = Path(directory)
        file_list = []

        for file_path in directory_path.rglob("*"):
            if file_path.is_dir() or file_path.name in self.ignored_files:
                continue
            if any(
                ignored_dir in str(file_path.parts) for ignored_dir in self.ignored_dirs
            ):
                continue
            if (
                file_path.name in self.specified_files
                or file_path.suffix in self.file_types
            ):
                file_list.append(str(file_path))

        with open(output_file, "w") as f:
            json.dump(file_list, f)

        logging.info(f"Generated file list saved to {output_file}.")
        return output_file

    def analyze_from_list(self, file_list_path: str):
        """
        The `analyze_from_list` function analyzes specific lines from files in a provided list and returns
        the results.

        :param file_list_path: The `file_list_path` parameter is a string that represents the path to a file
        containing a list of file paths. This file should be in JSON format
        :type file_list_path: str
        :return: The method `analyze_from_list` returns the `results` dictionary, which contains the
        analysis results for each file in the provided list.
        """
        results = {}
        try:
            with open(file_list_path, "r", encoding="utf-8") as f:
                files = json.load(f)

            for file_path in files:
                file_result = self._process_file(file_path)
                results[file_path] = file_result

            logging.info(f"Analysis complete for {len(files)} files.")
            self.analysis = results
        except Exception as e:
            logging.error(f"Error during analysis: {e}")
        return results

    def output_analysis(self, directory, output_filename):
        """
        The `output_analysis` function writes the analysis results to an output file.

        :param directory: The `directory` parameter is a string that represents the directory where the
        analysis results are located
        :param output_filename: The `output_filename` parameter is a string that represents the name of the
        file where the analysis results will be written
        """
        with open(output_filename, "w", encoding="utf-8") as f:
            f.write(f"Project dir: {directory}\n")
            for key in self.analysis:
                body = self.analysis[key]
                if isinstance(body, dict):
                    if "lines" in body:
                        f.write(f"{key.replace(directory, '')}\n")
                        for line in body.get("lines", []):
                            f.write(line.strip() + "\n")
                    if "ast" in body:
                        f.write(f"AST: \n")
                        f.write(str(body.get("ast")) + "\n")

                else:
                    f.write(f"Unexpected item in analysis: {body}\n")

    def _process_file(self, file_path: str):
        """
        The `_process_file` function reads a file, analyzes its contents using an AST analyzer, and returns
        the result.

        :param file_path: The `file_path` parameter is a string that represents the path to the file that
        needs to be processed. It should be a valid file path on the system
        :type file_path: str
        :return: a dictionary with the following keys and values:
        """
        lines, source_code = self._read_file(
            file_path, os.path.basename(file_path) in self.specified_files
        )
        result = {"lines": lines, "file_path": file_path}
        if file_path.endswith(".py") and not (
            os.path.basename(file_path) in self.specified_files
        ):
            result["ast"] = {}
            self.ast_analyzer.analyze(source_code)
            if self.analyze_function_names:
                result["ast"]["functions"] = self.ast_analyzer.functions
            if self.analyze_global_variables:
                result["ast"]["gs"] = self.ast_analyzer.global_variables
            if self.analyze_imports:
                result["ast"]["imports"] = self.ast_analyzer.imports
            if self.analyze_docstring:
                result["ast"]["docstring"] = self.ast_analyzer.docstring
            if self.analyze_class_names:
                result["ast"]["classes"] = self.ast_analyzer.classes

            result["ast"] = utils.reduce_tokens(result["ast"])

        return result

    def _read_file(self, file_path: str, return_all: bool = False):
        """
        The `_read_file` function reads a file and returns a list of lines up to a specified limit,
        excluding lines that start with a "#" character.

        :param file_path: The `file_path` parameter is a string that represents the path to the file that
        you want to read. It should be the absolute or relative path to the file on your system
        :type file_path: str
        :param return_all: The `return_all` parameter is a boolean flag that determines whether all lines of
        the file should be returned or only up to a specified limit. If `return_all` is set to `True`, all
        lines will be returned. If it is set to `False` (default), only up to, defaults to False
        :type return_all: bool (optional)
        :return: The `_read_file` function returns a tuple containing two elements: `lines` and
        `source_code`. `lines` is a list of strings, which are the lines of code read from the file.
        `source_code` is a string, which is the entire content of the file.
        """
        lines = []
        with open(file_path, "r") as file:
            source_code = file.read()
            for i, line in enumerate(source_code.splitlines()):
                if line.strip().startswith("#"):
                    self.lines_to_read = self.lines_to_read + 1
                    continue
                if return_all or (i < self.lines_to_read):
                    lines.append(line.strip())
                else:
                    break
        return lines, source_code
