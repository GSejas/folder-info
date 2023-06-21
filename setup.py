from setuptools import setup, find_packages

setup(
    name='folderinfo',
    version='0.1',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'folderinfo = folderinfo.main:main',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3.6',
        'License :: OSI Approved :: MIT License',
    ],
    python_requires='>=3.6',
)
