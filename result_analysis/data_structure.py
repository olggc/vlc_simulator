"""
    Data structure file to all types of ambients sets
"""

## EXAMPLE AMBIENTE DATA
data_ex = {
    'ambient_settings': {
        'total_simulation_time': None,  # None para simulação estática
        'ambient': {
            'room_sizes': {'x': 3, 'y': 3, 'z': 3},  # comprimento, largura e alture
            'floor_level': 0,  # altura do chão
            'divisions_number': 9,  # numero de divisões ex: para 10 x 10 a simulação deve ter 9 divisões
            'sample_frequency': 100000,  # frequencia da simulação
            'walls_refletance': 0.0,  # refletancia das paredes
            'refletance_aperture': None,  # abertura da reflexão pode ser limitada
            'walls': [  # planos das paredes
                {'x': 0},
                {'x': 3},
                {'y': 0},
                {'y': 3}
            ]
        },
        'luminaries': {
            'positions': [  # posição das luminárias um dict para cada posição
                {'x': 3 * 0.5, 'y': 3 * 0.5, 'z': 3 * 1}
            ],
            'ies_file_path': 'LampPeq.txt',  # arquivo ies da lampada
            'modulation_frequencies': [2000]  # frequencias de cada luminária
        },
        'sensor': {'position': {'x': 0, 'y': 0, 'z': 0},  # posição inicial do sensor
                   'filter_parameter': {'filter_1': {'low_cut': 1500.0,
                                                     'high_cut': 2250.0,
                                                     'order': 5}}}  # parametros do filtro do sensor
    },  # configurações do ambient
    'dialux_results': [19, 22, 24, 26, 27, 27, 26, 25, 22, 20,
                       22, 25, 28, 30, 32, 32, 31, 28, 26, 22,
                       24, 28, 31, 34, 36, 36, 34, 32, 28, 25,
                       26, 30, 34, 37, 39, 39, 37, 34, 31, 27,
                       26, 31, 35, 38, 40, 40, 39, 36, 32, 28,
                       26, 31, 35, 38, 40, 40, 39, 36, 32, 27,
                       25, 30, 34, 37, 38, 38, 37, 34, 30, 26,
                       24, 27, 31, 34, 35, 35, 34, 31, 28, 24,
                       21, 25, 27, 30, 31, 31, 30, 28, 25, 22,
                       19, 21, 24, 25, 26, 27, 26, 25, 22, 19]  # resultados do dialux
}


## abm1ai relux

data_amb1air = {
    'ambient_settings': {
        'total_simulation_time': None,  # None para simulação estática
        'ambient': {
            'room_sizes': {'x': 5, 'y': 2, 'z': 3},  # comprimento, largura e alture
            'floor_level': 0,  # altura do chão
            'divisions_number': 9,  # numero de divisões ex: para 10 x 10 a simulação deve ter 9 divisões
            'sample_frequency': 100000,  # frequencia da simulação
            'walls_refletance': 0.0,  # refletancia das paredes
            'refletance_aperture': None,  # abertura da reflexão pode ser limitada
            'walls': [  # planos das paredes
                {'x': 0},
                {'x': 3},
                {'y': 0},
                {'y': 3}
            ]
        },
        'luminaries': {
            'positions': [  # posição das luminárias um dict para cada posição
                {'x': 3 * 0.5, 'y': 3 * 0.5, 'z': 3 * 1}
            ],
            'ies_file_path': 'LampPeq.txt',  # arquivo ies da lampada
            'modulation_frequencies': [2000]  # frequencias de cada luminária
        },
        'sensor': {'position': {'x': 0, 'y': 0, 'z': 0},  # posição inicial do sensor
                   'filter_parameter': {'filter_1': {'low_cut': 1500.0,
                                                     'high_cut': 2250.0,
                                                     'order': 5}}}  # parametros do filtro do sensor
    },
}