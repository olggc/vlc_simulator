import numpy as np
from matplotlib import pyplot as plt
from ambient import Ambient
from simulator import Simulator

ambient_sets = {
    'ambient': {
        'room_sizes': {'x': 1, 'y': 1, 'z': 1},
        'floor_level': 0,
        'divisions_number': 4,
        'sample_frequency': 100000,
        'walls_refletance': 0.5,
        'refletance_aperture': None,
        'walls': [
            {'x': 0},
            {'x': 1},
            {'y': 0},
            {'y': 1}
        ]
    },
    'luminaries': {
        'positions': [
            {'x': 0.49, 'y': 0.24, 'z': 1},
            {'x': 0.24, 'y': 0.74, 'z': 1},
            {'x': 0.74, 'y': 0.74, 'z': 1}
        ],
        'ies_file_path': 'LEDblue.txt',
        'modulation_frequencies': [2000, 3000, 4000]
    },
    'sensor_position': {'x': 0, 'y': 0, 'z': 0}
}
ambient = Ambient(ambient_sets)
simulator = Simulator(ambient)
results = simulator.simulate()
# simulator.animate()

results_dialux = np.array([12, 15, 16, 15, 14,
                           14, 17, 18, 18, 16,
                           15, 17, 19, 19, 17,
                           14, 17, 18, 18, 16,
                           12, 14, 16, 15, 14])

results_dialux_10 = np.array([13, 15, 17, 16, 15,
                              15, 18, 19, 19, 17,
                              16, 18, 20, 20, 18,
                              15, 18, 19, 19, 17,
                              13, 15, 17, 16, 15])

results_dialux_20 = np.array([14, 16, 18, 17, 16,
                              16, 19, 21, 20, 18,
                              17, 20, 21, 21, 19,
                              16, 19, 21, 20, 18,
                              14, 16, 18, 17, 16])

results_dialux_30 = np.array([15, 18, 19, 19, 17,
                              17, 20, 22, 21, 19,
                              18, 21, 23, 23, 20,
                              17, 20, 22, 21, 19,
                              15, 17, 19, 18, 15])

results_dialux_40 = np.array([16, 19, 20, 20, 18,
                              19, 22, 24, 23, 20,
                              19, 23, 25, 24, 22,
                              18, 22, 24, 23, 21,
                              16, 19, 20, 20, 18])

results_dialux_50 = np.array([18, 21, 22, 22, 19,
                              20, 23, 26, 25, 22,
                              21, 25, 27, 26, 23,
                              20, 24, 25, 25, 22,
                              17, 20, 22, 21, 19])

results_dialux_60 = np.array([19, 23, 24, 24, 21,
                              22, 26, 28, 27, 24,
                              23, 27, 29, 29, 25,
                              22, 26, 28, 27, 24,
                              19, 22, 24, 23, 21])

results_dialux_70 = np.array([22, 25, 27, 26, 23,
                              25, 28, 31, 30, 26,
                              25, 30, 32, 31, 28,
                              25, 29, 31, 30, 27,
                              22, 25, 27, 26, 23])

results_dialux_80 = np.array([24, 28, 30, 29, 26,
                              28, 32, 34, 33, 30,
                              28, 33, 35, 35, 31,
                              28, 32, 34, 34, 30,
                              25, 28, 30, 29, 26])

results_dialux_90 = np.array([28, 32, 34, 33, 30,
                              32, 36, 39, 38, 34,
                              32, 37, 40, 39, 35,
                              32, 36, 39, 38, 34,
                              28, 32, 34, 33, 30])
r = results[0]
key_values = [(x, y) for x in r.keys() for y in r[x].keys()]
result_simulator = np.array([round(r[point[0]][point[1]]) for point in key_values])
dialux_results = results_dialux_60
erro1 = np.subtract(dialux_results, result_simulator)
m_erro1 = [abs(e) / dialux_results[n] for n, e in enumerate(erro1)]
erro1 = sum(m_erro1) / len(erro1)
x = [n + 1 for n in range(len(result_simulator))]

l1 = plt.plot(x, dialux_results)
l2 = plt.plot(x, result_simulator)
plt.legend(['DiaLux', 'Simulator'])
plt.xlabel('Plane Point')
plt.ylabel('Iluminance')
plt.show()

# temporal_iluminance_in_point = [results[dt][0.5][0.5] for dt in results.keys()]
# time = [dt for dt in results.keys()]
# plt.scatter(time, temporal_iluminance_in_point)
# plt.show()
# x = 1
