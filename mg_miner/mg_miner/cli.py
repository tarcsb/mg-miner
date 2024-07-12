"""
CLI script for mg-miner to mine and summarize project files.
"""

import os
import fnmatch
import argparse
import json
import logging

# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler('mg_miner.log')
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

def load_config(config_file):
    """
    Load configuration from a JSON file.

    Parameters:
    config_file (str): Path to the configuration file.

    Returns:
    dict: Configuration dictionary.
    """
    try:
        with open(config_file, 'r') as file:
            return json.load(file)
    except Exception as e:
        logger.error(f"Error loading config file: {e}")
        return {}

def is_excluded(file_path, excluded_dirs):
    """
    Check if the file path should be excluded based on the excluded directories.

    Parameters:
    file_path (str): Path to the file.
    excluded_dirs (list): List of directories to exclude.

    Returns:
    bool: True if the file should be excluded, False otherwise.
    """
    return any(part in excluded_dirs for part in file_path.split(os.sep))

def get_project_type(files, project_types):
    """
    Determine the project type based on the files present.

    Parameters:
    files (list): List of files in the project.
    project_types (dict): Dictionary of project types and their associated file patterns.

    Returns:
    list: Sorted list of tuples with project type and confidence score.
    """
    type_count = {project_type: 0 for project_type in project_types}
    for file in files:
        for project_type, patterns in project_types.items():
            if any(fnmatch.fnmatch(file, pattern) for pattern in patterns):
                type_count[project_type] += 1
    total_files = sum(type_count.values())
    if total_files == 0:
        return [("Undetermined", 0)]
    confidence_scores = [(ptype, count / total_files) for ptype, count in type_count.items()]
    return sorted(confidence_scores, key=lambda x: x[1], reverse=True)

