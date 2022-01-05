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
        'walls_refletance': 0,
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
r = results[0]
key_values = [(x, y) for x in r.keys() for y in r[x].keys()]
result_simulator = np.array([round(r[point[0]][point[1]]) for point in key_values])
dialux_results = results_dialux
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
