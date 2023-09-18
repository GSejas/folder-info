import sys
from folderinfo import *

def main():
    # Instantiate configuration handler and read the configuration
    config = ConfigHandler('config.ini')

    # Instantiate and use file processor
    file_processor = FileProcessor(config)

    # Process files and print top lines
    file_processor.process_files(sys.argv[1])

    # Instantiate and generate project summary
    summary = ProjectSummary(sys.argv[1], config)
    summary.generate_summary()
    

    
if __name__ == "__main__":
    main()
