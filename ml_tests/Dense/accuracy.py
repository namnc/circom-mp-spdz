import json
from ml_tests.util import DenseInt

def main():
    with open('ml_tests/Dense/dense_input.json', 'r') as f:
        data = json.load(f)

    input_data = data['in_unchanged']
    weights = data['weights_unchanged']
    bias = data['bias_unchanged']
    real_output = data['out']

    for i in range(len(real_output)):
        print(float(real_output[i]))
        real_output[i] = float(real_output[i])
        real_output[i] /= 2**10
        
    correct_output = DenseInt(20, 10, 10, input_data, weights, bias)

    print(f"Correct output: {correct_output}")
    print(f"Real output: {real_output}")

if __name__ == "__main__":
    main()