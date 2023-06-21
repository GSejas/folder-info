# Python Recursive File Reader

## Description

This Python script recursively reads through a specified directory and prints out the content of the files. This script is designed to be lightweight and does not require any external libraries. It can be configured to ignore certain file types and directories.

## Getting Started

### Prerequisites

- Python 3.6 or higher.

### Installation

1. Clone this repository or download the script.
   ```shell
   git clone https://github.com/gsejas/fileinfo.git
   ```
2. Navigate into the project directory.
   ```shell
   pip install fileinfo
   ```

### Usage

You can run the script using the following command:
   ```shell
   fileinfo [directory] [lines_to_read]
   ```
Replace `[directory]` with the directory you want to scan and `[lines_to_read]` with the maximum number of lines to read per file (optional, defaults to 20).

This script will skip files in any directories named `venv` or `logs`, as well as any files ending in `.log` or `.txt`.

## Contributing

Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are greatly appreciated.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

Distributed under the MIT License. See `LICENSE` for more information.

## Contact

Jorge Sequeira - jsequeira03@gmail.com

Project Link: [https://github.com/your_username/PythonFileReader](https://github.com/your_username/PythonFileReader)
