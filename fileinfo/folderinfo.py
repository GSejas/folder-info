
from typing import Union
import os
import sys
LINES_TO_READ = 20

# Optional argument specifies max lines per file
lines_to_read = int(sys.argv[2]) if len(sys.argv) > 2 else LINES_TO_READ
import ast

import os
import configparser
import logging
from typing import Union
from pathlib import Path

class ConfigHandler:
    def __init__(self, config_file):
        self.config = configparser.ConfigParser()
        self.config.read(config_file)

    def get(self, section, option):
        try:
            return self.config.get(section, option)
        except configparser.NoSectionError as e:
            logging.error(f"Section not found in configuration: {e}")
        except configparser.NoOptionError as e:
            logging.error(f"Option not found in configuration: {e}")

class FileProcessor:
    def __init__(self, config):
        self.lines_to_read = int(config.get('Main', 'LinesToRead'))
        self.file_types = config.get('Main', 'FileTypes').split(',')


    def analyze_code(self, file_path):
        with open(file_path, 'r') as file:
            source_code = file.read()
            tree = ast.parse(source_code)
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    print(f"Function found: {node.name}")
                elif isinstance(node, ast.ClassDef):
                    print(f"Class found: {node.name}")

    def process_file(self, file_path):
        logging.info(f"Processing File: {Path(file_path).name}")

        if file_path.endswith('.py'):
            self.analyze_code(file_path)
            
        with open(file_path, 'r') as file:
            for i, line in enumerate(file):
                if i < self.lines_to_read:
                    # Ignore comments
                    if not line.strip().startswith("#"):
                        print(line, end="")
                else:
                    break

    def process_files(self, directory):
        for root, _, files in os.walk(directory):
            if "venv" in root:
                continue
            for file_name in files:
                if file_name.endswith(tuple(self.file_types)):
                    self.process_file(os.path.join(root, file_name))

class ProjectSummary:
    def __init__(self, directory, config):
        self.directory = directory
        self.count_lines_extensions = config.get('Main', 'FileTypes').split(',')

    def generate_summary(self):
        extension_counts = {}
        directory_count = 0

        for root, _, files in os.walk(self.directory):
            if "venv" in root:
                continue
            directory_count += 1
            for file_name in files:
                _, ext = os.path.splitext(file_name)

                if ext in self.count_lines_extensions:
                    extension_counts[ext] = extension_counts.get(ext, 0) + 1

        print(f"Directory: {self.directory}")
        print(f"Total directories: {directory_count}")
        print("File counts by type:")
        for ext, count in extension_counts.items():
            print(f"{ext}: {count}")








