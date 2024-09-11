import argparse
from dataclasses import dataclass
from enum import Enum
import json
import os
import subprocess
from pathlib import Path
import re

import time


class AGateType(Enum):
    ADD = 'AAdd'
    DIV = 'ADiv'
    EQ = 'AEq'
    GT = 'AGt'
    GEQ = 'AGEq'
    LT = 'ALt'
    LEQ = 'ALEq'
    MUL = 'AMul'
    NEQ = 'ANeq'
    SUB = 'ASub'
    BW_XOR = 'AXor'
    POW = 'APow'
    IDIV = 'AIntDiv'
    MOD = 'AMod'
    BW_SHL = 'AShiftL'
    BW_SHR = 'AShiftR'
    BW_OR = 'ABoolOr'
    BW_AND = 'ABoolAnd'
    # ABitOr,
    # ABitAnd,


MAP_GATE_TYPE_TO_OPERATOR_STR = {
    AGateType.ADD: '+',
    AGateType.MUL: '*',
    AGateType.DIV: '/',
    AGateType.LT: '<',
    AGateType.SUB: '-',
    AGateType.EQ: '==',
    AGateType.NEQ: '!=',
    AGateType.GT: '>',
    AGateType.GEQ: '>=',
    AGateType.LEQ: '<=',
    AGateType.BW_XOR: "^",
    AGateType.POW: "**",
    AGateType.IDIV: "/",
    AGateType.MOD: "%",
    AGateType.BW_SHL: "<<",
    AGateType.BW_SHR: ">>",
    AGateType.BW_OR: "|",
    AGateType.BW_AND:"&"
}



PROJECT_ROOT = Path(__file__).parent
CIRCOM_2_ARITHC_PROJECT_ROOT = PROJECT_ROOT / '..' / 'circom-2-arithc'
MPSPDZ_PROJECT_ROOT = PROJECT_ROOT / '..' / 'MP-SPDZ'
MPSPDZ_CIRCUIT_DIR = MPSPDZ_PROJECT_ROOT / 'Programs' / 'Source'
ARITHC_TO_BRISTOL_SCRIPT = PROJECT_ROOT / "arithc_to_bristol.py"
EXAMPLES_DIR = PROJECT_ROOT / 'ml_tests'

MPC_PROTOCOL = 'semi'


