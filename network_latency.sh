#!/bin/bash

tc qdisc add dev eth0 root handle 1:0 netem delay 50ms
tc qdisc add dev eth0 parent 1:1 handle 10:0 tbf rate 100kbit burst 1kb limit 10kb
