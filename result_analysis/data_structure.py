import json
from math import sqrt

import pandas as pd
import numpy as np

"""
    Data structure file to all types of ambients sets
"""
scale_factor_x = 4
scale_factor_y = 4
scale_factor_z = 2.5

amb1ai0 = {
    'total_simulation_time': None,
    'ambient': {
        'room_sizes': {'x': scale_factor_x * 1, 'y': scale_factor_y * 1, 'z': scale_factor_z * 1},
        'floor_level': 0,
        'divisions_number': 9,
        'sample_frequency': 120000,
        'walls_refletance': 0.0,
        'refletance_aperture': None,
        'walls': [
            {'x': 0},
            {'x': scale_factor_x * 1},
            {'y': 0},
            {'y': scale_factor_y * 1}
        ]
    },
    'luminaries': {
        'positions': [
            {'x': scale_factor_x * 0.24, 'y': scale_factor_y * 0.74, 'z': scale_factor_z * 1},
            {'x': scale_factor_x * 0.49, 'y': scale_factor_y * 0.24, 'z': scale_factor_z * 1},
            {'x': scale_factor_x * 0.74, 'y': scale_factor_y * 0.74, 'z': scale_factor_z * 1}
        ],
        'ies_file_path': 'LampPeq.txt',
        'modulation_frequencies': [2000, 3000, 4000]
    },
    'sensor': {'position': {'x': 0, 'y': 0, 'z': 0},
               'filter_parameter': {'filter_1': {'low_cut': 1500.0,
                                                 'high_cut': 2250.0,
                                                 'order': 5}}}
}


def prepare_data(amb_id: str):
    amb_relux = amb_id + '.xlsx'
    data1 = pd.read_excel(amb_relux, header=None)
    raw_relux_data = data1.to_numpy()
    raw_relux_data_transposte = raw_relux_data.T
    relux_data = []
    for values in raw_relux_data_transposte:
        for value in reversed(values):
            relux_data.append(value)

    with open('new_dialux_data.json', 'r') as fp:
        raw_dialux_data = json.load(fp)

    amb_key = amb_id[:len(amb_id) - 1]
    amb_num = amb_id[len(amb_id) - 1:len(amb_id)]
    dialux_data = raw_dialux_data[amb_key][amb_num]

    prepared_data_dict = {
        'ambient_settings': amb1ai0,
        'dialux_results': dialux_data,
        'relux_results': relux_data
    }
    return prepared_data_dict
