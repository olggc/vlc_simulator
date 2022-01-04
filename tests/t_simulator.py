from math import floor

import numpy as np
from matplotlib import pyplot as plt
from ambient import Ambient
from simulator import Simulator

ambient_sets = {
    'ambient': {
        'room_sizes': {'x': 1, 'y': 1, 'z': 1},
        'floor_level': 0,
        'divisions_number': 4,
        'sample_frequency': None,
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
        'ies_file_path': 'LampPeq.txt',
        'modulation_frequencies': [2000, 3000, 4000]
    },
    'sensor_position': {'x': 0, 'y': 0, 'z': 0}
}
ambient_sets_10 = {
    'ambient': {
        'room_sizes': {'x': 1, 'y': 1, 'z': 1},
        'floor_level': 0,
        'divisions_number': 4,
        'sample_frequency': None,
        'walls_refletance': 0.1,
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
ambient_sets_20 = {
    'ambient': {
        'room_sizes': {'x': 1, 'y': 1, 'z': 1},
        'floor_level': 0.2,
        'divisions_number': 4,
        'sample_frequency': None,
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
simulator = Simulator(ambient.luminaries, ambient.floor, ambient.walls, ambient.sensor, None, ambient)
results = simulator.simulate()
results_dialux = np.array([12, 14, 15, 14, 12,
                           15, 17, 17, 17, 14,
                           16, 18, 19, 18, 16,
                           15, 18, 19, 18, 15,
                           14, 16, 17, 16, 14])
results_dialux_10 = np.array([13, 15, 16, 15, 13,
                           15, 18, 18, 18, 15,
                           17, 19, 20, 19, 17,
                           16, 19, 20, 19, 16,
                           15, 17, 18, 17, 15])
results_dialux_20 = np.array([14, 16, 17, 16, 14,
                           16, 19, 20, 19, 16,
                           18, 21, 21, 21, 18,
                           17, 20, 21, 20, 17,
                           16, 18, 19, 18, 16])
r = results[0]
key_values = [(x, y) for x in r.keys() for y in r[x].keys()]
result_simulator = np.array([round(r[point[0]][point[1]]) for point in key_values])

erro1 = np.subtract(results_dialux_20, result_simulator)
m_erro1 = [abs(e) / results_dialux[n] for n, e in enumerate(erro1)]
erro1 = sum(m_erro1) / len(erro1)
x = [n + 1 for n in range(len(result_simulator))]

plt.plot(x, results_dialux_20)
plt.plot(x, result_simulator)
plt.xlabel('Plane Point')
plt.ylabel('Iluminance')
plt.show()