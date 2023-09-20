from folderinfo.src.file_processor import FileProcessor
from folderinfo.src.config_handler import ConfigHandler


# DIRECTORY = r"C:\Users\delir\Documents\coursegen\4"
# OUTPUT_FILES = "coursegen.files"
# LINES_TO_READ = 14
# FILE_TYPES = ".py,.bat,.md,.rst,.ini,.yaml,.html,.js,.json"
# OUTPUT_LOG = "coursegen.output"

# DIRECTORY = r"C:\Users\delir\Documents\repo\knowbytes\knowbytes"
DIRECTORY = r"C:\Users\delir\Documents\repo\knowbytes\knowbytes\app\blueprints"
OUTPUT_FILES = "knowbytes.files"
LINES_TO_READ = 5
FILE_TYPES = ".py,.bat,.md,.rst,.ini,.yaml,.js,.json"
OUTPUT_LOG = "knowbytes.output"


# DIRECTORY = r"C:\Users\delir\Documents\repo\folder-info\folder-info"
# OUTPUT_FILES = "folder-info.files"
# LINES_TO_READ = 1
# FILE_TYPES = ".py,.bat,.md,.rst,.ini,.yaml,.html,.js,.json"
# OUTPUT_LOG = "folderinfo.output"


def configure(config_handler):
    """Configure settings based on provided configurations."""
    if not config_handler.has_section("Main"):
        config_handler.config.add_section("Main")

    config_handler.config.set("Main", "LinesToRead", str(LINES_TO_READ))
    config_handler.config.set("Main", "FileTypes", FILE_TYPES)


import pyperclip


def process_folder():
    """Process a folder and generate analysis."""
    config_handler = ConfigHandler("config.ini")
    configure(config_handler)

    processor = FileProcessor(config_handler.config)
    processor.generate_file_list(DIRECTORY, OUTPUT_FILES)

    analysis = processor.analyze_from_list(OUTPUT_FILES)
    processor.output_analysis(DIRECTORY, OUTPUT_LOG)
    analysis_str = open(OUTPUT_LOG, "r").read()
    prompt = """
I've used single-character keys for the compressed output. The mapping is as follows:
AST_FORMAT    {
    "h": "header",
    "f": "functions",
    "n": "name",
    "l": "line",
    "d": "docstring",
    "c": "classes",
    "i": "imports",
    "a": "arguments",
    "r": "returns",
    ...
}

The afore mentioned code comes from a folder in a project. 
I am showing you the top {LINES_TO_READ} lines of the files, excluding some python comments, in a project. 
some files are actually empty. 
Suggest improvements and help me keep fleshing out the application we're currently working on. 
Be succint and through
        """
    analysis_str = analysis_str + prompt
    with open(OUTPUT_LOG, "a") as f:
        f.write(prompt)
    print(f"Length: {len(analysis_str)}")
    pyperclip.copy(analysis_str)
    print("Done!")


if __name__ == "__main__":
    process_folder()
