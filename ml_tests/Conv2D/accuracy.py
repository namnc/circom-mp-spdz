import json
from ml_tests.util import Conv2DInt

def main():
    with open('ml_tests/Conv2D/Conv2D_input.json', 'r') as f:
        data = json.load(f)

    input_data = data['in_unchanged']
    weights = data['weights_unchanged']
    bias = data['bias_unchanged']
    real_output = data['out']

    for i in range(len(real_output)):
        for j in range(len(real_output[i])):
            for k in range(len(real_output[i][j])):
                real_output[i][j][k] = float(real_output[i][j][k])
                real_output[i][j][k] /= 2**10
        
    correct_output = Conv2DInt(5, 5, 3, 2, 3, 1, 10, input_data, weights, bias)

    print(f"Correct output: {correct_output}")
    print(f"Real output: {real_output}")

if __name__ == "__main__":
    main()