import argparse
import os
import paramiko
import subprocess
import time

EXCLUDED_CIRCUITS = ["circomlib", "circomlib-matrix", "circuits", "crypto", "Keras2Circom", ".DS_Store"]
SSH_PORT = 22

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

    for circuit_name in circuits_to_compile:
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

        print("6. Set Latency for Europe/One region")
        run_remote_command(ssh, f"tc qdisc del dev eth0 root")
        run_remote_command(ssh, f"tc qdisc add dev eth0 root handle 1:0 netem delay 2ms")
        run_remote_command(ssh, f"tc qdisc add dev eth0 parent 1:1 handle 10:0 tbf rate 5gbit burst 200kb limit 20000kb")

        print(f"7. Running MP-SPDZ with circuit {circuit_name}...")
        spdz_local = subprocess.Popen(["./semi-party.x", "-N", "2", "-p", "0", "-OF", ".", "circuit", "-ip", "hosts"])
        time.sleep(1) # to be sure that the process was started
        run_remote_command(ssh, f"cd ../testing/MP-SPDZ && ./semi-party.x -N 2 -p 1 -OF . circuit -ip hosts")
        spdz_local.wait()
        print()
        print()

        print("7. Set Latency for US-Europe/two regions")
        run_remote_command(ssh, f"tc qdisc del dev eth0 root")
        run_remote_command(ssh, f"tc qdisc add dev eth0 root handle 1:0 netem delay 75ms")
        run_remote_command(ssh, f"tc qdisc add dev eth0 parent 1:1 handle 10:0 tbf rate 2.5gbit burst 150kb limit 15000kb")

        print(f"8. Running MP-SPDZ with circuit {circuit_name}...")
        spdz_local = subprocess.Popen(["./semi-party.x", "-N", "2", "-p", "0", "-OF", ".", "circuit", "-ip", "hosts"])
        time.sleep(1) # to be sure that the process was started
        run_remote_command(ssh, f"cd ../testing/MP-SPDZ && ./semi-party.x -N 2 -p 1 -OF . circuit -ip hosts")
        spdz_local.wait()
        print()
        print("------------------------------")
        print()

    ssh.close()

if __name__ == "__main__":
    main()