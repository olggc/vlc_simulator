from math import sqrt
from statistics import mean, stdev, median

from ambient import Ambient
from result_analysis.data_structure import prepare_data
import matplotlib.pyplot as plt
import seaborn as sb
from matplotlib import cm
import numpy as np
import json
import pandas as pd

from simulator import Simulator

if __name__ == '__main__':

    scale_factor_x = 4
    scale_factor_y = 4
    scale_factor_z = 2.5
    amb_ids = ['ramb1ci0', 'ramb1ci1', 'ramb1ci2']
    sob_plot_pos = [(321, 322), (323, 324), (325, 326)]
    # fig1, ax1 = plt.subplots()
    # fig2, ax2 = plt.subplots()
    # ax1 = fig1.add_subplot(1, 3, 1, projection='3d')
    l = []
    erros1 = []
    erros2 = []
    for n, refletance in enumerate([0.0, 0.3, 0.7]):
        if refletance in {}:
            continue
        # fig1 = plt.figure(figsize=(12, 3), dpi=80)
        # fig1.subplots_adjust(wspace=0.2, hspace=0)
        pos_a, pos_b = sob_plot_pos[n]
        amb_sets = {
            'total_simulation_time': None,
            'ambient': {
                'room_sizes': {'x': scale_factor_x * 1, 'y': scale_factor_y * 1, 'z': scale_factor_z * 1},
                'floor_level': 0,
                'divisions_number': 9,
                'sample_frequency': 120000,
                'walls_refletance': refletance,
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
                'modulation_frequencies': [2000, 3000, 4000, 5000]
            },
            'sensor': {'position': {'x': 0, 'y': 0, 'z': 0},
                       'filter_parameter': {'filter_1': {'low_cut': 1500.0,
                                                         'high_cut': 2250.0,
                                                         'order': 5}}}
        }
        ambient = Ambient(amb_sets)
        simulator = Simulator(ambient)
        results = simulator.simulate()
        # Z = simulator.f(0)
        # dx = len(Z[0])
        # X = np.arange(0, 1, 1 / dx)
        # Y = np.arange(0, 1, 1 / dx)
        # X, Y = np.meshgrid(X, Y)
        # row, col, pos = (1, 3, 1)
        # ax1 = fig1.add_subplot(row, col, pos, projection='3d')
        # surf1 = ax1.plot_surface(X, Y, Z, cmap='viridis',
        #                        edgecolor='none',
        #                        linewidth=0, antialiased=False)
        # ax1.set_title(f'Simulador - Reflexão = {round(refletance * 100)} %')
        # ax1.set_xlabel('x')
        # ax1.set_ylabel('y')
        # ax1.set_zlabel('Lux')
        # fig1.colorbar(surf1, shrink=0.5, aspect=5)
        results_from_relux = prepare_data(amb_ids[n])
        # relux_results = results_from_relux['relux_results']
        # divisions_numbers = int(sqrt(len(relux_results)))
        # z_axis = np.array(relux_results).reshape(divisions_numbers, divisions_numbers)
        # z_axis = z_axis.T
        # Z = []
        # for values in z:
        #     for value in reversed(values):
        #         Z.append(value)
        # z = np.array(Z).reshape(divisions_numbers, divisions_numbers)
        # row, col, pos = (1, 3, 2)
        # ax1 = fig1.add_subplot(row, col, pos, projection='3d')
        # surf2 = ax1.plot_surface(X, Y, z_axis, cmap='viridis',
        #                        edgecolor='none',
        #                        linewidth=0, antialiased=False)
        # ax1.set_title(f'Relux - Reflexão = {round(refletance * 100)} %')
        # ax1.set_xlabel('x')
        # ax1.set_ylabel('y')
        # ax1.set_zlabel('Lux')
        # fig1.colorbar(surf2, shrink=0.5, aspect=5)
        dialux_results = results_from_relux['dialux_results']
        relux_results = results_from_relux['relux_results']
        divisions_numbers = int(sqrt(len(dialux_results)))
        z_axis = np.array(dialux_results).reshape(divisions_numbers, divisions_numbers)
        z_axis = z_axis.T
        Z = []
        for z in reversed(z_axis):
            Z.append(z)
        z_axis = np.array(Z)
        # Z = []
        # for values in z_axis:
        #     for value in values:
        #         Z.append(value)
        # z_axis = np.array(Z).reshape(divisions_numbers, divisions_numbers)
        # row, col, pos = (1, 3, 3)
        # ax1 = fig1.add_subplot(row, col, pos, projection='3d')
        # surf3 = ax1.plot_surface(X, Y, z_axis, cmap='viridis',
        #                         edgecolor='none',
        #                         linewidth=0, antialiased=False)
        # ax1.set_title(f'Dialux - Reflexão = {round(refletance * 100)} %')
        # ax1.set_xlabel('x')
        # ax1.set_ylabel('y')
        # ax1.set_zlabel('Lux')
        # # fig1.colorbar(surf3, shrink=0.5, aspect=5)
        # fig1.tight_layout()
        # plt.show()

        r = results[0]  # resultado estático par a t = 0
        key_values = [(x, y) for x in r.keys() for y in r[x].keys()]
        res = [r[x][y] for x, y in key_values]
        dialux_results = []
        for v in z_axis:
            for vi in list(v):
                dialux_results.append(vi)
        result_simulator = np.array(res)
        # dialux_results.reverse()
        # relux_results.reverse()
        erro1_list = np.subtract(relux_results, result_simulator)
        erro2_list = np.subtract(dialux_results, result_simulator)
        m_erro1 = [abs(e) / relux_results[n] for n, e in enumerate(erro1_list)]
        m_erro2 = [abs(e) / dialux_results[n] for n, e in enumerate(erro2_list)]
        mean_relative_error1 = mean(m_erro1)
        mean_relative_error2 = mean(m_erro2)
        print(f'RELUX - ERRO MÉDIO: {mean_relative_error1}')
        print(f'DIALUX - ERRO MÉDIO: {mean_relative_error2}')
        erros1.append(mean_relative_error1)
        erros2.append(mean_relative_error2)
        x = [n + 1 for n in range(len(result_simulator))]
        plt.plot(x, dialux_results)
        plt.plot(x, result_simulator)
        plt.legend(['Dialux', 'Simulador'])
        plt.axis('square')
        plt.show()
        plt.plot(x, relux_results)
        plt.plot(x, result_simulator)
        plt.legend(['Relux', 'Simulador'])
        plt.axis('square')
        plt.show()
        # plt.subplot(pos_b)
    #     sb.histplot(m_erro2, bins=10, stat='percent', color='g')
    #     plt.title('Distribuição do Erro Relativo')
    #     plt.xlabel('Erro Relativo [lux]')
    #     plt.ylabel('Freq.[%]')
    #     plt.axis('tight')
    #     plt.grid(True)
    #     plt.subplot(pos_a)
    #     x = [n + 1 for n in range(len(result_simulator))]
    #     l1 = plt.plot(x, res)
    #     l2 = plt.plot(x, dialux_results)
    #     l.append(l1)
    #     l.append(l2)
    #     plt.title(f'Iluminância - Reflexão {round(refletance * 100)} %')
    #     plt.xlabel('Pontos no plano de referência')
    #     plt.ylabel('Lux')
    #     if n == 0:
    #         plt.legend(['SIMULADOR', 'DIALUX'], loc='upper right', prop={'size': 6})
    #     plt.axis('tight')
    #     plt.grid(True)
    #
    # fig2.tight_layout()
    # fig1.tight_layout()
    # plt.show()

    for m, e in enumerate(erros1):
        print(f'Relux - Erro {m} : {e}')

    for m, e in enumerate(erros2):
        print(f'Dialux - Erro {m} : {e}')
