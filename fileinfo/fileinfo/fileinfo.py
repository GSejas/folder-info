import os
import sys
from typing import Union

# Optional argument specifies max lines per file
lines_to_read = int(sys.argv[2]) if len(sys.argv) > 2 else 20

def process_file(file_path):
    dir_path = Path(file_path)
    print(f"File: {dir_path.name}")
    print()
    
    with open(file_path, 'r') as file:
        for i, line in enumerate(file):
            if i < lines_to_read:
                # Ignore comments
                if not line.strip().startswith("#"):
                    print(line, end="")
            else:
                break

def project_summary(directory: str, count_lines_extensions: Union[None, list]=None, exclude_extensions: Union[None, list]=None):
    extension_counts = {}
    line_counts = {}
    directory_count = 0

    if count_lines_extensions is not None:
        assert isinstance(count_lines_extensions, list)

    if exclude_extensions is not None:
        assert isinstance(exclude_extensions, list)

    for root, dirs, files in os.walk(directory):
        # Skip processing files in directories named exactly "venv"
        if "venv" in root:
            continue
        print(dirs)
        directory_count += len(dirs)
        for file_name in files:
            x, ext = (file_name.split("."))[:-1], (file_name.split("."))[-1]
            
            ext = "."+ext            
            if ext in count_lines_extensions:

                if ext in extension_counts:
                    extension_counts[ext] += 1
                else:
                    extension_counts[ext] = 1
                    
                # try:
                #     with open(os.path.join(root, file_name), 'r', encoding='utf-8') as f:
                #         lines = len(f.readlines())
                #     if ext in line_counts:
                #         line_counts[ext] += lines
                #     else:
                #         line_counts[ext] = lines
                # except UnicodeDecodeError:
                #     print(f"Unable to read {file_name} due to UnicodeDecodeError.")
                # except Exception as e:
                #     print(f"Unable to read {file_name}. Error: {str(e)}")
    print(f"Directory: {directory}")
    print(f"Total directories: {directory_count}")
    print("File counts by type:")
    for ext, count in extension_counts.items():
        print(f"{ext}: {count}")
    # print("Line counts by file type:")
    # for ext, count in line_counts.items():
    #     print(f"{ext}: {count}")

from pathlib import Path

def process_files(directory):
    dir_path = Path(directory)
    print(f"Directory parent: {dir_path}")
    file_paths = []
    # project_summary(directory, count_lines_extensions=['.py','.bat', '.md', '.rst', '.ini', '.yaml', '.json'])
    for root, dirs, files in os.walk(directory):
        # Skip processing files in directories named exactly "venv"
        if "venv" in root:
            continue
        for file_name in files:
            if file_name.endswith(('.py','.bat', '.md', '.rst', '.ini', '.yaml', '.json')):
                file_paths.append((os.path.join(root, file_name), file_name))
    for (fullepath, namepath) in file_paths:            

        process_file(fullepath)





if __name__ == "__main__":
    # Call the function to process files recursively
    process_files(sys.argv[1])
