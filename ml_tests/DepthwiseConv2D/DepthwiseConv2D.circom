pragma circom 2.1.0;

include "../circuits/DepthwiseConv2D.circom";

component main = DepthwiseConv2D(5, 5, 3, 2, 3, 1, 10**36);
