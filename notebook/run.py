import os
import subprocess
import re
import argparse
from concurrent.futures import ThreadPoolExecutor
from termcolor import colored

# Function to find all Python files in directories ending with *_runs
def find_python_files(root_dir):
    py_files = []
    for dirpath, dirnames, filenames in os.walk(root_dir):
        if dirpath.endswith('_runs'):
            for file in filenames:
                if file.endswith('.py') and not file.startswith("_"):
                    full_path = os.path.join(dirpath, file)
                    py_files.append(full_path)
    return py_files

# Function to extract a leading number if it exists for sorting
def extract_leading_number(filename):
    match = re.match(r'(\d+)_', os.path.basename(filename))
    if match:
        return int(match.group(1))
    return float('inf')  # Return a high value if no number

# Function to run a Python file
def run_python_file(file, silent):
    # Print the file being executed in color
    print(colored(f"Running: {file}", "green"))

    if not silent:
        # Capture output and log it
        result = subprocess.run(['python3', file], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        # Log stdout and stderr if needed
        if result.stdout:
            print(colored(f"Output of {file}:\n", "yellow") + result.stdout)
        if result.stderr:
            print(colored(f"Error in {file}:\n", "red") + result.stderr)
    else:
        # Suppress the output
        subprocess.run(['python3', file], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if result.stderr:
            print(colored(f"Error in {file}:\n", "red") + result.stderr)

# Main function
def main():
    # Argument parsing for --silent flag
    parser = argparse.ArgumentParser(description="Run all Python files in directories ending with *_runs")
    parser.add_argument('--silent', action='store_true', help="Enable logging of stdout and stderr of each subprocess")
    args = parser.parse_args()

    root_dir = '.'  # Starting directory
    py_files = find_python_files(root_dir)

    # Sort files based on the leading number (if exists)
    py_files_sorted = sorted(py_files, key=extract_leading_number)

    # Run Python files in parallel, with the smaller number files running first
    with ThreadPoolExecutor() as executor:
        executor.map(lambda file: run_python_file(file, args.silent), py_files_sorted)

if __name__ == "__main__":
    main()
