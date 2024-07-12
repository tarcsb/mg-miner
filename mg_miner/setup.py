from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="mg-miner",
    version="0.1.0",
    author="Jeffrey Plewak",
    author_email="plewak.jeff@gmail.com",
    description="A tool to mine and summarize project files",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tarcsb/mg-miner",
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "mg_miner=mg_miner.cli:main",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        # List your package dependencies here, e.g.,
        # 'requests',
        # 'pandas',
    ],
    extras_require={
        'dev': [
            'check-manifest',
            'flake8',
            'black',
            'unittest',
        ],
    },
)