def generate_mpspdz_circuit(
    arith_circuit_path: Path,
    circuit_info_path: Path,
    mpc_settings_path: Path,
) -> Path:
    '''
    Generate the MP-SPDZ circuit code that can be run by MP-SPDZ.

    Steps:
    1. Read the arithmetic circuit file to get the gates
    2. Read the circuit info file to get the input/output wire mapping
    3. Read the input config file to get which party inputs should be read from
    4. Generate the MP-SPDZ from the inputs above. The code should:
        4.1. Initialize a `wires` list with input wires filled in: if a wire is a constant, fill it in directly. if a wire is an input, fill in which party this input comes from
        4.2. Translate the gates into corresponding operations in MP-SPDZ
        4.3. Print the outputs
    '''
    # {
    #   "input_name_to_wire_index": { "a": 1, "b": 0, "c": 2},
    #   "constants": {"d": {"value": 50, "wire_index": 3}},
    #   "output_name_to_wire_index": { "a_add_b": 4, "a_mul_c": 5 }
    # }
    with open(circuit_info_path, 'r') as f:
        raw = json.load(f)

    input_name_to_wire_index = {k: int(v) for k, v in raw['input_name_to_wire_index'].items()}
    constants: dict[str, dict[str, int]] = raw['constants']
    output_name_to_wire_index = {k: int(v) for k, v in raw['output_name_to_wire_index'].items()}
    # [
    #     {
    #         "name": "alice",
    #         "inputs": ["a"],
    #         "outputs": ["a_add_b", "a_mul_c"]
    #     },
    #     {
    #         "name": "bob",
    #         "inputs": ["b"],
    #         "outputs": ["a_add_b", "a_mul_c"]
    #     }
    # ]
    with open(mpc_settings_path, 'r') as f:
        mpc_settings = json.load(f)

    # Read number of wires from the bristol circuit file
    # A bristol circuit file looks like this:
    # 2 5
    # 3 1 1 1
    # 2 1 1
    #
    # 2 1 1 0 3 AAdd
    # 2 1 1 2 4 AMul
    # """

    # Each gate line looks like this: '2 1 1 0 3 AAdd'
    @dataclass(frozen=True)
    class Gate:
        num_inputs: int
        num_outputs: int
        gate_type: AGateType
        inputs_wires: list[int]
        output_wire: int
    with open(arith_circuit_path, 'r') as f:
        first_line = next(f)
        num_gates, num_wires = map(int, first_line.split())
        second_line = next(f)
        num_inputs = int(second_line.split()[0])
        third_line = next(f)
        num_outputs = int(third_line.split()[0])
        # Skip the next line
        next(f)

        # Read the gate lines
        gates: list[Gate] = []
        for line in f:
            line = line.split()
            num_inputs = int(line[0])
            num_outputs = int(line[1])
            inputs_wires = [int(x) for x in line[2:2+num_inputs]]
            # Support 2 inputs only for now
            assert num_inputs == 2 and num_inputs == len(inputs_wires)
            output_wires = list(map(int, line[2+num_inputs:2+num_inputs+num_outputs]))
            output_wire = output_wires[0]
            # Support 1 output only for now
            assert num_outputs == 1 and num_outputs == len(output_wires)
            gate_type = AGateType(line[2+num_inputs+num_outputs])
            gates.append(Gate(num_inputs, num_outputs, gate_type, inputs_wires, output_wire))
    assert len(gates) == num_gates

    # Make inputs to circuit (not wires!!) from the user config
    # Initialize a list `inputs` with `num_wires` with value=None
    inputs_str_list = [None] * num_wires
    print_outputs_str_list = []
    # Fill in the constants
    for name, o in constants.items():
        value = int(o['value'])
        # descaled_value = value / (10 ** scale)
        wire_index = int(o['wire_index'])
        # Sanity check
        if inputs_str_list[wire_index] is not None:
            raise ValueError(f"Wire index {wire_index} is already filled in: {inputs_str_list[wire_index]=}")
        # Should check if we should use cfix instead
        inputs_str_list[wire_index] = f'cint({value})'
    for party_index, party_settings in enumerate(mpc_settings):
        # Fill in the inputs from the parties
        for input_name in party_settings['inputs']:
            wire_index = int(input_name_to_wire_index[input_name])
            # Sanity check
            if inputs_str_list[wire_index] is not None:
                raise ValueError(f"Wire index {wire_index} is already filled in: {inputs_str_list[wire_index]=}")
            # Should check if we should use sfix instead
            inputs_str_list[wire_index] = f'sint.get_input_from({party_index})'
        # Fill in the outputs
        for output_name in party_settings['outputs']:
            wire_index = int(output_name_to_wire_index[output_name])
            print_outputs_str_list.append(
                f"print_ln_to({party_index}, 'outputs[{len(print_outputs_str_list)}]: {output_name}=%s', wires[{wire_index}].reveal_to({party_index}))"
            )


    # Replace all `None` with str `'None'`
    inputs_str_list = [x if x is not None else 'None' for x in inputs_str_list]

    #
    # Generate the circuit code
    #
    inputs_str = '[' + ', '.join(inputs_str_list) + ']'

    # Translate bristol gates to MP-SPDZ operations
    # E.g.
    # '2 1 1 0 2 AAdd' in bristol
    #   is translated to
    # 'wires[2] = wires[1] + wires[0]' in MP-SPDZ
    gates_str_list = []
    for gate in gates:
        gate_str = ''
        if gate.gate_type not in MAP_GATE_TYPE_TO_OPERATOR_STR:
            raise ValueError(f"Gate type {gate.gate_type} is not supported")
        else:
            operator_str = MAP_GATE_TYPE_TO_OPERATOR_STR[gate.gate_type]
            gate_str = f'wires[{gate.output_wire}] = wires[{gate.inputs_wires[0]}] {operator_str} wires[{gate.inputs_wires[1]}]'
        gates_str_list.append(gate_str)
    gates_str = '\n'.join(gates_str_list)

    # For outputs, should print the actual output names, and
    # lines are ordered by actual output wire index since it's guaranteed the order
    # E.g.
    # print_ln('outputs[0]: a_add_b=%s', outputs[0].reveal())
    # print_ln('outputs[1]: a_mul_c=%s', outputs[1].reveal())
    # print_outputs_str_list = [
    #     f"print_ln('outputs[{i}]: {output_name}=%s', wires[{output_name_to_wire_index[output_name]}].reveal())"
    #     for i, output_name in enumerate(output_name_to_wire_index.keys())
    # ]
    print_outputs_str = '\n'.join(print_outputs_str_list)

    circuit_code = f"""
program.use_trunc_pr = True
program.use_edabit(True)
wires = {inputs_str}
{gates_str}
# Print outputs
{print_outputs_str}
"""
    circuit_name = arith_circuit_path.stem
    out_mpc_path = MPSPDZ_CIRCUIT_DIR / f"{circuit_name}.mpc"
    with open(out_mpc_path, 'w') as f:
        f.write(circuit_code)
    return out_mpc_path


