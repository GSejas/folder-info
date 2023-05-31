import sys
from .filereader import process_files

def main():
    # Call your function here
    process_files(sys.argv[1])

if __name__ == "__main__":
    main()
