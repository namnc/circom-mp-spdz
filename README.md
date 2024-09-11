# circom-mp-spdz

circom-MP-SPDZ allows parties to perform Multi-Party Computation (MPC) by writing Circom code using the MP-SPDZ framework. Circom code is compiled into an arithmetic circuit and then translated gate by gate to the corresponding MP-SPDZ operators. See the write-up to learn how it works (roughly) and the spec of inputs and outputs: [circom-mp-spdz write-up](https://hackmd.io/Iuu9yge4ShKBjawAcmFjvw?view).

**NOTE:** Now circom-2-arithc also conveniently outputs the Bristol format with corresponding circuit_info (hence the json_arbistol is not necessary anymore).

## Supported Circom Type and Op

| Type            | Op                       | Supported |
| --------------- | ------------------------ | :-------: |
| **Int** (sint, cint)        | `+`      Addition           |    ✅     |
|                 | `/`      Division            |    ✅     |
|                 | `==`     Equality      |    ✅     |
|                 | `>`      Greater Than      |    ✅     |
|                 | `>=`     Greater Than or Equal        |    ✅     |
|                 | `<`      Less Than            |    ✅     |
|                 | `<=`     Less Than or Equal            |    ✅     |
|                 | `*`   Multiplication     |    ✅     |
|                 | `!=` Not Equal |    ✅     |
|                 | `-`  Subtraction   |    ✅     |
|                 | `**` Exponentiation               |    ✅     |
|                 | `<<` Shift Left                |    ✅     |
|                 | `>>` Shift Right                |    ✅     |
|                 | `^`  Bitwise XOR               |    ❌     |
|                 | `\|` Bitwise OR                |    ❌     |
|                 | `&`  Bitwise AND               |    ❌     |
|                 | `%`  Modulo               |    ❌     |

**NOTE** Int can also be used in quantization aware mode, by scaling every input with 2^f and shift left f after every multiplication of two scaled values.

## Structure
- [circom-2-arithc](https://github.com/namnc/circom-2-arithc) - we're using commit [800e2d4](https://github.com/namnc/circom-2-arithc/commit/800e2d44aa175c57698de739e5839eb7af03498a) not so far from the latest version of [circom-2-arithc](https://github.com/namnc/circom-2-arithc).
- [MP-SPDZ](https://github.com/mhchia/MP-SPDZ/) - the custom MP-SPDZ framework to run the MPC protocol. We are using commit [704049e](https://github.com/mhchia/MP-SPDZ/commit/7eeb7e423e10bd023338d0dd60603b6624ab56eb).
- [arithc_to_bristol.py](./arithc_to_bristol.py) - a script to transplie the arithmetic Bristol format to MP-SPDZ .mpc program.
- [main.py](./main.py) - the main script to run the circom-mp-spdz. It does the following:
  - Compiles the Circom code to the arithmetic circuit with `circom-2-arithc`.
  - Generates an MP-SPDZ circuit from the Bristol format circuit with `arithc_to_bristol.py`.
  - Generates MP-SPDZ input files for each party from the `inputs_party_i.json`.
  - Performs the computation using MP-SPDZ by running all parties on the local machine.
  - Prints the outputs.
- [examples](./examples) - example circuits to run with circom-mp-spdz.

## Installation

### Clone the repo

```bash
git clone https://github.com/namnc/circom-mp-spdz.git
git clone https://github.com/namnc/circom-2-arithc
git clone https://github.com/mhchia/MP-SPDZ/
```

### Build circom-2-arithc
Go to the circom-2-arithc submodule directory:
```bash
cd circom-2-arithc
git checkout 800e2d4
```

Initialize the .env file:
```bash
touch .env
vim .env
```
and add LOG_LEVEL="DEBUG"

Build the compiler:

```bash
cargo build --release
```

### Build MP-SPDZ

You may need to install some dependencies, see: [MP-SPDZ](https://github.com/mhchia/MP-SPDZ/).

Go to the MP-SPDZ submodule directory:
```bash
cd ../MP-SPDZ
git checkout 704049e
```

Build the MPC VM for `semi` protocol

```bash
make -j8 semi-party.x
# Make sure `semi-party.x` exists
ls semi-party.x
```

## How to run

We have two examples available
- [ops_tests](./examples/ops_tests/) - a benchmark of supported ops for sint
- [naive_search](./examples/naive_search/) - a benchmark of naive search

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
- `{circuit_name}` is the name of the circuit you want to run. Can either be `ops_tests` or `naive_search`.
- Intermediate files will be stored in the `outputs/{circuit_name}` directory. **NOTE**: we also output `circuit.mpc` which you can use to run with the original MP-SPDZ.
- Outputs are directly printed to the console.



#### Example `ops_tests`

```bash
python main.py ops_tests
```

You can see the the intermediate files in the `outputs/ops_tests` directory. And you should see the following outputs in the console:

```bash
...
========= Computation has finished =========


Outputs: {...}
```


#### Example `naive_search`

```bash
python main.py naive_search
```

You can see the the intermediate files in the `outputs/naive_search` directory. And you should see the following outputs in the console:

```bash
...
========= Computation has finished =========


Outputs: {...}
```

# Moving Forward
The `circuit.mpc` program in the respective output folder can be used with MP-SPDZ in an appropriate deployment settings.
