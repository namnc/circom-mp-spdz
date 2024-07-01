nRows = 3
nCols = 4
nChannels = 5
nFilters = 3
n = 5

intxt = "0.in"
weightstxt = "0.weights"
biastxt = "0.bias"
out = "0.out"
inlistdictlist = {}
inlistdictlist2 = {}

list = [ { "name": "alice", "inputs": [], "outputs": [] }, { "name": "bob", "inputs": [], "outputs": [] } ]

for i in range(nRows):
    for j in range(nCols):
        for k in range(nChannels):
            txt = intxt + f"[{i}][{j}][{k}]"
            list[0]['inputs'].append(txt)
            inlistdictlist[txt] = i * j * k

for i in range(nChannels):
    for j in range(nFilters):
        txt = weightstxt + f"[{i}][{j}]"
        list[1]['inputs'].append(txt)
        inlistdictlist2[txt] = i * j

for i in range(nFilters):
    txt = weightstxt + f"[{i}]"
    list[1]['inputs'].append(txt)
    inlistdictlist2[txt] = i

for i in range(nRows):
    for j in range(nCols):
        for k in range(nFilters):
            outtxt = out + f"[{i}][{j}][{k}]"
            list[0]['outputs'].append(outtxt)
            list[1]['outputs'].append(outtxt)

import json
with open('mpc_settings.json', 'w') as fp:
    json.dump(list, fp)

with open('inputs_party_0.json', 'w') as fp:
    json.dump(inlistdictlist, fp)

with open('inputs_party_1.json', 'w') as fp:
    json.dump(inlistdictlist2, fp)