from folderinfo.src.file_processor import FileProcessor
from folderinfo.src.config_handler import ConfigHandler

DIRECTORY = r"C:\Users\delir\Documents\repo\folder-info\folder-info"
OUTPUT = "folder-info.json"
LINES_TO_READ = 5
FILE_TYPES = ".py,.bat,.md,.rst,.ini,.yaml,.html,.js,.json"


def configure(config_handler):
    """Configure settings based on provided configurations."""
    if not config_handler.has_section("Main"):
        config_handler.config.add_section("Main")

    config_handler.config.set("Main", "LinesToRead", str(LINES_TO_READ))
    config_handler.config.set("Main", "FileTypes", FILE_TYPES)


def process_folder():
    """Process a folder and generate analysis."""
    config_handler = ConfigHandler("config.ini")
    configure(config_handler)

    processor = FileProcessor(config_handler.config)
    processor.generate_file_list(DIRECTORY, OUTPUT)

    analysis = processor.analyze_from_list(OUTPUT)
    processor.output_analysis("coursegen.log")
    print("Done!")


if __name__ == "__main__":
    process_folder()
