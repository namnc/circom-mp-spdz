import json
from ml_tests.util import GlobalAveragePooling2DInt

def main():
    with open('ml_tests/GlobalAveragePooling2D/globalAveragePooling2D_input.json', 'r') as f:
        data = json.load(f)

    input_data = data['in_unchanged']
    real_output = data['out']

    for i in range(len(real_output)):
        real_output[i] = float(real_output[i])
        real_output[i] /= 2**10
        
    correct_output = GlobalAveragePooling2DInt(5, 5, 3, input_data)

    print(f"Correct output: {correct_output}")
    print(f"Real output: {real_output}")

if __name__ == "__main__":
    main()