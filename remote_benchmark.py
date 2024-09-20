import argparse
import os
import paramiko
import subprocess
import time
import re

EXCLUDED_CIRCUITS = ["circomlib", "circomlib-matrix", "circuits", "crypto", "Keras2Circom", ".DS_Store", "util.py", "__init__.py", "__pycache__"]
SSH_PORT = 22
BENCHMARK_FILE = "BENCHMARK.md"

def read_benchmark_table():
    benchmarks = {}
    with open(BENCHMARK_FILE, "r") as f:
        lines = f.readlines()
        for line in lines[2:]:  # Skip header
            parts = line.strip().split("|")
            if len(parts) >= 3:
                circuit = parts[1].strip()
                benchmarks[circuit] = {
                    "Time": parts[2].strip(),
                    "One region": "",
                    "Different regions": ""
                }
    return benchmarks

def write_benchmark_table(benchmarks):
    with open(BENCHMARK_FILE, "w") as f:
        f.write("| Circuit | Fast LAN (rate 10gb, latency 0.25ms) | LAN (rate 1gb, latency 1ms) | WAN (rate 100mb, latency 50ms) |\n")
        f.write("| --- | --- | --- | --- |\n")
        for circuit, times in benchmarks.items():
            f.write(f"| {circuit} | {times['fastlan']} | {times['lan']} | {times['wan']} |\n")
        f.write(f"\n")

def write_data_info_to_benchmark_file(benchmarks):
    with open(BENCHMARK_FILE, "a") as f:
        f.write("\n| Circuit | Data sent (MB) | Rounds | Global data sent (MB) |\n")
        f.write("| --- | --- | --- | --- |\n")
        
        for circuit_name, data in benchmarks.items():
            f.write(f"| {circuit_name} | {data['Data sent']} | {data['Rounds']} | {data['Global data sent']} |\n")

def extract_time_from_output(output):
    for line in output.splitlines():
        if line.startswith("Time ="):
            return float(line.split("=")[1].split()[0])
    return None

def extract_data_info_from_output(output):
    data_info = {
        "Data sent": None,
        "Rounds": None,
        "Global data sent": None
    }

    data_sent_re = re.compile(r"Data sent = ([\d.]+) MB")
    rounds_re = re.compile(r"in ~(\d+) rounds")
    global_data_sent_re = re.compile(r"Global data sent = ([\d.]+) MB")

    for line in output.splitlines():
        if "Data sent" in line:
            data_info["Data sent"] = data_sent_re.search(line).group(1)
            data_info["Rounds"] = rounds_re.search(line).group(1)
        if "Global data sent" in line:
            data_info["Global data sent"] = global_data_sent_re.search(line).group(1)

    return data_info

def connect_ssh(hostname, port, username="root", password="password"):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname, port=port, username=username, password=password)
    return ssh

def run_remote_command_verbose(ssh, command):
    stdin, stdout, stderr = ssh.exec_command(command)
    stdout.channel.recv_exit_status()  # Wait for the command to finish
    output = stdout.read().decode()
    error = stderr.read().decode()
    return output, error

def run_remote_command(ssh, command):
    stdin, stdout, stderr = ssh.exec_command(command)
    stdout.channel.recv_exit_status()
    return stdout.read().decode(), stderr.read().decode()

def create_hosts_file(local_ip="0.0.0.0", party_ip="127.0.0.1", local_port=3001, party_port=3000):
    hosts_content = f"{local_ip}:{local_port}\n{party_ip}:{party_port}\n"
    with open("hosts", "w") as hosts_file:
        hosts_file.write(hosts_content)

