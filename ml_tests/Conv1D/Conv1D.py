import json

nInputs = 20
nChannels = 3
nFilters = 2
kernelSize = 4
strides = 3

intxt = "0.in"
weightstxt = "0.weights"
biastxt = "0.bias"
out = "0.out"
inlistdictlist = {}
inlistdictlist2 = {}

inputs_file_path = "conv1D_input.json"

with open(inputs_file_path, 'r') as file:
    inputs_dict = json.load(file)


list = [ { "name": "alice", "inputs": [], "outputs": [] }, { "name": "bob", "inputs": [], "outputs": [] } ]

for i in range(nInputs):
    for j in range(nChannels):
        txt = intxt + f"[{i}][{j}]"
        list[0]['inputs'].append(txt)
        inlistdictlist[txt] = inputs_dict["in"][i][j]

for i in range(kernelSize):
    for j in range(nChannels):
        for k in range(nFilters):
            txt = weightstxt + f"[{i}][{j}][{k}]"
            list[1]['inputs'].append(txt)
            inlistdictlist2[txt] = inputs_dict["weights"][i][j][k]

for i in range(nFilters):
    txt = biastxt + f"[{i}]"
    list[1]['inputs'].append(txt)
    inlistdictlist2[txt] = inputs_dict["bias"][i]

for i in range((nInputs - kernelSize) // strides + 1):
    for j in range(nFilters):
        outtxt = out + f"[{i}][{j}]"
        list[0]['outputs'].append(outtxt)
        list[1]['outputs'].append(outtxt)

with open('mpc_settings.json', 'w') as fp:
    json.dump(list, fp)

with open('inputs_party_0.json', 'w') as fp:
    json.dump(inlistdictlist, fp)

with open('inputs_party_1.json', 'w') as fp:
    json.dump(inlistdictlist2, fp)