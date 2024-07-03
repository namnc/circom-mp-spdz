pragma circom 2.1.0;

include "../circuits/DepthwiseConv2D.circom";

component main = DepthwiseConv2D(3, 3, 8, 8, 3, 1, 8);
