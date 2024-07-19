import json

nRows = 7
nCols = 7
nChannels = 3
nDepthFilters = 3
nPointFilters = 6
depthKernelSize = 3
strides = 1

intxt = "0.in"
depthWeightstxt = "0.depthWeights"
depthBiastxt = "0.depthBias"
depthOuttxt = "0.depthOut"
pointWeightstxt = "0.pointWeights"
pointBiastxt = "0.pointBias"
pointOut = "0.pointOut"
inlistdictlist = {}
inlistdictlist2 = {}

inputs_file_path = "separableConv2D_input.json"

with open(inputs_file_path, 'r') as file:
    inputs_dict = json.load(file)

list = [ { "name": "alice", "inputs": [], "outputs": [] }, { "name": "bob", "inputs": [], "outputs": [] } ]

for i in range(nRows):
    for j in range(nCols):
        for k in range(nChannels):
            txt = intxt + f"[{i}][{j}][{k}]"
            list[0]['inputs'].append(txt)
            inlistdictlist[txt] = inputs_dict["in"][i][j][k]

for i in range(depthKernelSize):
    for j in range(depthKernelSize):
        for k in range(nDepthFilters):
            txt = depthWeightstxt + f"[{i}][{j}][{k}]"
            list[1]['inputs'].append(txt)
            inlistdictlist2[txt] = inputs_dict["depthWeights"][i][j][k]

for i in range(nDepthFilters):
    txt = depthBiastxt + f"[{i}]"
    list[1]['inputs'].append(txt)
    inlistdictlist2[txt] = inputs_dict["depthBias"][i]

for i in range((nRows - depthKernelSize) // strides + 1):
    for j in range((nCols - depthKernelSize) // strides + 1):
        for k in range(nDepthFilters):
            txt = depthOuttxt + f"[{i}][{j}][{k}]"
            list[1]['inputs'].append(txt)
            inlistdictlist2[txt] = inputs_dict["depthOut"][i][j][k]

for i in range(nChannels):
    for j in range(nPointFilters):
        txt = pointWeightstxt + f"[{i}][{j}]"
        list[0]['inputs'].append(txt)
        inlistdictlist[txt] = inputs_dict["pointWeights"][i][j]

for i in range(nPointFilters):
    txt = pointBiastxt + f"[{i}]"
    list[0]['inputs'].append(txt)
    inlistdictlist[txt] = inputs_dict["pointBias"][i]

for i in range((nRows - depthKernelSize) // strides + 1):
    for j in range((nCols - depthKernelSize) // strides + 1):
        for k in range(nPointFilters):
            outtxt = pointOut + f"[{i}][{j}][{k}]"
            list[0]['outputs'].append(outtxt)
            list[1]['outputs'].append(outtxt)

with open('mpc_settings.json', 'w') as fp:
    json.dump(list, fp)

with open('inputs_party_0.json', 'w') as fp:
    json.dump(inlistdictlist, fp)

with open('inputs_party_1.json', 'w') as fp:
    json.dump(inlistdictlist2, fp)