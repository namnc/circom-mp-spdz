# The code is taken from https://github.com/ora-io/keras2circom

# assume all inputs are strings
def AveragePooling2DInt (nRows, nCols, nChannels, poolSize, strides, input):
    out = [[[0 for _ in range(nChannels)] for _ in range((nCols-poolSize)//strides + 1)] for _ in range((nRows-poolSize)//strides + 1)]
    for i in range((nRows-poolSize)//strides + 1):
        for j in range((nCols-poolSize)//strides + 1):
            for k in range(nChannels):
                for x in range(poolSize):
                    for y in range(poolSize):
                        out[i][j][k] += float(input[i*strides+x][j*strides+y][k])
                out[i][j][k] = str(out[i][j][k] / poolSize**2)
    return out

def BatchNormalizationInt(nRows, nCols, nChannels, n, X_in, a_in, b_in):
    out = [[[None for _ in range(nChannels)] for _ in range(nCols)] for _ in range(nRows)]
    for i in range(nRows):
        for j in range(nCols):
            for k in range(nChannels):
                out[i][j][k] = float(X_in[i][j][k])*float(a_in[k]) + float(b_in[k])
                out[i][j][k] = str(out[i][j][k])
    return out

def Conv1DInt(nInputs, nChannels, nFilters, kernelSize, strides, n, input, weights, bias):
    out = [[0 for _ in range(nFilters)] for j in range((nInputs - kernelSize)//strides + 1)]
    for i in range((nInputs - kernelSize)//strides + 1):
        for j in range(nFilters):
            for k in range(kernelSize):
                for l in range(nChannels):
                    out[i][j] += float(input[i*strides + k][l])*float(weights[k][l][j])
            out[i][j] += float(bias[j])
            out[i][j] = str(out[i][j])
    return out

def Conv2DInt(nRows, nCols, nChannels, nFilters, kernelSize, strides, n, input, weights, bias):
    out = [[[0 for _ in range(nFilters)] for _ in range((nCols - kernelSize)//strides + 1)] for _ in range((nRows - kernelSize)//strides + 1)]
    for i in range((nRows - kernelSize)//strides + 1):
        for j in range((nCols - kernelSize)//strides + 1):
            for m in range(nFilters):
                for k in range(nChannels):
                    for x in range(kernelSize):
                        for y in range(kernelSize):
                            out[i][j][m] += float(input[i*strides+x][j*strides+y][k])*float(weights[x][y][k][m])
                out[i][j][m] += float(bias[m])
                out[i][j][m] = str(out[i][j][m])
    return out

def DenseInt(nInputs, nOutputs, n, input, weights, bias):
    out = [0 for _ in range(nOutputs)]
    for j in range(nOutputs):
        for i in range(nInputs):
            out[j] += float(input[i]) * float(weights[i][j])
        out[j] += float(bias[j])
        out[j] = str(out[j])
    return out

def GlobalAveragePooling2DInt(nRows, nCols, nChannels, input):
    out = [0 for _ in range(nChannels)]
    for k in range(nChannels):
        for i in range(nRows):
            for j in range(nCols):
                out[k] += float(input[i][j][k])
        out[k] = float(out[k] / (nRows * nCols))
    return out

def GlobalMaxPooling2DInt(nRows, nCols, nChannels, input):
    out = [max(float(input[i][j][k]) for i in range(nRows) for j in range(nCols)) for k in range(nChannels)]
    return out

def MaxPooling2DInt(nRows, nCols, nChannels, poolSize, strides, input):
    out = [[[str(max(float(input[i*strides + x][j*strides + y][k]) for x in range(poolSize) for y in range(poolSize))) for k in range(nChannels)] for j in range((nCols - poolSize) // strides + 1)] for i in range((nRows - poolSize) // strides + 1)]
    return out

def Flatten2DInt(nRows, nCols, nChannels, input):
    out = [str(float(input[i][j][k])) for i in range(nRows) for j in range(nCols) for k in range(nChannels)]
    return out

def ReLUInt(nRows, nCols, nChannels, input):
    out = [[[str(max(float(input[i][j][k]), 0)) for k in range(nChannels)] for j in range(nCols)] for i in range(nRows)]
    return out

def ArgMaxInt(input):
    return [input.index(str(max(int(input[i]) for i in range(len(input)))))]

def reshape_array(values_list, dimensions):
    total_size = 1
    for dim in dimensions:
        total_size *= dim
    assert len(values_list) == total_size, "Total size does not match the number of values"

    def helper(vals, dims):
        if len(dims) == 1:
            return vals[:dims[0]]
        else:
            step = len(vals) // dims[0]
            return [helper(vals[i*step:(i+1)*step], dims[1:]) for i in range(dims[0])]

    return helper(values_list, dimensions)
