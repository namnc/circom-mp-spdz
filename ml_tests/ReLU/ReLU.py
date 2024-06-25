import random

n = 5

intxt = "0.in"
out = "0.out"

list = [ { "name": "alice", "inputs": [intxt], "outputs": [out] }, { "name": "bob", "inputs": [], "outputs": [out] } ]

import json
with open('mpc_settings.json', 'w') as fp:
    json.dump(list, fp)

with open('inputs_party_0.json', 'w') as fp:
    json.dump({"0.in": random.randint(1, 100)}, fp)

with open('inputs_party_1.json', 'w') as fp:
    json.dump({}, fp)