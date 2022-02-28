from math import sqrt
from statistics import mean, stdev, median
from scipy.stats import norm, gamma
import numpy as np
from matplotlib import pyplot as plt
from ambient import Ambient
import seaborn as sb
from result_analysis.data_structure import data_ex
from simulator import Simulator


def plotting_dialux(z_axis, divisions_numbers, graph_type='surface'):
    z_axis = np.array(z_axis).reshape(divisions_numbers, divisions_numbers)
    z_axis = z_axis.T
    if graph_type == 'heatmap':
        ax = sb.heatmap(z_axis)
        ax.invert_yaxis()
        ax.set_title('Dialux Iluminance[cd] Room Heatmap')
        ax.set_xlabel('X points')
        ax.set_ylabel('Y points')
        plt.show()
    if graph_type == 'surface':
        fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
        n = len(z_axis[0])
        X = np.arange(0, n, 1)
        Y = np.arange(0, n, 1)
        X, Y = np.meshgrid(X, Y)
        surf = ax.plot_surface(X, Y, z_axis, cmap='viridis',
                               edgecolor='none',
                               linewidth=0, antialiased=False)
        ax.set_title('Dialux Iluminance[cd] Room Distribution')
        ax.set_xlabel('X points')
        ax.set_ylabel('Y points')
        ax.set_zlabel('Illuminance[cd]')
        fig.colorbar(surf, shrink=0.5, aspect=5)

        plt.show()


def get_results(data):
    ambient_sets = data['ambient_settings']
    dialux_results = data['dialux_results']
    num_div = ambient_sets['ambient']['divisions_number'] + 1

    ambient = Ambient(ambient_sets)
    simulator = Simulator(ambient)
    results = simulator.simulate()
    simulator.plotting(0, graph_type='surface')
    simulator.plotting(0, graph_type='heatmap')
    plotting_dialux(dialux_results, num_div, graph_type='surface')
    plotting_dialux(dialux_results, num_div, graph_type='heatmap')
    r = results[0]  # resultado estático par a t = 0
    key_values = [(x, y) for x in r.keys() for y in r[x].keys()]
    res = [r[x][y] for x, y in key_values]
    result_simulator = np.array(res)
    erro1_list = np.subtract(dialux_results, result_simulator)
    m_erro1 = [abs(e) / dialux_results[n] for n, e in enumerate(erro1_list)]
    mean_relative_error = mean(m_erro1)
    std_relative_error = stdev(m_erro1)
    median_relative_error = median(m_erro1)
    g1 = plt.hist(m_erro1, bins=15, density=True, alpha=0.6, color='b')
    plt.title('Relative Error Distribution')
    plt.xlabel('Relative Error [cd]')
    plt.ylabel('Frequency')
    plt.show()
    x = [n + 1 for n in range(len(result_simulator))]
    sqrt_x = int(sqrt(len(x)))
    vec_ones = np.ones(len(x))
    l1 = plt.plot(x, m_erro1)
    l2 = plt.plot(x, mean_relative_error * vec_ones)
    l2 = plt.plot(x, median_relative_error * vec_ones)
    plt.title('Relative Error')
    plt.xlabel('Plane Point')
    plt.ylabel('Iluminance[cd]')
    plt.legend(['Relative Error Curve', 'Mean Relative Error', 'Median Relative Error'])
    plt.show()
    print(f'Mean Relative Error: {mean_relative_error} \n'
          f'Standard Deviation Relative Errror: {std_relative_error} \n'
          f'Median Relative Error: {median_relative_error} \n'
          f'Max Relative Error: {max(m_erro1)}')

    fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
    abs_erro = np.array([abs(e) for e in erro1_list])
    E = abs_erro.reshape(sqrt_x, sqrt_x)
    X = np.arange(0, sqrt_x, 1)
    Y = np.arange(0, sqrt_x, 1)
    X, Y = np.meshgrid(X, Y)
    surf = ax.plot_surface(X, Y, E, cmap='viridis',
                           linewidth=0, antialiased=False)
    fig.colorbar(surf, shrink=0.5, aspect=5)
    ax.set_title('Mean Relative Error Distribution')
    ax.set_xlabel('X points')
    ax.set_xlabel('Y points')
    plt.show()


if __name__ == '__main__':
    d = data_ex
    get_results(d)
