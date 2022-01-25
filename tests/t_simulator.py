import numpy as np
from matplotlib import pyplot as plt
import json
from ambient import Ambient
from simulator import Simulator

## DADOS
with open('dialux_data.json', 'r') as fp:
    dialux_data_dict = json.load(fp)

refletance_to_id_converter = {str(int(k) / 10): k for k in dialux_data_dict.keys()}
ambient_sets = {
    'total_simulation_time': None,
    'ambient': {
        'room_sizes': {'x': 1, 'y': 1, 'z': 1},
        'floor_level': 0,
        'divisions_number': 4,
        'sample_frequency': 100000,
        'walls_refletance': 0.0,
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
id = str(refletance_to_id_converter[str(ambient_sets['ambient']['walls_refletance'])])
dialux_results = dialux_data_dict[id]
ambient = Ambient(ambient_sets)
simulator = Simulator(ambient)
results = simulator.simulate()

# simulator.animate()  ## descomentar para ver 'heatmap' animation

r = results[0]
key_values = [(x, y) for x in r.keys() for y in r[x].keys()]
result_simulator = np.array([round(r[point[0]][point[1]]) for point in key_values])
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
print('erro: ', erro1)

## descomentar para regerar os resultados temporais
# temporal_results = {x: {y: [] for y in results[0][0].keys()} for x in results[0].keys()}
#
# for dt in results.keys():
#     for x in results[dt].keys():
#         for y in results[dt][x].keys():
#             temporal_results[x][y].append(results[dt][x][y])
#
# with open('temporal_results.json', 'w') as f:
#     json.dump(temporal_results, f)