def is_text_file(file_path):
    """
    Check if a file is a text file.

    Parameters:
    file_path (str): Path to the file.

    Returns:
    bool: True if the file is a text file, False otherwise.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            f.read()
        return True
    except (UnicodeDecodeError, IOError):
        return False

def collect_files(root_dir, excluded_dirs, excluded_extensions):
    """
    Collect files from the root directory, excluding specified directories and extensions.

    Parameters:
    root_dir (str): Root directory to scan.
    excluded_dirs (list): List of directories to exclude.
    excluded_extensions (list): List of file extensions to exclude.

    Returns:
    tuple: List of collected files and list of remnants.
    """
    files = []
    remnants = []
    for dirpath, dirnames, filenames in os.walk(root_dir):
        dirnames[:] = [d for d in dirnames if not is_excluded(os.path.join(dirpath, d), excluded_dirs)]
        for filename in filenames:
            if not any(filename.endswith(ext) for ext in excluded_extensions):
                file_path = os.path.join(dirpath, filename)
                try:
                    if is_text_file(file_path):
                        files.append(file_path)
                    else:
                        remnants.append(file_path)
                except PermissionError:
                    logger.error(f"Permission denied: {file_path}")
                    remnants.append(file_path)
    return files, remnants

def detect_component(files, indicators):
    """
    Detect components in the project based on the indicators.

    Parameters:
    files (list): List of files in the project.
    indicators (dict): Dictionary of components and their associated file patterns.

    Returns:
    list: List of detected components with confidence scores.
    """
    component_files = {component: 0 for component in indicators}
    for file in files:
        for component, patterns in indicators.items():
            if any(fnmatch.fnmatch(file, pattern) for pattern in patterns):
                component_files[component] += 1
    total_files = sum(component_files.values())
    if total_files == 0:
        return [("Undetermined", 0)]
    confidence_scores = [(comp, count / total_files) for comp, count in component_files.items()]
    return [comp for comp, score in confidence_scores if score > 0.1]

def summarize_optional_dirs(root_dir, optional_dirs):
    """
    Summarize the contents of optional directories.

    Parameters:
    root_dir (str): Root directory to scan.
    optional_dirs (list): List of optional directories to summarize.

    Returns:
    dict: Dictionary of summarized contents.
    """
    summaries = {}
    for optional_dir in optional_dirs:
        optional_path = os.path.join(root_dir, optional_dir)
        if os.path.exists(optional_path):
            summaries[optional_dir] = []
            for dirpath, _, filenames in os.walk(optional_path):
                for filename in filenames:
                    file_path = os.path.join(dirpath, filename)
                    summaries[optional_dir].append(file_path)
    return summaries

def redact_sensitive_info(files):
    """
    Redact sensitive information from files.

    Parameters:
    files (list): List of files to redact.

    Returns:
    list: List of tuples with file path and redacted content.
    """
    redacted_files = []
    for file in files:
        try:
            with open(file, 'r') as f:
                content = f.read()
            redacted_content = content.replace('secret', 'REDACTED').replace('password', 'REDACTED').replace('key', 'REDACTED')
            redacted_files.append((file, redacted_content))
        except PermissionError:
            logger.error(f"Permission denied: {file}")
    return redacted_files

def create_summary(files, project_type, backend, frontend, testing):
    """
    Create a summary of the project.

    Parameters:
    files (list): List of files in the project.
    project_type (list): Detected project type and confidence score.
    backend (list): Detected backend components.
    frontend (list): Detected frontend components.
    testing (list): Detected testing frameworks.

    Returns:
    str: Summary of the project.
    """
    summary = f"Project Type: {project_type[0][0]} ({project_type[0][1]*100:.2f}% confidence)\n"
    summary += f"Number of source files: {len(files)}\n"
    summary += f"Files:\n"
    for file in files:
        summary += f"  {file}\n"
    summary += f"\nBackend components: {', '.join(backend) if backend else 'None'}\n"
    summary += f"Frontend components: {', '.join(frontend) if frontend else 'None'}\n"
    summary += f"Testing frameworks: {', '.join(testing) if testing else 'None'}\n"
    return summary

def concatenate_files(files, output_file):
    """
    Concatenate the content of multiple files into a single output file.

    Parameters:
    files (list): List of files to concatenate.
    output_file (str): Path to the output file.

    Returns:
    None
    """
    with open(output_file, 'w') as out_file:
        for file in files:
            try:
                with open(file, 'r') as in_file:
                    content = in_file.read()
                out_file.write(f"===== Start of {file} =====\n")
                out_file.write(content)
                out_file.write(f"\n===== End of {file} =====\n\n")
            except PermissionError:
                logger.error(f"Permission denied: {file}")

def main():
    """
    Main function to parse arguments and execute the script.
    """
    parser = argparse.ArgumentParser(description='Mine and summarize project files.')
    parser.add_argument('--root_dir', type=str, default='.', help='The root directory to scan (default is current directory)')
    parser.add_argument('--output_dir', type=str, help='The directory to store the output files (default is .mgminer in the root directory)')
    parser.add_argument('--config', type=str, default='mg_miner/config.json', help='Path to the configuration file (default is mg_miner/config.json)')
    parser.add_argument('--exclude_files', type=str, nargs='*', help='Additional files to exclude')
    parser.add_argument('--silent', action='store_true', help='Run in silent mode, suppressing output to console')
    args = parser.parse_args()

    if args.silent:
        logging.getLogger().setLevel(logging.ERROR)

    config = load_config(args.config)
    root_dir = args.root_dir
    output_dir = args.output_dir if args.output_dir else os.path.join(root_dir, '.mgminer')

    excluded_dirs = set(config['excluded_dirs'])
    excluded_extensions = set(config['excluded_extensions'])
    if args.exclude_files:
        excluded_extensions.update(args.exclude_files)

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    files, remnants = collect_files(root_dir, excluded_dirs, excluded_extensions)
    project_type = get_project_type(files, config['project_types'])
    backend = detect_component(files, config['backend_indicators'])
    frontend = detect_component(files, config['frontend_indicators'])
    testing = detect_component(files, config['testing_frameworks'])
    summary = create_summary(files, project_type, backend, frontend, testing)
    
    optional_summaries = summarize_optional_dirs(root_dir, config['optional_dirs'])
    redacted_optional_summaries = {k: redact_sensitive_info(v) for k, v in optional_summaries.items()}
    
    # Writing summaries
    with open(os.path.join(output_dir, 'summary_source.txt'), 'w') as summary_file:
        summary_file.write(summary)
    
    with open(os.path.join(output_dir, 'summary_extras.txt'), 'w') as extras_file:
        for dir, files in redacted_optional_summaries.items():
            extras_file.write(f"{dir}:\n")
            for file, content in files:
                extras_file.write(f"  {file}\n    {content[:100]}...\n")  # Only showing the first 100 characters

    with open(os.path.join(output_dir, 'remnants.txt'), 'w') as remnants_file:
        for file in remnants:
            remnants_file.write(f"{file}\n")
    
    concatenate_files(files, os.path.join(output_dir, 'concatenated_source.txt'))

if __name__ == '__main__':
    main()
