from math import sqrt

import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np
import json
from ambient import Ambient
from simulator import Simulator

## DADOS
with open('data/dialux_data.json', 'r') as fp:
    dialux_data_dict = json.load(fp)

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
ambient_data = 'ambient_10x10_lamppeq_3x3x3'
id = '0'
dialux_results = dialux_data_dict[id]

## SIMULAÇÃO
ambient = Ambient(ambient_sets)
simulator = Simulator(ambient)
results = simulator.simulate()

# simulator.animate()  ## descomentar para ver 'heatmap' animation

# comparação ponto a ponto
r = results[0]  # resultado estático par a t = 0
key_values = [(x, y) for x in r.keys() for y in r[x].keys()]
result_simulator = np.array([r[point[0]][point[1]] for point in key_values])
erro1_list = np.subtract(dialux_results, result_simulator)
m_erro1 = [abs(e) / dialux_results[n] for n, e in enumerate(erro1_list)]
erro1 = sum(m_erro1) / len(erro1_list)
x = [n + 1 for n in range(len(result_simulator))]
sqrt_x = int(sqrt(len(x)))


l1 = plt.plot(x, dialux_results)
l2 = plt.plot(x, result_simulator)
plt.legend(['DiaLux', 'Simulator'])
plt.xlabel('Plane Point')
plt.ylabel('Iluminance')
plt.show()
print('erro: ', erro1)

fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
abs_erro = np.array([abs(e) for e in erro1_list])
E = abs_erro.reshape(sqrt_x, sqrt_x)
X = np.arange(0, 5, 1)
Y = np.arange(0, 5, 1)
X, Y = np.meshgrid(X, Y)
surf = ax.plot_surface(X, Y, E, cmap=cm.coolwarm,
                       linewidth=0, antialiased=False)
fig.colorbar(surf, shrink=0.5, aspect=5)

plt.show()

