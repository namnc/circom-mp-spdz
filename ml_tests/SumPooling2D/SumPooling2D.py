
nRows = 7
nCols = 11
nChannels = 5
poolSize = 3
strides = 2

list = [ { "name": "alice", "inputs": [], "outputs": [] }, { "name": "bob", "inputs": [], "outputs": [] } ]

intxt = "0.in"
outtxt = "0.out"
inlistdictlist = {}
inlistdictlist2 = {}

for i in range(nRows):
    for j in range(nCols):
        for k in range(nChannels):
            inops = f"{intxt}[{i}][{j}][{k}]"
            list[0]['inputs'].append(inops);
            inlistdictlist[inops] = i*j*k;

for i in range((nRows-poolSize)//strides+1):
    for j in range((nCols-poolSize)//strides+1):
        for k in range(nChannels):
            outops = f"{outtxt}[{i}][{j}][{k}]"
            list[0]['outputs'].append(outops)
            list[1]['outputs'].append(outops)

import json
with open('mpc_settings.json', 'w') as fp:
    json.dump(list, fp)

with open('inputs_party_0.json', 'w') as fp:
    json.dump(inlistdictlist, fp)

with open('inputs_party_1.json', 'w') as fp:
    json.dump(inlistdictlist2, fp)

#in[nRows][nCols][nChannels];
#out[(nRows-poolSize)\strides+1][(nCols-poolSize)\strides+1][nChannels];