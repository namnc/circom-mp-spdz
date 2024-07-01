nRows = 1
nCols = 1
nChannels = 1
n = 1000

list = [ { "name": "alice", "inputs": [], "outputs": [] }, { "name": "bob", "inputs": [], "outputs": [] } ]

in_arr = "0.in"
in_a = "0.a"
in_b = "0.b"
out = "0.out"
inlistdictlist = {}
inlistdictlist2 = {}

for i in range(nRows):
    for j in range(nCols):
        for k in range(nChannels):
            in_arr_txt = f"{in_arr}[{i}][{j}][{k}]"
            list[0]['inputs'].append(in_arr_txt);
            inlistdictlist[in_arr_txt] = i*j*k;

for i in range(nChannels):
    in_a_txt = f"{in_a}[{i}]"
    in_b_txt = f"{in_b}[{i}]"
    list[0]['inputs'].append(in_a_txt)
    list[1]['inputs'].append(in_b_txt)
    inlistdictlist[in_a_txt] = i
    inlistdictlist2[in_b_txt] = i

for i in range(nRows):
    for j in range(nCols):
        for k in range(nChannels):
            out_txt = f"{out}[{i}][{j}][{k}]"
            list[0]['outputs'].append(out_txt);
            list[1]['outputs'].append(out_txt);

import json
with open('mpc_settings.json', 'w') as fp:
    json.dump(list, fp)

with open('inputs_party_0.json', 'w') as fp:
    json.dump(inlistdictlist, fp)

with open('inputs_party_1.json', 'w') as fp:
    json.dump(inlistdictlist2, fp)