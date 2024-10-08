pragma circom 2.0.0;

// Flatten layer with that accepts a 2D input
template Flatten2D (nRows, nCols, nChannels) {
    signal input in[nRows][nCols][nChannels];
    signal output out[nRows*nCols*nChannels];

    var idx = 0;

    for (var i=0; i<nRows; i++) {
        for (var j=0; j<nCols; j++) {
            for (var k=0; k<nChannels; k++) {
                // TODO: remove a need to create a gate
                out[idx] <== in[i][j][k] + 0;
                idx++;
            }
        }
    }
}