def generate_mpspdz_inputs_for_party(
    party: int,
    input_json_for_party_path: Path,
    circuit_info_path: Path,
    mpc_settings_path: Path,
):
    '''
    Generate MP-SPDZ circuit inputs for a party.

    For each party, we need to translate `party_{i}.inputs.json` to an input file for MP-SPDZ according to their inputs' wire order
    - The input file format of MP-SPDZ is `input0 input1 input2 ... inputN`. Each value is separated with a space
    - This order is determined by the position (index) of the inputs in the MP-SPDZ wires
        - For example, the actual wires in the generated MP-SPDZ circuit might look like this:
            `[cfix(123), sfix.get_input_from(0), sfix.get_input_from(1), cfix(456), sfix.get_input_from(0), ...]`
            - For party `0`, its MP-SPDZ inputs file should contain two values: one is for the first `sfix.get_input_from(0)`
                and the other is for the second `sfix.get_input_from(0)`.
        - This order can be obtained by sorting the `input_name_to_wire_index` by the wire index
    '''

    # Read inputs value from user provided input files
    with open(input_json_for_party_path) as f:
        input_values_for_party_json = json.load(f)

    with open(mpc_settings_path, 'r') as f:
        mpc_settings = json.load(f)
    inputs_from: dict[str, int] = {}
    for party_index, party_settings in enumerate(mpc_settings):
        for input_name in party_settings['inputs']:
            inputs_from[input_name] = int(party_index)

    with open(circuit_info_path, 'r') as f:
        circuit_info = json.load(f)
        input_name_to_wire_index = circuit_info['input_name_to_wire_index']

    wire_to_name_sorted = sorted(input_name_to_wire_index.items(), key=lambda x: x[1])
    wire_value_in_order_for_mpsdz = []
    for wire_name, wire_index in wire_to_name_sorted:
        wire_from_party = int(inputs_from[wire_name])
        # For the current party, we only care about the inputs from itself
        if wire_from_party == party:
            wire_value = input_values_for_party_json[wire_name]
            wire_value_in_order_for_mpsdz.append(wire_value)
    # Write these ordered wire inputs for mp-spdz usage
    input_file_for_party_mpspdz = MPSPDZ_PROJECT_ROOT / "Player-Data" / f"Input-P{party}-0"
    with open(input_file_for_party_mpspdz, 'w') as f:
        f.write(" ".join(map(str, wire_value_in_order_for_mpsdz)))
    return input_file_for_party_mpspdz


def run_mpspdz_circuit(mpspdz_circuit_path: Path, num_parties: int) -> dict[str, int]:
    # Run the MP-SPDZ interpreter to interpret the arithmetic circuit
    # mpspdz_circuit_path = 'tutorial.mpc'
    assert mpspdz_circuit_path.exists(), f"The MP-SPDZ circuit file {mpspdz_circuit_path} does not exist."
    assert mpspdz_circuit_path.suffix == '.mpc', f"The MP-SPDZ circuit file {mpspdz_circuit_path} should have the extension .mpc."
    # Check mpspdz_circuit_path is under mpspdz_circuit_dir
    assert mpspdz_circuit_path.parent.absolute() == MPSPDZ_CIRCUIT_DIR.absolute(), \
        f"The MP-SPDZ circuit file {mpspdz_circuit_path} should be under {MPSPDZ_CIRCUIT_DIR}."
    # circuit_name = 'tutorial'
    circuit_name = mpspdz_circuit_path.stem
    # Compile and run MP-SPDZ in the local machine
    command = f'cd {MPSPDZ_PROJECT_ROOT} && PLAYERS={num_parties} Scripts/compile-run.py -E {MPC_PROTOCOL} {circuit_name} -M'

    result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    if result.returncode != 0:
        raise ValueError(f"Failed to run MP-SPDZ interpreter. Error code: {result.returncode}\n{result.stderr}")

    # Use regular expressions to parse the output
    # E.g.
    # "outputs[0]: keras_tensor_3=16"
    # "outputs[1]: keras_tensor_4[0][0]=8.47524e+32"
    # ...
    output_pattern = re.compile(r"outputs\[\d+\]: 0.(\w+(?:\[\d+\])*)=(.+)$")
    outputs = {}
    for line in result.stdout.splitlines():
        match = output_pattern.search(line)
        if match:
            output_name, value = match.groups()
            outputs[output_name] = float(value) if '.' in value else int(value)
    return outputs


