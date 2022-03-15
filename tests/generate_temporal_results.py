import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np
import json
from ambient import Ambient
from simulator import Simulator

scale_factor = 4

data_dir = 'data/'
filename = 'temporal_results.json'

ambient_sets = {
    'total_simulation_time': 0.024,
    'ambient': {
        'room_sizes': {'x': scale_factor * 1, 'y': scale_factor * 1, 'z': scale_factor * 1},
        'floor_level': 0,
        'divisions_number': 9,
        'sample_frequency': 120000,
        'walls_refletance': 0.0,
        'refletance_aperture': None,
        'walls': [
            {'x': 0},
            {'x': scale_factor * 1},
            {'y': 0},
            {'y': scale_factor * 1}
        ]
    },
    'luminaries': {
        'positions': [
            {'x': scale_factor * 0.49, 'y': scale_factor * 0.24, 'z': scale_factor * 1},
            {'x': scale_factor * 0.24, 'y': scale_factor * 0.74, 'z': scale_factor * 1},
            {'x': scale_factor * 0.74, 'y': scale_factor * 0.74, 'z': scale_factor * 1}
        ],
        'ies_file_path': data_dir + 'LampPeq.txt',
        'modulation_frequencies': [2000, 3000, 4000]
    },
    'sensor': {'position': {'x': 0, 'y': 0, 'z': 0},
               'filter_parameter': {'filter_1': {'low_cut': 1500.0,
                                                 'high_cut': 2250.0,
                                                 'order': 5}}}
}

ambient = Ambient(ambient_sets)
simulator = Simulator(ambient)
results = simulator.simulate()
simulator.plotting(0)

temporal_results = {x: {y: [] for y in results[0][0].keys()} for x in results[0].keys()}

for dt in results.keys():
    for x in results[dt].keys():
        for y in results[dt][x].keys():
            temporal_results[x][y].append(results[dt][x][y])

with open(data_dir + filename, 'w') as f:
    json.dump(temporal_results, f)
