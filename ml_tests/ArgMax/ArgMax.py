n = 5

intxt = "0.in"
out = "0.out"
inlistdictlist = {}
inlistdictlist2 = {}

list = [ { "name": "alice", "inputs": [], "outputs": [out] }, { "name": "bob", "inputs": [], "outputs": [out] } ]

for i in range(n):
    txt = intxt + f"[{i}]"
    list[0]['inputs'].append(txt)
    inlistdictlist[txt] = i

import json
with open('mpc_settings.json', 'w') as fp:
    json.dump(list, fp)

with open('inputs_party_0.json', 'w') as fp:
    json.dump(inlistdictlist, fp)

with open('inputs_party_1.json', 'w') as fp:
    json.dump(inlistdictlist2, fp)