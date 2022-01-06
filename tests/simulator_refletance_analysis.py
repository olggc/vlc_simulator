from math import ceil

import numpy as np
from matplotlib import pyplot as plt
from ambient import Ambient
from simulator import Simulator

for r in range(5, 6, 1):

    ambient_sets = {
        'ambient': {
            'room_sizes': {'x': 1, 'y': 1, 'z': 1},
            'floor_level': 0,
            'divisions_number': r,
            'sample_frequency': None,
            'walls_refletance': 0.2,
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
                {'x': 0.5, 'y': 0.5, 'z': 1}
            ],
            'ies_file_path': 'LEDblue.txt',
            'modulation_frequencies': [2000]
        },
        'sensor_position': {'x': 0, 'y': 0, 'z': 0}
    }
    ambient = Ambient(ambient_sets)
    simulator = Simulator(ambient)
    results = simulator.simulate()
    r = results[0]
    key_values = [(x, y) for x in r.keys() for y in r[x].keys()]
    result_simulator = np.array([r[point[0]][point[1]] for point in key_values])
#     x = [n + 1 for n in range(len(result_simulator))]
#     plt.plot(x, result_simulator)
#
# plt.xlabel('Plane Point')
# plt.ylabel('Iluminance')
# plt.show()

l = int(len(result_simulator) / 2)
r1 = result_simulator[:l]
r2 = result_simulator[l:]
r2 = r2[::-1]
dr = np.subtract(np.array(r1), np.array(r2))
x = [n + 1 for n in range(len(r1))]

l1 = plt.plot(x, dr)
plt.legend(['Erro'])
plt.xlabel('Plane Point')
plt.ylabel('Iluminance')
plt.show()
