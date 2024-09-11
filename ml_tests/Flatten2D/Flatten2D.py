import json
import random

nRows = 5
nCols = 5
nChannels = 3

intxt = "0.in"
out = "0.out"
inlistdictlist = {}
inlistdictlist2 = {}

inputs_file_path = "flatten2D_input.json"

array_3d = [[[random.randint(0, 100) for _ in range(nChannels)] for _ in range(nCols)] for _ in range(nRows)]
flattened = [elem for row in array_3d for col in row for elem in col]

output = {
    "in": array_3d,
    "out": flattened
}

with open(inputs_file_path, 'w') as f:
    json.dump(output, f, indent=2)

with open(inputs_file_path, 'r') as file:
    inputs_dict = json.load(file)

list = [ { "name": "alice", "inputs": [], "outputs": [] }, { "name": "bob", "inputs": [], "outputs": [] } ]

for i in range(nRows):
    for j in range(nCols):
        for k in range(nChannels):
            txt = intxt + f"[{i}][{j}][{k}]"
            list[0]['inputs'].append(txt)
            inlistdictlist[txt] = inputs_dict["in"][i][j][k]

for i in range(nRows * nCols * nChannels):
    outtxt = out + f"[{i}]"
    list[0]['outputs'].append(outtxt)
    list[1]['outputs'].append(outtxt)

with open('mpc_settings.json', 'w') as fp:
    json.dump(list, fp)

with open('inputs_party_0.json', 'w') as fp:
    json.dump(inlistdictlist, fp)

with open('inputs_party_1.json', 'w') as fp:
    json.dump(inlistdictlist2, fp)