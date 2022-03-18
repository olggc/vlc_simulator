import json
from math import sqrt

import pandas as pd
import numpy as np

"""
    Data structure file to all types of ambients sets
"""

amb1ai0 = {
    'total_simulation_time': None,  # None para simulação estática
    'ambient': {
        'room_sizes': {'x': 5, 'y': 2, 'z': 2.5},  # comprimento, largura e alture
        'floor_level': 0,  # altura do chão
        'divisions_number': 9,  # numero de divisões ex: para 10 x 10 a simulação deve ter 9 divisões
        'sample_frequency': 100000,  # frequencia da simulação
        'walls_refletance': 0.7,  # refletancia das paredes
        'refletance_aperture': None,  # abertura da reflexão pode ser limitada
        'walls': [  # planos das paredes
            {'x': 0},
            {'x': 5},
            {'y': 0},
            {'y': 2}
        ]
    },
    'luminaries': {
        'positions': [  # posição das luminárias um dict para cada posição
            {'x': 5 * 0.5, 'y': 2 * 0.5, 'z': 1 * 2.5}
        ],
        'ies_file_path': 'LampPeq.txt',  # arquivo ies da lampada
        'modulation_frequencies': [2000]  # frequencias de cada luminária
    },
    'sensor': {'position': {'x': 0, 'y': 0, 'z': 0},  # posição inicial do sensor
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
