pragma circom 2.1.0;

include "../circuits/DepthwiseConv2D.circom";

component main = DepthwiseConv2D(7, 7, 3, 3, 3, 1, 10);
