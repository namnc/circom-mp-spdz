// from 0xZKML/zk-mnist

pragma circom 2.0.0;

include "../circuits/ArgMax.circom";

component main = ArgMax(5);

/* INPUT = {
    "in":  ["2","3","1","5","4"],
    "out": "3"
} */