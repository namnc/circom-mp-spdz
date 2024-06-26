# -*- coding: utf-8 -*-
"""naive_search.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1vU3qtkYyHlHF_1UFmtfZir76Aq_3HcSs
"""

in1txt = "0.in1";
in2txt = "0.in2";
outtxt = "0.out";

N = 1000;

list = [ { "name": "alice", "inputs": [], "outputs": [outtxt] }, { "name": "bob", "inputs": [in2txt], "outputs": [outtxt] } ]
in1dict = {};
in2dict = {in2txt: 10};
for i in range(N):
  in1ops = in1txt + "["+ str(i) + "]";
  list[0]['inputs'].append(in1ops);
  in1dict[in1ops] = i;

# print(list);
# print(in1dict);
# print(in2dict);

import json
with open('mpc_settings.json', 'w') as fp:
    json.dump(list, fp)

with open('inputs_party_0.json', 'w') as fp:
    json.dump(in1dict, fp)

with open('inputs_party_1.json', 'w') as fp:
    json.dump(in2dict, fp)

raw = """
def naive_search(n):
	# hardcoded "secret" list from Alice - in a real application this should be a private input
	a = [sint(i) for i in range(n)]
	print_ln("Waiting for search input from Bob")
	b = sint.get_input_from(1)

	eq_bits = [x == b for x in a]
	b_in_a = sum(eq_bits)
	print_ln("Is b in Alice's list? %s", b_in_a.reveal())

naive_search(1000)
""";

with open('raw_circuit.mpc', 'w') as fp:
    fp.write(raw);