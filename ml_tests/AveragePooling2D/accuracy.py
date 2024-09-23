import json
from ml_tests.util import AveragePooling2DInt

def main():
    with open('ml_tests/AveragePooling2D/averagePooling2D_input.json', 'r') as f:
        data = json.load(f)

    input_data = data['in_unchanged']
    real_output = data['out']

    for i in range(len(real_output)):
        for j in range(len(real_output[i])):
            for k in range(len(real_output[i][j])):
                print(float(real_output[i][j][k]))
                real_output[i][j][k] = float(real_output[i][j][k])
                real_output[i][j][k] /= 2**10
        
    correct_output = AveragePooling2DInt(5, 5, 3, 2, 2, input_data)

    print(f"Correct output: {correct_output}")
    print(f"Real output: {real_output}")

if __name__ == "__main__":
    main()