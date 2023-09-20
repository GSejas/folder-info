import os


class ProjectSummary:
    def __init__(self, directory: str, config):
        self.directory = directory
        self.count_lines_extensions = config.get("Main", "FileTypes").split(",")

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
