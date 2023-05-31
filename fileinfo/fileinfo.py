import os
import sys

# Optional argument specifies max lines per file
lines_to_read = int(sys.argv[2]) if len(sys.argv) > 2 else 20

def process_file(file_path):
    print(f"File: {file_path}")
    print()

    with open(file_path, 'r') as file:
        for i, line in enumerate(file):
            if i < lines_to_read:
                # Ignore comments
                if not line.strip().startswith("#"):
                    print(line, end="")
            else:
                break
from types import Union
import os






def process_files(directory):
    print(f"Directory: {directory}")
    file_paths  = []
    # Process files
    for root, dirs, files in os.walk(directory):
        # Skip processing files in venv
        if "venv" in root:
            continue

        project_summary(sys.argv[1])

        for file_name in files:
            if file_name.endswith(('.py','.bat', '.md', '.rst', '.ini', '.yaml', '.json')):
                file_paths.append((os.path.join(root, file_name), file_name))
    for (fullepath, namepath) in file_paths:            
        process_file(fullepath)

# Add initial prompt request to the output text
print("Suggest a readme for the following code.A good README file should be clear, concise, and well-A good README file should be clear, concise, and well-organized. It should include a descriptive title and overview of the project, installation instructions, usage guidelines, and API documentation if applicable. Configuration details, examples, and use cases should be provided to help users understand and apply the project effectively. Contributing guidelines, testing instructions, and troubleshooting tips are essential for fostering collaboration and addressing common issues. Including the project's license, acknowledgments, references, and contact information adds value to the README. ")
# Call the function to process files recursively
process_files(sys.argv[1])
