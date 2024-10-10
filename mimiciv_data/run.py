import os
import subprocess
import re
import argparse
from concurrent.futures import ProcessPoolExecutor
from termcolor import colored
import time

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
    return None  # Return None if no leading number exists

# Function to run a Python file
def run_python_file(file, silent):
    print(colored(f"Running: {file}", "green"))

    if not silent:
        result = subprocess.run(['python3', file], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.stdout:
            print(colored(f"Output of {file}:\n", "yellow") + result.stdout)
        if result.stderr:
            print(colored(f"Error in {file}:\n", "red") + result.stderr)
    else:
        result = subprocess.run(['python3', file], stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, text=True)
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

    # Separate order-sensitive and non-order-sensitive files
    order_sensitive = []
    non_order_sensitive = []

    for file in py_files:
        if extract_leading_number(file) is not None:
            order_sensitive.append(file)
        else:
            non_order_sensitive.append(file)

    # Sort order-sensitive files based on leading number
    order_sensitive_sorted = sorted(order_sensitive, key=extract_leading_number)
    
    print("Running non-order-sensitive files in parallel...")
    with ProcessPoolExecutor() as executor:
        futures = [executor.submit(run_python_file, file, args.silent) for file in non_order_sensitive]
        for future in futures:
            future.result()  # Wait for each parallel task to complete

    # Run order-sensitive files sequentially
    print("Running order-sensitive files sequentially...")
    for file in order_sensitive_sorted:
        run_python_file(file, args.silent)

    # Run non-order-sensitive files in parallel


if __name__ == "__main__":
    start_time = time.time()
    main()
    end_time = time.time()
    exec_time = end_time - start_time
    print(f"Execution time: {exec_time}")