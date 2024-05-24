pragma circom 2.0.0;

template Main() {
    signal input a;
    signal input b;
    signal input c <== 3;

    signal output a_add_b <== a + b;
    signal output a_mul_c <== a * c;
}

component main = Main();
