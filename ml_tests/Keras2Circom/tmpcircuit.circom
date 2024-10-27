pragma circom 2.0.0;

include "../circuits/ArgMax.circom";
include "../circuits/Dense.circom";
include "../circuits/Flatten2D.circom";

template Model() {
signal input in[2][1][1];
signal input dense_23_weights[2][10];
signal input dense_23_bias[10];
signal output out[1];

component flatten_11 = Flatten2D(2, 1, 1);
component dense_23 = Dense(2, 10, 18);
component dense_23_softmax = ArgMax(10);

for (var i0 = 0; i0 < 2; i0++) {
    for (var i1 = 0; i1 < 1; i1++) {
        for (var i2 = 0; i2 < 1; i2++) {
            flatten_11.in[i0][i1][i2] <== in[i0][i1][i2];
}}}
for (var i0 = 0; i0 < 2; i0++) {
    flatten_11.out[i0] <== flatten_11_out[i0];
}
for (var i0 = 0; i0 < 2; i0++) {
    dense_23.in[i0] <== flatten_11.out[i0];
}
for (var i0 = 0; i0 < 2; i0++) {
    for (var i1 = 0; i1 < 10; i1++) {
        dense_23.weights[i0][i1] <== dense_23_weights[i0][i1];
}}
for (var i0 = 0; i0 < 10; i0++) {
    dense_23.bias[i0] <== dense_23_bias[i0];
}
for (var i0 = 0; i0 < 10; i0++) {
    dense_23.out[i0] <== dense_23_out[i0];
}
for (var i0 = 0; i0 < 10; i0++) {
    dense_23_softmax.in[i0] <== dense_23.out[i0];
}
for (var i0 = 0; i0 < 1; i0++) {
    dense_23_softmax.out[i0] <== dense_23_softmax_out[i0];
}
out[0] <== dense_23_softmax.out;

}

component main = Model();