def main():
    parser = argparse.ArgumentParser(description="Compile circom to JSON and Bristol and circuit info files.")
    parser.add_argument("circuit_name", type=str, help="The name of the circuit (used for input/output file naming)")

    args = parser.parse_args()
    circuit_name = args.circuit_name

    circuit_dir = EXAMPLES_DIR / circuit_name
    circom_path = circuit_dir / f"{circuit_name}.circom"
    mpc_settings_path = circuit_dir / "mpc_settings.json"

    # ./outputs/{circuit_name}/...
    output_dir = PROJECT_ROOT / Path("outputs") / circuit_name
    output_dir.mkdir(parents=True, exist_ok=True)
    # Step 1: run circom-2-arithc
    code = os.system(f"cd {CIRCOM_2_ARITHC_PROJECT_ROOT} && ./target/release/circom-2-arithc --input {circom_path} --output {output_dir}")
    if code != 0:
        raise ValueError(f"Failed to compile circom. Error code: {code}")
    
    # Step 1b: run circuit script
    # python {circuit}.py
    code = os.system(f"cd {circuit_dir} && python3 {circuit_name}.py")
    if code != 0:
        raise ValueError(f"Failed to run {circuit_name}.py. Error code: {code}")
    
    with open(mpc_settings_path, 'r') as f:
        mpc_settings = json.load(f)
    num_parties = len(mpc_settings)
    input_json_path_for_each_party = [circuit_dir / f"inputs_party_{i}.json" for i in range(num_parties)]
    
    # code = os.system(f"cd {circuit_dir} && cp ./raw_circuit.mpc {MPSPDZ_CIRCUIT_DIR}")
    # if code != 0:
    #     raise ValueError(f"Failed to move raw_circuit.mpc. Error code: {code}")

    
    # Step 2: run arithc-to-bristol
    # python arithc_to_bristol.py {arithc_path} {output_dir}
    arithc_path = output_dir / "circuit.json"
    ### NOW NOT NEEDED
    # code = os.system(f"python {ARITHC_TO_BRISTOL_SCRIPT} {arithc_path} {output_dir}")
    # if code != 0:
    #     raise ValueError(f"Failed to run arithc-to-bristol. Error code: {code}")
    ### NOW NOT NEEDED

    bristol_path = output_dir / "circuit.txt"
    circuit_info_path = output_dir / "circuit_info.json"
    # Step 3: generate MP-SPDZ circuit
    mpspdz_circuit_path = generate_mpspdz_circuit(
        bristol_path,
        circuit_info_path,
        mpc_settings_path,
    )
    print(f"Generated MP-SPDZ circuit at {mpspdz_circuit_path}")

    code = os.system(f"cd {MPSPDZ_CIRCUIT_DIR} && cp ./circuit.mpc {output_dir}")
    if code != 0:
        raise ValueError(f"Failed to compile circom. Error code: {code}")
    
    # Step 4: generate MP-SPDZ inputs for each party
    for i, input_json_for_party_path in enumerate(input_json_path_for_each_party):
        input_file_for_party_mpspdz = generate_mpspdz_inputs_for_party(
            i,
            input_json_for_party_path,
            circuit_info_path,
            mpc_settings_path,
        )
        print(f"Generated MP-SPDZ inputs for party {i} at {input_file_for_party_mpspdz}")

    st = time.time()
    # Step 5: run MP-SPDZ circuit
    outputs = run_mpspdz_circuit(mpspdz_circuit_path, num_parties)
    print(f"\n\n\n========= Computation has finished =========\n\n")
    print(f"Outputs: {outputs}")
    et = time.time()
    elapsed_time = et - st
    print('\n\n\nCIRCOM Execution time:', elapsed_time, 'seconds')
    with open(f"./outputs/{circuit_name}/benchmark.json", 'w') as fp:
        json.dump({"computation_time" : elapsed_time}, fp)

    # rawpath = Path(str(mpspdz_circuit_path).replace("circuit", "raw_circuit"));
    # print(f"\n\n\nBENCH RAW MP-SPDZ circuit at {rawpath}")

    # st = time.time()
    # raw_outputs = run_mpspdz_circuit(rawpath, num_parties)
    # print(f"\n\n\n========= Raw Computation has finished =========\n\n")
    # print(f"Outputs: {raw_outputs}")
    # et = time.time()
    # elapsed_time = et - st
    # print('\n\n\nRAW Execution time:', elapsed_time, 'seconds')


if __name__ == '__main__':
    main()
