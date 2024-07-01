pragma circom 2.1.0;

include "../circuits/SeparableConv2D.circom";

component main = SeparableConv2D(5, 5, 3, 2, 2, 3, 1, 10**36);