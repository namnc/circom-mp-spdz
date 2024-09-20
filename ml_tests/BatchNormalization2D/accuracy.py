import json
from ml_tests.util import BatchNormalizationInt

def main():
    with open('ml_tests/BatchNormalization2D/batchNormalization_input.json', 'r') as f:
        data = json.load(f)

    input_data = data['in_unchanged']
    a = data['a_unchanged']
    b = data['b_unchanged']
    real_output = data['out']

    for i in range(len(real_output)):
        for j in range(len(real_output[i])):
            for k in range(len(real_output[i][j])):
                real_output[i][j][k] = float(real_output[i][j][k])
                real_output[i][j][k] /= 2**10
        
    correct_output = BatchNormalizationInt(5, 5, 3, 10, input_data, a, b)

    print(f"Correct output: {correct_output}")
    print(f"Real output: {real_output}")

if __name__ == "__main__":
    main()