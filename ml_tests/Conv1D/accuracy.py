import json
from ml_tests.util import Conv1DInt

def main():
    with open('ml_tests/Conv1D/Conv1D_input.json', 'r') as f:
        data = json.load(f)

    input_data = data['in_unchanged']
    weights = data['weights_unchanged']
    bias = data['bias_unchanged']
    real_output = data['out']

    for i in range(len(real_output)):
        for j in range(len(real_output[i])):
            real_output[i][j] = float(real_output[i][j])
            real_output[i][j] /= 2**10
        
    correct_output = Conv1DInt(20, 3, 2, 4, 3, 10, input_data, weights, bias)

    print(f"Correct output: {correct_output}")
    print(f"Real output: {real_output}")

if __name__ == "__main__":
    main()