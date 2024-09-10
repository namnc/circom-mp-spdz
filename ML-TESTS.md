# Machine Learning circuits in circom-mp-spdz

[ml_tests](./ml_tests/) dir is a set of ML circuits - fork of [circomlib-ml](https://github.com/socathie/circomlib-ml); with circom-mp-spdz - project that connect frontend (circom2arithc compiler) and backend (e.g. MP-SPDZ) it's possible to run them with almost no changes.

## Changes in the circuits

Original circomlib-ml was aimed to work in zk, in a specific domain/field.Here it's different; and even though we still don't have an "access" to float numbers, but at least we can make "scaling" operations more effective. That's why we don't need `remainders` in the circuit as inputs **and** we don't need to do divisions (divisions check specifically) to scale back - we can use right shifts - they're free in the given domain.

## Minor changes in .mpc generator

Changes from the [original circom-mp-spdz runner](./main.py) script have been done in the [main_ml_tests.py](./main_ml_tests.py) in the .mpc generator. 
They were suggested by MP-SPDZ - adding two lines in the beginning of .mpc:
```bash
program.use_trunc_pr = True
program.use_edabit(True)
```

## Summary

As a result of the work we have benchmarks for different ML circuits. They can be found [here](./BENCHMARK.md). If you want to run benchmarks locally see [instruction](#how-to-run-ml-testsbenchmarks)

---

## How to run ml tests/benchmarks

Explained [here](https://hackmd.io/Lv6OuKNgQLqA6YGTGWG4DQ?view#Docker-Settings-abd-running-MP-SPDZ-on-multiple-machines)