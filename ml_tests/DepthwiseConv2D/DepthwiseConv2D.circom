pragma circom 2.1.0;

include "../circuits/DepthwiseConv2D.circom";

component main = DepthwiseConv2D(5, 5, 2, 4, 3, 1, 8);
