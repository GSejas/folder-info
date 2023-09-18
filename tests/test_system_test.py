import os
import json
from folderinfo.src.file_processor import FileProcessor
from folderinfo.src.config_handler import ConfigHandler

# Test configuration
TEST_DIR = os.path.dirname(os.path.abspath(__file__))
SAMPLE_DIRECTORY = os.path.join(TEST_DIR, "sample_data")
OUTPUT_FILE = "output.json"

# Sample data directory should contain some test files.
# For this example, at least one Python file is assumed for AST testing.
CONFIG_PATH = os.path.join(SAMPLE_DIRECTORY, "config.ini")


def setup_module():
    """Set up before all tests."""
    # Here we can add setup code which should run before any test
    pass


def teardown_module():
    """Tear down after all tests."""
    if os.path.exists(OUTPUT_FILE):
        os.remove(OUTPUT_FILE)


def test_generate_file_list():
    """Test the file generation functionality."""
    # Sample data
    config = ConfigHandler(CONFIG_PATH)
    processor = FileProcessor(config)

    processor.generate_file_list(SAMPLE_DIRECTORY, OUTPUT_FILE)

    assert os.path.exists(OUTPUT_FILE), "Output file was not generated."

    with open(OUTPUT_FILE, "r") as f:
        data = json.load(f)
        assert isinstance(data, list), "Output file should contain a list."
        assert len(data) > 0, "List of files should not be empty."


def test_analyze_files():
    """Test the file analysis functionality."""
    # Assuming that you have a function analyze_files in FileProcessor.
    config = ConfigHandler(CONFIG_PATH)
    processor = FileProcessor(config)

    processor.generate_file_list(
        SAMPLE_DIRECTORY, OUTPUT_FILE
    )  # First generate the file list
    results = processor.analyze_from_list(OUTPUT_FILE)  # Then analyze

    # Some basic checks
    assert isinstance(results, dict), "Analysis should return a dictionary."

    # Let's check Python files for sample AST results (classes and functions)
    py_files = [file for file in results if file.endswith(".py")]
    for file in py_files:
        file_results = results[file]
        print(file_results)
