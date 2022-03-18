from math import sqrt
from statistics import mean, stdev, median
from scipy.stats import norm, gamma
import numpy as np
from matplotlib import pyplot as plt
from ambient import Ambient
import seaborn as sb
from result_analysis.data_structure import prepare_data
from simulator import Simulator


def plotting_result(z_axis, divisions_numbers, result_from, graph_type='surface'):
    z_axis = np.array(z_axis).reshape(divisions_numbers, divisions_numbers)
    z_axis = z_axis.T
    if graph_type == 'heatmap':
        ax = sb.heatmap(z_axis)
        ax.invert_yaxis()
        ax.set_title(result_from + ' Iluminance[cd] Room Heatmap')
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
        ax.set_title(result_from + ' Iluminance[cd] Room Distribution')
        ax.set_xlabel('X points')
        ax.set_ylabel('Y points')
        ax.set_zlabel('Illuminance[cd]')
        fig.colorbar(surf, shrink=0.5, aspect=5)

        plt.show()


def get_results(data):
    ambient_sets = data['ambient_settings']
    dialux_results = data['dialux_results']
    relux_results = data['relux_results']
    num_div = ambient_sets['ambient']['divisions_number'] + 1
    a = int(sqrt(len(dialux_results)))
    dialux_results = np.array(dialux_results)
    dialux_results = dialux_results.reshape(a, a)
    dialux_results = dialux_results.T
    new_dia_lux_results = []
    for values in dialux_results:
        for value in values:
            new_dia_lux_results.append(value)
    dialux_results = new_dia_lux_results
    ambient = Ambient(ambient_sets)
    simulator = Simulator(ambient)
    results = simulator.simulate()
    simulator.plotting(0, graph_type='surface')
    simulator.plotting(0, graph_type='heatmap')
    plotting_result(dialux_results, num_div, 'Dialux', graph_type='surface')
    plotting_result(dialux_results, num_div, 'Dialux', graph_type='heatmap')
    plotting_result(relux_results, num_div, 'Relux', graph_type='surface')
    plotting_result(relux_results, num_div, 'Relux', graph_type='heatmap')
    r = results[0]  # resultado estático par a t = 0
    key_values = [(x, y) for x in r.keys() for y in r[x].keys()]
    res = [r[x][y] for x, y in key_values]
    result_simulator = np.array(res)
    dialux_results = np.array(dialux_results)
    # error dialux
    erro1_list = np.subtract(dialux_results, result_simulator)
    m_erro1 = [abs(e) / dialux_results[n] for n, e in enumerate(erro1_list)]
    mean_relative_error1 = mean(m_erro1)
    std_relative_error1 = stdev(m_erro1)
    median_relative_error1 = median(m_erro1)
    # erro relux
    erro2_list = np.subtract(relux_results, result_simulator)
    m_erro2 = [abs(e) / relux_results[n] for n, e in enumerate(erro2_list)]
    mean_relative_error2 = mean(m_erro2)
    std_relative_error2 = stdev(m_erro2)
    median_relative_error2 = median(m_erro2)
    g1 = plt.hist(m_erro1, bins=15, density=True, alpha=0.6, color='b')
    plt.title('Dialux - Relative Error Distribution')
    plt.xlabel('Relative Error [lx]')
    plt.ylabel('Frequency')
    plt.show()
    g2 = plt.hist(m_erro2, bins=15, density=True, alpha=0.6, color='b')
    plt.title('Relux - Relative Error Distribution')
    plt.xlabel('Relative Error [cd]')
    plt.ylabel('Frequency')
    plt.show()
    x = [n + 1 for n in range(len(result_simulator))]
    sqrt_x = int(sqrt(len(x)))
    vec_ones = np.ones(len(x))
    l1 = plt.plot(x, res)
    l2 = plt.plot(x, dialux_results)
    l3 = plt.plot(x, relux_results)
    # l2 = plt.plot(x, median_relative_error * vec_ones)
    plt.title('Relative Error')
    plt.xlabel('Plane Point')
    plt.ylabel('Iluminance[lx]')
    plt.legend(['Simulator', 'Dialux', 'Relux'])
    plt.show()
    print(f'\n\nResults Dialux \n\n'
          f'Mean Relative Error: {mean_relative_error1} \n'
          f'Standard Deviation Relative Errror: {std_relative_error1} \n'
          f'Median Relative Error: {median_relative_error1} \n'
          f'Max Relative Error: {max(m_erro1)}')

    print(f'\n\nResults Relux \n\n'
          f'Mean Relative Error: {mean_relative_error2} \n'
          f'Standard Deviation Relative Errror: {std_relative_error2} \n'
          f'Median Relative Error: {median_relative_error2} \n'
          f'Max Relative Error: {max(m_erro1)}')

    fig1, ax1 = plt.subplots(subplot_kw={"projection": "3d"})
    abs_erro1 = np.array([abs(e) for e in erro1_list])
    E1 = abs_erro1.reshape(sqrt_x, sqrt_x)
    X1 = np.arange(0, sqrt_x, 1)
    Y1 = np.arange(0, sqrt_x, 1)
    X1, Y1 = np.meshgrid(X1, Y1)
    surf1 = ax1.plot_surface(X1, Y1, E1, cmap='viridis',
                           linewidth=0, antialiased=False)
    fig1.colorbar(surf1, shrink=0.5, aspect=5)
    ax1.set_title('Dialux - Mean Relative Error Distribution')
    ax1.set_xlabel('X points')
    ax1.set_xlabel('Y points')
    plt.show()

    fig2, ax2 = plt.subplots(subplot_kw={"projection": "3d"})
    abs_erro2 = np.array([abs(e) for e in erro2_list])
    E2 = abs_erro2.reshape(sqrt_x, sqrt_x)
    X2 = np.arange(0, sqrt_x, 1)
    Y2 = np.arange(0, sqrt_x, 1)
    X2, Y2 = np.meshgrid(X2, Y2)
    surf2 = ax2.plot_surface(X2, Y2, E2, cmap='viridis',
                           linewidth=0, antialiased=False)
    fig2.colorbar(surf2, shrink=0.5, aspect=5)
    ax2.set_title('Relux - Mean Relative Error Distribution')
    ax2.set_xlabel('X points')
    ax2.set_xlabel('Y points')
    plt.show()


if __name__ == '__main__':
    amb_id = 'amb2ai2'
    d = prepare_data(amb_id)
    get_results(d)
