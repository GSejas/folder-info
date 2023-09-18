from setuptools import setup, find_packages
import pathlib

# Get the long description from the README file
here = pathlib.Path(__file__).parent.resolve()
long_description = (here / "README.md").read_text(encoding="utf-8")

setup(
    name="folderinfo",
    version="0.1",
    description="A tool to get information about folders and their content.",  # New description
    long_description=long_description,  # New long description from README
    long_description_content_type="text/markdown",  # Type of the long description
    url="https://github.com/yourusername/folderinfo",  # Replace with your project URL
    author="Your Name",  # Replace with your name
    author_email="you@example.com",  # Replace with your email
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
    ],
    packages=find_packages(),
    python_requires=">=3.6",
    install_requires=[
        # Add your project dependencies here. For example:
        "click",
        "rich",
    ],
    entry_points={
        "console_scripts": [
            "folderinfo = folderinfo.src:cli",
        ],
    },
)
