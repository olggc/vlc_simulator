from math import sqrt
from statistics import mean

import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np
import json
from ambient import Ambient
from simulator import Simulator

dialux_results_data_path = 'data/dialux_data.json'
with open(dialux_results_data_path, 'r') as fp:
    dialux_data_dict = json.load(fp)

main_key = 'ambient_10x10_1lamppeq_3x3x3'

dialux_data = dialux_data_dict[main_key]

dialux_results = []
for key in dialux_data.keys():
    dialux_results.append(dialux_data[key])

x = [n + 1 for n in range(len(dialux_results[0]))]
# l1 = plt.plot(x, dialux_results[0])
# l2 = plt.plot(x, dialux_results[1])
# l3 = plt.plot(x, dialux_results[2])
# plt.legend(['DiaLux 0%', 'DiaLux 30%', 'DiaLux 70%'])
# plt.xlabel('Plane Point')
# plt.ylabel('Iluminance')
# plt.show()

results_data_path = '/home/olange/PycharmProjects/vlc_simulator/tests/data/temporal_results_10x10_1lampped_3x3x3_0.json'
with open(results_data_path, 'r') as fp:
    result1 = json.load(fp)

r = result1  # resultado estático par a t = 0
key_values = [(x, y) for x in r.keys() for y in r[x].keys()]
res1 = [round(r[point[0]][point[1]][0]) for point in key_values]
result_simulator1 = np.array(res1)

results_data_path = '/home/olange/PycharmProjects/vlc_simulator/tests/data/temporal_results_10x10_1lamped_3x3x3_1.json'
with open(results_data_path, 'r') as fp:
    result2 = json.load(fp)

r = result2  # resultado estático par a t = 0
key_values = [(x, y) for x in r.keys() for y in r[x].keys()]
res2 = [round(r[point[0]][point[1]][0]) for point in key_values]
result_simulator2 = np.array(res2)

results_data_path = '/home/olange/PycharmProjects/vlc_simulator/tests/data/temporal_results_10x10_1lamped_3x3x3_2.json'
with open(results_data_path, 'r') as fp:
    result3 = json.load(fp)

r = result3  # resultado estático par a t = 0
key_values = [(x, y) for x in r.keys() for y in r[x].keys()]
res3 = [round(r[point[0]][point[1]][0]) for point in key_values]
result_simulator3 = np.array(res3)
n = np.ones(len(x))
s1 = plt.plot(x, mean(dialux_results[0] / result_simulator1) * n)
s2 = plt.plot(x, mean(dialux_results[1] / result_simulator2) * n)
s3 = plt.plot(x, mean(dialux_results[2] / result_simulator3) * n)
plt.legend(['Sim 0%', 'Sim 30%', 'Sim 70%'])
plt.xlabel('Plane Point')
plt.ylabel('Iluminance')
plt.show()
