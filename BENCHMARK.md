| Circuit | Fast LAN (rate 10gb, latency 0.25ms) | LAN (rate 1gb, latency 1ms) | WAN (rate 100mb, latency 50ms) |
| --- | --- | --- | --- |
| DepthwiseConv2D | 4.508590 | 5.333890 | 40.752400 |
| GlobalMaxPooling2D | 1.580060 | 2.121270 | 34.043500 |
| BatchNormalization2D | 4.517530 | 5.289740 | 39.124600 |
| Conv1D | 1.499740 | 1.970370 | 27.505500 |
| ArgMax | 0.727750 | 1.143670 | 18.592200 |
| Conv2D | 1.929560 | 2.499890 | 29.358900 |
| Dense | 1.552070 | 2.187230 | 27.990800 |
| AveragePooling2D | 0.477079 | 0.724241 | 11.612400 |
| SumPooling2D | 0.005776 | 0.007228 | 0.174216 |
| GlobalAveragePooling2D | 0.812070 | 1.236330 | 17.276700 |
| SeparableConv2D | 11.701600 | 12.948200 | 90.974200 |
| ReLU | 1.696460 | 2.404690 | 30.424000 |
| Flatten2D | 0.004507 | 0.007012 | 0.174841 |
| MaxPooling2D | 0.707512 | 1.182670 | 18.457000 |
| PointwiseConv2D | 8.216470 | 9.359570 | 68.186700 |


| Circuit | Data sent (MB) | Rounds | Global data sent (MB) |
| --- | --- | --- | --- |
| DepthwiseConv2D | 66.2456 | 1014 | 132.561 |
| GlobalMaxPooling2D | 0.737164 | 983 | 1.48662 |
| BatchNormalization2D | 63.1446 | 1003 | 126.359 |
| Conv1D | 13.1792 | 647 | 26.3749 |
| ArgMax | 0.270383 | 500 | 0.548958 |
| Conv2D | 19.3392 | 682 | 38.6988 |
| Dense | 12.0876 | 658 | 24.1916 |
| AveragePooling2D | 0.27011 | 327 | 0.548412 |
| SumPooling2D | 0.029897 | 34 | 0.059794 |
| GlobalAveragePooling2D | 0.349556 | 503 | 0.707304 |
| SeparableConv2D | 192.085 | 1947 | 384.371 |
| ReLU | 0.651317 | 890 | 1.31083 |
| Flatten2D | 0.031913 | 34 | 0.063826 |
| MaxPooling2D | 0.440606 | 493 | 0.889404 |
| PointwiseConv2D | 129.147 | 1464 | 258.428 |
