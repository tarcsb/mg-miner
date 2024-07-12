from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="mg-miner",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A tool to mine and summarize project files",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/mg-miner",
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "mg_miner=mg_miner.cli:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
