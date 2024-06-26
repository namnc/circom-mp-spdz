m = 3
n = 4
p = 5

in_a = "0.a"
in_b = "0.b"
out = "0.out"
inlistdictlist = {}
inlistdictlist2 = {}

list = [ { "name": "alice", "inputs": [], "outputs": [] }, { "name": "bob", "inputs": [], "outputs": [] } ]

for i in range(m):
    for j in range(n):
        in_a_txt = f"{in_a}[{i}][{j}]"
        list[0]['inputs'].append(in_a_txt)
        inlistdictlist[in_a_txt] = (i * n) + j

for i in range(n):
    for j in range(p):
        in_b_txt = f"{in_b}[{i}][{j}]"
        list[1]['inputs'].append(in_b_txt)
        inlistdictlist2[in_b_txt] = (i * p) + j

for i in range(m):
    for j in range(p):
        out_txt = f"{out}[{i}][{j}]"
        list[0]['outputs'].append(out_txt)
        list[1]['outputs'].append(out_txt)

import json
with open('mpc_settings.json', 'w') as fp:
    json.dump(list, fp)

with open('inputs_party_0.json', 'w') as fp:
    json.dump(inlistdictlist, fp)

with open('inputs_party_1.json', 'w') as fp:
    json.dump(inlistdictlist2, fp)