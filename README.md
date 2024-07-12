# mg-miner

`mg-miner` is a command-line tool designed to mine and summarize project files, providing an overview of the project's structure, types of files, backend and frontend components, and testing frameworks used.
Its the extractor portion of ma much larger purpose of assessing maturity, compliance, maintenance and portability for cloud migrations. My goal is to play well with ETL.

## Wanted Features
  
- **UI**
- **Pre-flight**
- **Testing**
- **Dynamic/Batch Processing**
- **Integrate Snowflake**
- **Integrate Apache**
- **Analytics**
- **Tools**: Prometheus, Grafana
- **Docker**
- **Kubernetes**
- **SRE**
- **Security**
- **Templating**: Jinja or similar


## Features

- **File Collection**: Collects files from a specified root directory, excluding specified directories and file extensions.
- **Project Type Detection**: Determines the project type based on the files present.
- **Component Detection**: Identifies backend and frontend components and testing frameworks.
- **Summary Creation**: Generates a summary of the project, including the number of files and detected components.
- **File Concatenation**: Concatenates the content of multiple files into a single output file.
- **Sensitive Information Redaction**: Redacts sensitive information from files.
- **Silent Mode**: Runs in silent mode, suppressing output to the console.

## Installation

Install the package via pip:

pip install mg-miner

## Usage

To use `mg-miner`, run the following command:

mg_miner --root_dir /path/to/root/dir --output_dir /path/to/output/dir --exclude_files "*.tmp" "*.log" --silent

### Command-Line Arguments

- `--root_dir`: The root directory to scan (default is the current directory).
- `--output_dir`: The directory to store the output files (default is `.mgminer` in the root directory).
- `--config`: Path to the configuration file (default is `mg_miner/config.json`).
- `--exclude_files`: Additional files to exclude (e.g., `"*.tmp" "*.log"`).
- `--silent`: Run in silent mode, suppressing output to the console.

### Example

To scan a project directory and output the results to a specific directory while excluding temporary and log files:

mg_miner --root_dir my_project --output_dir my_output --exclude_files "*.tmp" "*.log" --silent

## Configuration

The configuration file (`config.json`) specifies directories and file extensions to exclude, project types, component indicators, and optional directories. Here is an example configuration:

{
  "excluded_dirs": [".git", "__pycache__", "node_modules", "venv", ".env", ".mypy_cache"],
  "excluded_extensions": ["zip", "tar", "gz", "rar", "7z", "db", "sqlite", "bak", "log", "package-lock.json"],
  "project_types": {
    "Python": ["*.py"],
    "JavaScript": ["*.js", "*.jsx", "*.ts", "*.tsx"],
    "Java": ["*.java"],
    "C++": ["*.cpp", "*.h"],
    "C": ["*.c", "*.h"],
    "HTML": ["*.html", "*.css", "*.js"],
    "YAML": ["*.yaml", "*.yml"],
    "JSON": ["*.json"],
    "INI": ["*.ini"],
    "Markdown": ["README.md", "*.md"],
    "Embedded": ["*.c", "*.cpp", "*.h", "*.ino", "*.asm", "*.S"],
    "Cloud": ["*.yaml", "*.yml", "*.json", "*.tf", "Dockerfile", "docker-compose.yml"],
    "Ruby": ["*.rb"],
    "PHP": ["*.php"],
    "Go": ["*.go"],
    "Swift": ["*.swift"],
    "Kotlin": ["*.kt"],
    "R": ["*.r"],
    "Perl": ["*.pl"],
    "Scala": ["*.scala"],
    "Haskell": ["*.hs"],
    "Rust": ["*.rs"]
  },
  "backend_indicators": {
    "Python": ["*.py", "requirements.txt", "Pipfile", "pyproject.toml"],
    "Django": ["manage.py", "django.*"],
    "Flask": ["app.py", "flask.*"],
    "FastAPI": ["main.py", "fastapi.*"],
    "Java": ["*.java", "pom.xml", "build.gradle"],
    "Spring": ["application.properties", "application.yml", "spring.*"],
    "Node.js": ["*.js", "*.ts", "package.json", "yarn.lock"],
    "Express": ["app.js", "express.*"],
    "Ruby": ["*.rb", "Gemfile"],
    "Rails": ["config.ru", "rails.*"],
    "PHP": ["*.php", "composer.json"],
    "Laravel": ["artisan", "laravel.*"],
    "Go": ["*.go", "go.mod", "go.sum"],
    "Gin": ["gin.*"],
    "Fiber": ["fiber.*"],
    "Swift": ["*.swift", "Package.swift"],
    "Kotlin": ["*.kt", "build.gradle.kts"],
    "Scala": ["*.scala", "build.sbt"],
    "Haskell": ["*.hs", "stack.yaml"],
    "Rust": ["*.rs", "Cargo.toml"],
    "ASP.NET": ["*.csproj", "*.vbproj"],
    "GCP": ["*.yaml", "*.yml", "*.json", "Dockerfile", "docker-compose.yml", "*.tf"],
    "AWS": ["*.yaml", "*.yml", "*.json", "Dockerfile", "docker-compose.yml", "*.tf", "cloudformation.json", "cloudformation.yaml"],
    "Azure": ["*.yaml", "*.yml", "*.json", "Dockerfile", "docker-compose.yml", "*.tf", "azure-pipelines.yml", "azure-pipelines.yaml"]
  },
  "frontend_indicators": {
    "HTML": ["*.html", "*.css", "*.js"],
    "React": ["*.jsx", "*.tsx", "package.json", "yarn.lock"],
    "Vue": ["*.vue", "package.json", "yarn.lock"],
    "Angular": ["*.ts", "*.html", "angular.json"],
    "Svelte": ["*.svelte", "package.json", "yarn.lock"],
    "Ember": ["ember-cli-build.js", "package.json", "yarn.lock"]
  },
  "testing_frameworks": {
    "Python": ["pytest.ini", "conftest.py", "tox.ini"],
    "JavaScript": ["jest.config.js", "karma.conf.js", "mocha.opts"],
    "Java": ["*.java", "testng.xml", "junit-platform.properties"],
    "Ruby": ["*.rb", "spec_helper.rb", "Rakefile"],
    "PHP": ["*.php", "phpunit.xml"],
    "Go": ["*_test.go"],
    "Swift": ["*.swift", "XCTestManifest.swift"],
    "Kotlin": ["*.kt", "build.gradle.kts"],
    "Scala": ["*.scala", "build.sbt"],
    "Haskell": ["*.hs", "test/Spec.hs"],
    "Rust": ["*.rs", "Cargo.toml"],
    "C++": ["*.cpp", "CMakeLists.txt", "*.h"],
    "C": ["*.c", "CMakeLists.txt", "*.h"]
  },
  "optional_dirs": [".vscode", ".github", ".eclipse", "coverage", ".config", ".aws"]
}

## Development

To set up the development environment, follow these steps:

1. Clone the repository:

git clone https://github.com/tarcsb/mg-miner.git
cd mg-miner

2. Create a virtual environment and activate it:

python -m venv venv
source venv/bin/activate  # On Windows, use `venv\\Scripts\\activate`

3. Install the dependencies:

pip install -r requirements.txt

4. Run the tests:

python -m unittest discover tests

## Contributing

Contributions are welcome! Please read the [CONTRIBUTING.md](CONTRIBUTING.md) file for guidelines on how to contribute to this project.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.


Contact name: Jeffrey Plewak
Contact email: plewak.jeff@gmail.com
