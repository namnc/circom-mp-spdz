# circom-mp-spdz

circom-MP-SPDZ allows parties to perform Multi-Party Computation (MPC) by writing Circom code using the MP-SPDZ framework. Circom code is converted to an arithmetic circuit and then gate by gate translated to the corresponding MP-SPDZ operators.

In the current structure, input files are not limited to MP-SPDZ and can be applied to other MPC frameworks. We can adapt generate_mpspdz_circuit and generate_mpspdz_inputs_for_party to support other MPC frameworks.

See the write-up for more details: [circom-mp-spdz write-up](https://hackmd.io/Iuu9yge4ShKBjawAcmFjvw?view).

## Get started

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

NOTE: We are using a forked version of circom-2-arithc because our code relies on the old arithmetic circuit format, which is not compatible with the latest version of [circom-2-arithc](https://github.com/namnc/circom-2-arithc).


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

### Run the example

We have two examples available
- [two_outputs](./examples/two_outputs/) - a simple circuit with two outputs
- [nn_circuit_small](./examples/nn_circuit_small/) - a small neural network circuit

You can run these examples by following the instructions in the root directory.

```bash
# Go back to the root directory of circom-mp-spdz
cd ..
python main.py {circuit_name}
```
- `{circuit_name}` is the name of the circuit you want to run.
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
