import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np
import json
from ambient import Ambient
from simulator import Simulator

ambient_sets = {
    'total_simulation_time': None,
    'ambient': {
        'room_sizes': {'x': 1, 'y': 1, 'z': 1},
        'floor_level': 0,
        'divisions_number': 4,
        'sample_frequency': 100000,
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
    'sensor': {'position': {'x': 0, 'y': 0, 'z': 0},
               'filter_parameter': {'filter_1': {'low_cut': 1500.0,
                                                 'high_cut': 2250.0,
                                                 'order': 5}}}
}

ambient = Ambient(ambient_sets)
simulator = Simulator(ambient)
results = simulator.simulate()

temporal_results = {x: {y: [] for y in results[0][0].keys()} for x in results[0].keys()}

for dt in results.keys():
    for x in results[dt].keys():
        for y in results[dt][x].keys():
            temporal_results[x][y].append(results[dt][x][y])

with open('temporal_results.json', 'w') as f:
    json.dump(temporal_results, f)