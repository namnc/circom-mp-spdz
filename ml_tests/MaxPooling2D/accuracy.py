import json
from ml_tests.util import MaxPooling2DInt

def main():
    with open('ml_tests/MaxPooling2D/maxPooling2d_input.json', 'r') as f:
        data = json.load(f)

    input_data = data['in_unchanged']
    real_output = data['out']

    for i in range(len(real_output)):
        for j in range(len(real_output[i])):
            for k in range(len(real_output[i][j])):
                real_output[i][j][k] = float(real_output[i][j][k])
                real_output[i][j][k] /= 2**10
        
    correct_output = MaxPooling2DInt(5, 5, 3, 2, 2, input_data)

    print(f"Correct output: {correct_output}")
    print(f"Real output: {real_output}")

if __name__ == "__main__":
    main()