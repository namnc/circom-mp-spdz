import os
import json
import subprocess
import argparse

ml_tests_dir = 'ml_tests'
outputs_dir = 'outputs'
benchmark_file = 'BENCHMARK.md'

# List of directories to exclude
excluded_dirs = ['circomlib', 'circomlib-matrix', 'circuits', 'crypto', 'Keras2Circom']

table_header = "| Circuit | Time (without latency, on one machine) |\n| --- | --- |\n"

def create_table_row(directory, computation_time):
    return f"| {directory} | {computation_time:.6f} |\n"

def run_test(test_name):
    print(f"Running test: {test_name}")
    subprocess.run(['python3', 'main_ml_tests.py', test_name], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def run_all_tests():
    for item in os.listdir(ml_tests_dir):
        if os.path.isdir(os.path.join(ml_tests_dir, item)) and item not in excluded_dirs:
            run_test(item)

def generate_benchmark_table():
    table_content = table_header

    for root, dirs, files in os.walk(outputs_dir):
        for file in files:
            if file == 'benchmark.json':
                file_path = os.path.join(root, file)
                with open(file_path, 'r') as f:
                    data = json.load(f)
                    computation_time = data.get('computation_time', 'N/A')
                    relative_dir = os.path.relpath(root, outputs_dir)
                    table_content += create_table_row(relative_dir, computation_time)

    with open(benchmark_file, 'w') as f:
        f.write(table_content)

    print(f"Benchmark table has been written to {benchmark_file}")

def main():
    parser = argparse.ArgumentParser(description="Run tests and generate benchmark table.")
    parser.add_argument('--tests-run', type=str, choices=['true', 'false'], default='false',
                        help="Set to 'true' to run all tests before generating the benchmark table.")

    args = parser.parse_args()

    if args.tests_run.lower() == 'true':
        print("Running all tests...")
        run_all_tests()

    print("Generating benchmark table...")
    generate_benchmark_table()

if __name__ == "__main__":
    main()