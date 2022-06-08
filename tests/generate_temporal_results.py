import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np
import json
import pandas as pd
import seaborn as sb
from ambient import Ambient
from simulator import Simulator

scale_factor_x = 4
scale_factor_y = 4
scale_factor_z = 2.5
data_dir = 'data/'
filename = 'temporal_results.json'
times = [0.0, 0.0005, 0.00235, 0.00025, 0.00022500000000000002, 0.00015000000000000001, 0.00250, 5e-05]
total_time = max(times)
ambient_sets = {
    'total_simulation_time': None,
    'ambient': {
        'room_sizes': {'x': 11.85, 'y': 2, 'z': 2.5},
        'floor_level': 0,
        'divisions_number': 20,
        'sample_frequency': 120000,
        'walls_refletance': 0.7,
        'refletance_aperture': None,
        'walls': [
            {'x': 0},
            {'x': 11.85},
            {'y': 0},
            {'y': 2}
        ]
    },
    'luminaries': {
        'positions': [
            {'x': 1.06, 'y': 0.65, 'z': 3, 'ies_file_path': data_dir + 'avantDownlight.txt'},
            {'x': 1.06, 'y': 1.35, 'z': 3, 'ies_file_path': data_dir + 'slimG2.txt'},
            {'x': 2.48, 'y': 1.00, 'z': 3, 'ies_file_path': data_dir + 'LampPeq.txt'},
            {'x': 3.96, 'y': 0.65, 'z': 3, 'ies_file_path': data_dir + 'slimG2.txt'},
            {'x': 3.96, 'y': 1.35, 'z': 3, 'ies_file_path': data_dir + 'slimG2.txt'},
            {'x': 7.19, 'y': 0.65, 'z': 3, 'ies_file_path': data_dir + 'slimG2.txt'},
            {'x': 7.19, 'y': 1.35, 'z': 3, 'ies_file_path': data_dir + 'slimG2.txt'},
            {'x': 8.61, 'y': 1.00, 'z': 3, 'ies_file_path': data_dir + 'LampPeq.txt'},
            {'x': 10.09, 'y': 0.65, 'z': 3, 'ies_file_path': data_dir + 'slimG2.txt'},
            {'x': 10.09, 'y': 1.35, 'z': 3, 'ies_file_path': data_dir + 'slimG2.txt'}
        ],
        'modulation_frequencies': [2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000, 11000],
        'luminarie_aperture': 110
    },
    'sensor': {'position': {'x': 0, 'y': 0, 'z': 0},
               'filter_parameter': {'filter_1': {'low_cut': 1500.0,
                                                 'high_cut': 2250.0,
                                                 'order': 5}}}
}

ambient = Ambient(ambient_sets)
simulator = Simulator(ambient)
results = simulator.simulate()
simulator.plotting(0, 'surface')

temporal_results = {x: {y: [] for y in results[0.0][0.2222222222222222].keys()} for x in results[0.0].keys()}

for dt in results.keys():
    for x in results[dt].keys():
        for y in results[dt][x].keys():
            temporal_results[x][y].append(results[dt][x][y])

with open(data_dir + filename, 'w') as f:
    json.dump(temporal_results, f)


# time_instants = [1 / 8000]
# time_instants = [key for key in results.keys()]
# for time_instant in time_instants:
#     # times_diff = [abs(float(t) - time_instant) for t in results.keys()]
#     # min_index, _ = min([(idx, diff) for idx, diff in enumerate(times_diff)], key=lambda i: i[1])
#     # current_time = times[min_index]
#     simulator.plotting(time_instant, graph_type='heatmap')

# times = sorted(times)
# sob_plot_pos = [421, 422, 423, 424, 425, 426, 427, 428]
# fig, ax = plt.subplots(figsize=(8, 10), dpi=80)
# for l, time in enumerate(times):
#     plot_pos = sob_plot_pos[l]
#     z_axis = simulator.f(time)
#     x_axis = [0.4, 0.8, 1.2, 1.6, 2.0, 2.4, 2.8, 3.2, 3.6, 4.0]
#     y_axis = [0.4, 0.8, 1.2, 1.6, 2.0, 2.4, 2.8, 3.2, 3.6, 4.0]
#     df_cm = pd.DataFrame(z_axis, index=x_axis, columns=y_axis)
#     z_values = simulator.f(time, with_numpy=False)
#     plt.subplot(plot_pos)
#     sb.heatmap(df_cm, cbar_kws={'label': 'Iluminância[lux]'})
#     plt.ylim(min(z_values), max(z_values))
#     plt.xlim(min(z_values), max(z_values))
#     plt.title(f't = {round(time * 100000)} us')
#     plt.xlabel('X')
#     plt.ylabel('Y')
#     plt.axis('tight')
# fig.tight_layout()
# plt.show()