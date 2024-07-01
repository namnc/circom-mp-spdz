import os
import json

outputs_dir = 'outputs'
benchmark_file = 'BENCHMARK.md'

table_header = "| Circuit | Time |\n| --- | --- |\n"

def create_table_row(directory, computation_time):
    return f"| {directory} | {computation_time:.6f} |\n"

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