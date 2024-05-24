# circom-mp-spdz

circom-MP-SPDZ allows parties to perform Multi-Party Computation (MPC) by writing Circom code using the MP-SPDZ framework. Circom code is converted to an arithmetic circuit and then translated gate by gate to the corresponding MP-SPDZ operators. See the write-up to learn how it works and the spec of inputs and outputs: [circom-mp-spdz write-up](https://hackmd.io/Iuu9yge4ShKBjawAcmFjvw?view).

## Structure
- [circom-2-arithc](./circom-2-arithc) - we're using a forked version of circom-2-arithc that supports the old arithmetic circuit format, which is not compatible with the latest version of [circom-2-arithc](https://github.com/namnc/circom-2-arithc).
- [MP-SPDZ](./MP-SPDZ) - the MP-SPDZ framework to run the MPC protocol.
- [arithc_to_bristol.py](./arithc_to_bristol.py) - a script to convert the arithmetic circuit to the Bristol format.
- [main.py](./main.py) - the main script to run the circom-mp-spdz. It does the following:
  - Compiles the Circom code to the arithmetic circuit with `circom-2-arithc`.
  - Converts the arithmetic circuit to the Bristol format with `arithc_to_bristol.py`.
  - Generates an MP-SPDZ circuit from the Bristol format circuit.
  - Generates MP-SPDZ input files for each party from the `inputs_party_i.json`.
  - Performs the computation using MP-SPDZ by running all parties on the local machine.
  - Prints the outputs.
- [examples](./examples) - example circuits to run with circom-mp-spdz.

## Installation

### Clone the repo

```bash
git clone --recurse-submodules https://github.com/namnc/circom-mp-spdz.git
cd circom-mp-spdz
```

If you forgot to clone with `--recurse-submodules`

```bash
git submodule init
git submodule update
```

### Build circom-2-arithc
Go to the circom-2-arithc submodule directory:
```bash
cd circom-2-arithc
```

Initialize the .env file:
```bash
cp .env.example .env
```

Build the compiler:

```bash
cargo build --release
```

### Build MP-SPDZ

Go to the MP-SPDZ submodule directory:
```bash
cd ../MP-SPDZ
```

Build the MPC VM for `semi` protocol

```bash
make -j8 semi-party.x
# Make sure `semi-party.x` exists
ls semi-party.x
```

## How to run

We have two examples available
- [two_outputs](./examples/two_outputs/) - a simple circuit with only 3 inputs, 2 gates, and 2 outputs
- [nn_circuit_small](./examples/nn_circuit_small/) - a small neural network circuit, which is more complex

In both examples, we assume there are only 2 parties. You will find the following files in each example directory:
- `circuit.circom` - the circom code representing the circuit to be computed by all parties
- `mpc_settings.json` - the settings file defining for each party:
    - the party's name in string format
    - which input signals they should provide
    - which output signals they can learn the value of
- `inputs_party_0.json` - the input file for party 0. It must contain all the inputs for party 0
- `inputs_party_1.json` - the input file for party 1. It must contain all the inputs for party 1

See the section [Input files](https://hackmd.io/Iuu9yge4ShKBjawAcmFjvw?view#Input-files) in the write-up for more details.

You can run these examples by following the instructions in the root directory.

```bash
# Go back to the root directory of circom-mp-spdz
cd ..
python main.py {circuit_name}
```
- `{circuit_name}` is the name of the circuit you want to run. Can either be `two_outputs` or `nn_circuit_small`.
- Intermediate files will be stored in the `outputs/{circuit_name}` directory.
- Outputs are directly printed to the console.



#### Example `two_outputs`

```bash
python main.py two_outputs
```

You can see the the intermediate files in the `outputs/two_outputs` directory. And you should see the following outputs in the console:

```bash
...
========= Computation has finished =========


Outputs: {'a_add_b': 3, 'a_mul_c': 3}
```


#### Example `nn_circuit_small`

```bash
python main.py nn_circuit_small
```

You can see the the intermediate files in the `outputs/nn_circuit_small` directory. And you should see the following outputs in the console:

```bash
...
========= Computation has finished =========


Outputs: {'out[0]': 11846134085, 'out[1]': 12770577881, 'out[2]': 13695021677, 'out[3]': 14619465473}
```
