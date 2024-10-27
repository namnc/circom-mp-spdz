pragma circom 2.0.0;

include "../circuits/Flatten2D.circom";
include "../circuits/ReLU.circom";
include "../circuits/Conv2D.circom";
include "../circuits/Dense.circom";
include "../circuits/BatchNormalization2D.circom";
include "../circuits/ArgMax.circom";
include "../circuits/MaxPooling2D.circom";
include "../circuits/AveragePooling2D.circom";

template Model() {
signal input in[28][28][1];
signal input conv2d_weights[3][3][1][4];
signal input conv2d_bias[4];
signal input conv2d_out[26][26][4];
signal input batch_normalization_a[4];
signal input batch_normalization_b[4];
signal input batch_normalization_out[26][26][4];
signal input activation_out[26][26][4];
signal input max_pooling2d_out[13][13][4];
signal input conv2d_1_weights[3][3][4][8];
signal input conv2d_1_bias[8];
signal input conv2d_1_out[6][6][8];
signal input re_lu_out[6][6][8];
signal input average_pooling2d_out[3][3][8];
signal input flatten_out[72];
signal input dense_weights[72][10];
signal input dense_bias[10];
signal input dense_out[10];
signal input dense_softmax_out[1];
signal output out[1];

component conv2d = Conv2D(28, 28, 1, 4, 3, 1, 18);
component batch_normalization = BatchNormalization2D(26, 26, 4, 18);
component activation[26][26][4];
for (var i0 = 0; i0 < 26; i0++) {
    for (var i1 = 0; i1 < 26; i1++) {
        for (var i2 = 0; i2 < 4; i2++) {
            activation[i0][i1][i2] = ReLU();
}}}
component max_pooling2d = MaxPooling2D(26, 26, 4, 2, 2);
component conv2d_1 = Conv2D(13, 13, 4, 8, 3, 2, 18);
component re_lu[6][6][8];
for (var i0 = 0; i0 < 6; i0++) {
    for (var i1 = 0; i1 < 6; i1++) {
        for (var i2 = 0; i2 < 8; i2++) {
            re_lu[i0][i1][i2] = ReLU();
}}}
component average_pooling2d = AveragePooling2D(6, 6, 8, 2, 2);
component flatten = Flatten2D(3, 3, 8);
component dense = Dense(72, 10, 18);
component dense_softmax = ArgMax(10);

for (var i0 = 0; i0 < 28; i0++) {
    for (var i1 = 0; i1 < 28; i1++) {
        for (var i2 = 0; i2 < 1; i2++) {
            conv2d.in[i0][i1][i2] <== in[i0][i1][i2];
}}}
for (var i0 = 0; i0 < 3; i0++) {
    for (var i1 = 0; i1 < 3; i1++) {
        for (var i2 = 0; i2 < 1; i2++) {
            for (var i3 = 0; i3 < 4; i3++) {
                conv2d.weights[i0][i1][i2][i3] <== conv2d_weights[i0][i1][i2][i3];
}}}}
for (var i0 = 0; i0 < 4; i0++) {
    conv2d.bias[i0] <== conv2d_bias[i0];
}
for (var i0 = 0; i0 < 26; i0++) {
    for (var i1 = 0; i1 < 26; i1++) {
        for (var i2 = 0; i2 < 4; i2++) {
            conv2d.out[i0][i1][i2] <== conv2d_out[i0][i1][i2];
}}}
for (var i0 = 0; i0 < 26; i0++) {
    for (var i1 = 0; i1 < 26; i1++) {
        for (var i2 = 0; i2 < 4; i2++) {
            batch_normalization.in[i0][i1][i2] <== conv2d.out[i0][i1][i2];
}}}
for (var i0 = 0; i0 < 4; i0++) {
    batch_normalization.a[i0] <== batch_normalization_a[i0];
}
for (var i0 = 0; i0 < 4; i0++) {
    batch_normalization.b[i0] <== batch_normalization_b[i0];
}
for (var i0 = 0; i0 < 26; i0++) {
    for (var i1 = 0; i1 < 26; i1++) {
        for (var i2 = 0; i2 < 4; i2++) {
            batch_normalization.out[i0][i1][i2] <== batch_normalization_out[i0][i1][i2];
}}}
for (var i0 = 0; i0 < 26; i0++) {
    for (var i1 = 0; i1 < 26; i1++) {
        for (var i2 = 0; i2 < 4; i2++) {
            activation[i0][i1][i2].in <== batch_normalization.out[i0][i1][i2];
}}}
for (var i0 = 0; i0 < 26; i0++) {
    for (var i1 = 0; i1 < 26; i1++) {
        for (var i2 = 0; i2 < 4; i2++) {
            activation[i0][i1][i2].out <== activation_out[i0][i1][i2];
}}}
for (var i0 = 0; i0 < 26; i0++) {
    for (var i1 = 0; i1 < 26; i1++) {
        for (var i2 = 0; i2 < 4; i2++) {
            max_pooling2d.in[i0][i1][i2] <== activation[i0][i1][i2].out;
}}}
for (var i0 = 0; i0 < 13; i0++) {
    for (var i1 = 0; i1 < 13; i1++) {
        for (var i2 = 0; i2 < 4; i2++) {
            max_pooling2d.out[i0][i1][i2] <== max_pooling2d_out[i0][i1][i2];
}}}
for (var i0 = 0; i0 < 13; i0++) {
    for (var i1 = 0; i1 < 13; i1++) {
        for (var i2 = 0; i2 < 4; i2++) {
            conv2d_1.in[i0][i1][i2] <== max_pooling2d.out[i0][i1][i2];
}}}
for (var i0 = 0; i0 < 3; i0++) {
    for (var i1 = 0; i1 < 3; i1++) {
        for (var i2 = 0; i2 < 4; i2++) {
            for (var i3 = 0; i3 < 8; i3++) {
                conv2d_1.weights[i0][i1][i2][i3] <== conv2d_1_weights[i0][i1][i2][i3];
}}}}
for (var i0 = 0; i0 < 8; i0++) {
    conv2d_1.bias[i0] <== conv2d_1_bias[i0];
}
for (var i0 = 0; i0 < 6; i0++) {
    for (var i1 = 0; i1 < 6; i1++) {
        for (var i2 = 0; i2 < 8; i2++) {
            conv2d_1.out[i0][i1][i2] <== conv2d_1_out[i0][i1][i2];
}}}
for (var i0 = 0; i0 < 6; i0++) {
    for (var i1 = 0; i1 < 6; i1++) {
        for (var i2 = 0; i2 < 8; i2++) {
            re_lu[i0][i1][i2].in <== conv2d_1.out[i0][i1][i2];
}}}
for (var i0 = 0; i0 < 6; i0++) {
    for (var i1 = 0; i1 < 6; i1++) {
        for (var i2 = 0; i2 < 8; i2++) {
            re_lu[i0][i1][i2].out <== re_lu_out[i0][i1][i2];
}}}
for (var i0 = 0; i0 < 6; i0++) {
    for (var i1 = 0; i1 < 6; i1++) {
        for (var i2 = 0; i2 < 8; i2++) {
            average_pooling2d.in[i0][i1][i2] <== re_lu[i0][i1][i2].out;
}}}
for (var i0 = 0; i0 < 3; i0++) {
    for (var i1 = 0; i1 < 3; i1++) {
        for (var i2 = 0; i2 < 8; i2++) {
            average_pooling2d.out[i0][i1][i2] <== average_pooling2d_out[i0][i1][i2];
}}}
for (var i0 = 0; i0 < 3; i0++) {
    for (var i1 = 0; i1 < 3; i1++) {
        for (var i2 = 0; i2 < 8; i2++) {
            flatten.in[i0][i1][i2] <== average_pooling2d.out[i0][i1][i2];
}}}
for (var i0 = 0; i0 < 72; i0++) {
    flatten.out[i0] <== flatten_out[i0];
}
for (var i0 = 0; i0 < 72; i0++) {
    dense.in[i0] <== flatten.out[i0];
}
for (var i0 = 0; i0 < 72; i0++) {
    for (var i1 = 0; i1 < 10; i1++) {
        dense.weights[i0][i1] <== dense_weights[i0][i1];
}}
for (var i0 = 0; i0 < 10; i0++) {
    dense.bias[i0] <== dense_bias[i0];
}
for (var i0 = 0; i0 < 10; i0++) {
    dense.out[i0] <== dense_out[i0];
}
for (var i0 = 0; i0 < 10; i0++) {
    dense_softmax.in[i0] <== dense.out[i0];
}
for (var i0 = 0; i0 < 1; i0++) {
    dense_softmax.out[i0] <== dense_softmax_out[i0];
}
out[0] <== dense_softmax.out;

}

component main = Model();
