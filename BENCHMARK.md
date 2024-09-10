| Circuit | Time (without latency, on one machine) | One region (rate 5gb, latency 2ms) | Different regions (rate 2.5gb, latency 60ms) |
| --- | --- | --- | --- |
| DepthwiseConv2D | 9.121985 | 5.907890 | 42.709400 |
| GlobalMaxPooling2D | 0.215514 | 2.742590 | 33.824400 |
| BatchNormalization2D | 8.982086 | 5.862440 | 42.442000 |
| Conv1D | 1.567994 | 2.577810 | 24.699200 |
| ArgMax | 0.149328 | 1.351420 | 16.475400 |
| Conv2D | 2.317575 | 2.867000 | 26.225900 |
| Dense | 1.445482 | 2.452500 | 24.366000 |
| AveragePooling2D | 0.160485 | 0.888444 | 10.180900 |
| SumPooling2D | 0.104244 | 0.012256 | 0.152150 |
| GlobalAveragePooling2D | 0.186116 | 1.333930 | 15.093700 |
| SeparableConv2D | 27.892814 | 14.543400 | 97.868000 |
| ReLU | 0.245169 | 2.434900 | 26.685700 |
| Flatten2D | 0.153417 | 0.013079 | 0.155441 |
| MaxPooling2D | 0.183715 | 1.330040 | 16.130300 |
| PointwiseConv2D | 17.278185 | 10.273400 | 71.872700 |


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
