nInputs = 3
nOutputs = 4
n = 10**5

intxt = "0.in"
weightstxt = "0.weights"
biastxt = "0.bias"
remaindertxt = "0.reminder"
out = "0.out"
inlistdictlist = {}
inlistdictlist2 = {}

list = [ { "name": "alice", "inputs": [], "outputs": [] }, { "name": "bob", "inputs": [], "outputs": [] } ]

for i in range(nInputs):
    txt = intxt + f"[{i}]"
    list[0]['inputs'].append(txt)
    inlistdictlist[txt] = i

for i in range(nInputs):
    for j in range(nOutputs):
        txt = weightstxt + f"[{i}][{j}]"
        list[0]['inputs'].append(txt)
        inlistdictlist[txt] = i * j

for i in range(nOutputs):
    txt = biastxt + f"[{i}]"
    list[1]['inputs'].append(txt)
    inlistdictlist2[txt] = i

    txt = remaindertxt + f"[{i}]"
    list[1]['inputs'].append(txt)
    inlistdictlist2[txt] = i

for i in range(nOutputs):
    outtxt = out + f"[{i}]"
    list[0]['outputs'].append(outtxt)
    list[1]['outputs'].append(outtxt)

import json
with open('mpc_settings.json', 'w') as fp:
    json.dump(list, fp)

with open('inputs_party_0.json', 'w') as fp:
    json.dump(inlistdictlist, fp)

with open('inputs_party_1.json', 'w') as fp:
    json.dump(inlistdictlist2, fp)