def main():
    parser = argparse.ArgumentParser(description="Remote MP-SPDZ Benchmark Script")
    parser.add_argument("--party1", required=True, help="IP address and port of party1, e.g., 127.0.0.1:3000")
    parser.add_argument("--circuit", help="Specific circuit to run. If not provided, all circuits are used.")
    args = parser.parse_args()

    party1_ip, party1_port = args.party1.split(":")
    circuit = args.circuit

    if circuit:
        circuits_to_compile = [circuit]
    else:
        circuits_to_compile = [d for d in os.listdir("ml_tests") if d not in EXCLUDED_CIRCUITS]

    print(f"Connecting to party1 at {party1_ip}:{22} via SSH...")
    ssh = connect_ssh(party1_ip, SSH_PORT)
    local_ip = run_remote_command(ssh, "ping -c 1 host.docker.internal | head -1 | awk -F'[()]' '{print $2}'")[0][:-1]

    os.chdir("../MP-SPDZ")
    create_hosts_file()
    run_remote_command(ssh, f'cd ../testing/MP-SPDZ && echo "{local_ip}:3001\n0.0.0.0:{party1_port}" > hosts')

    print()

    # os.chdir("../circom-mp-spdz")
    # benchmarks = read_benchmark_table()
    benchmarks = {}

    for circuit_name in circuits_to_compile:
        benchmarks[circuit_name] = {}

        os.chdir("../circom-mp-spdz")
        print(f"1. Compiling circuit {circuit_name} to .mpc locally...")
        subprocess.run(["python3", "main_ml_tests.py", circuit_name], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f"2. Compiling {circuit_name} to bytecode for MP-SPDZ...")
        os.chdir("../MP-SPDZ")
        subprocess.run(["./compile.py", "circuit"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        print(f"3. Compiling circuit {circuit_name} to .mpc remotely on party1...")
        run_remote_command(ssh, f"cd ../testing/circom-mp-spdz && python3 main_ml_tests.py {circuit_name}")

        print(f"4. Copying {circuit_name}.mpc from local to party1...")
        subprocess.run(["sshpass", "-p", "password", "scp", f"Programs/Source/circuit.mpc", f"root@{party1_ip}:/testing/MP-SPDZ/Programs/Source/"])
        run_remote_command(ssh, f"cd ../testing/MP-SPDZ && ./compile.py circuit")

        print(f"5. Copying Inputs from local to party1...")
        subprocess.run(["sshpass", "-p", "password", "scp", f"Player-Data/Input-P0-0", f"root@{party1_ip}:/testing/MP-SPDZ/Player-Data"])
        subprocess.run(["sshpass", "-p", "password", "scp", f"Player-Data/Input-P1-0", f"root@{party1_ip}:/testing/MP-SPDZ/Player-Data"])

        print("6. Setting up Fast LAN")
        run_remote_command(ssh, f"tc qdisc del dev eth0 root")
        run_remote_command(ssh, f"tc qdisc add dev eth0 root handle 1:0 netem delay 0.25ms")
        run_remote_command(ssh, f"tc qdisc add dev eth0 parent 1:1 handle 10:0 tbf rate 10gbit")

        print(f"7. Running MP-SPDZ with circuit {circuit_name}...")
        spdz_local = subprocess.Popen(["./semi-party.x", "-N", "2", "-p", "0", "-OF", ".", "circuit", "-ip", "hosts"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        time.sleep(1) # to be sure that the process was started
        run_remote_command(ssh, f"cd ../testing/MP-SPDZ && ./semi-party.x -N 2 -p 1 -OF . circuit -ip hosts")
        spdz_local.wait()

        spdz_local.stdout.read()
        output = spdz_local.stderr.read()
        time_fastlan = extract_time_from_output(output)
        if time_fastlan is not None:
            benchmarks[circuit_name]["fastlan"] = f"{time_fastlan:.6f}"

        data_info = extract_data_info_from_output(output)
        benchmarks[circuit_name]["Data sent"] = data_info["Data sent"]
        benchmarks[circuit_name]["Rounds"] = data_info["Rounds"]
        benchmarks[circuit_name]["Global data sent"] = data_info["Global data sent"]
        
        print("8. Setting up LAN")
        run_remote_command(ssh, f"tc qdisc del dev eth0 root")
        run_remote_command(ssh, f"tc qdisc add dev eth0 root handle 1:0 netem delay 1ms")
        run_remote_command(ssh, f"tc qdisc add dev eth0 parent 1:1 handle 10:0 tbf rate 1gbit")

        print(f"9. Running MP-SPDZ with circuit {circuit_name}...")
        spdz_local = subprocess.Popen(["./semi-party.x", "-N", "2", "-p", "0", "-OF", ".", "circuit", "-ip", "hosts"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        time.sleep(1) # to be sure that the process was started
        run_remote_command(ssh, f"cd ../testing/MP-SPDZ && ./semi-party.x -N 2 -p 1 -OF . circuit -ip hosts")
        spdz_local.wait()

        spdz_local.stdout.read()
        output = spdz_local.stderr.read()
        time_lan = extract_time_from_output(output)
        if time_lan is not None:
            benchmarks[circuit_name]["lan"] = f"{time_lan:.6f}"

        
        print("10. Setting up WAN")
        run_remote_command(ssh, f"tc qdisc del dev eth0 root")
        run_remote_command(ssh, f"tc qdisc add dev eth0 root handle 1:0 netem delay 50ms")
        run_remote_command(ssh, f"tc qdisc add dev eth0 parent 1:1 handle 10:0 tbf rate 100mbit")

        print(f"11. Running MP-SPDZ with circuit {circuit_name}...")
        spdz_local = subprocess.Popen(["./semi-party.x", "-N", "2", "-p", "0", "-OF", ".", "circuit", "-ip", "hosts"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        time.sleep(1) # to be sure that the process was started
        run_remote_command(ssh, f"cd ../testing/MP-SPDZ && ./semi-party.x -N 2 -p 1 -OF . circuit -ip hosts")
        spdz_local.wait()

        spdz_local.stdout.read()
        output = spdz_local.stderr.read()
        time_wan = extract_time_from_output(output)
        if time_wan is not None:
            benchmarks[circuit_name]["wan"] = f"{time_wan:.6f}"

        print()
        print("------------------------------")
        print()
    
    ssh.close()
    os.chdir("../circom-mp-spdz")
    write_benchmark_table(benchmarks)
    write_data_info_to_benchmark_file(benchmarks)

if __name__ == "__main__":
    main()