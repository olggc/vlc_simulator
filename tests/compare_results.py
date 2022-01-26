from math import sqrt
from statistics import mean

import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np
import json
from ambient import Ambient
from simulator import Simulator

## DADOS
dialux_results_data_path = 'data/dialux_data.json'
with open(dialux_results_data_path, 'r') as fp:
    dialux_data_dict = json.load(fp)

simulation_results_data_path = 'data/temporal_results.json'
with open(simulation_results_data_path, 'r') as fp:
    simulation_results = json.load(fp)

# CARREGA DADOS DO DIALUX PARA AMBIENTE SELECIONADO
ambient_dialux_data = 'ambient_10x10_lamppeq_3x3x3'
id = '1'
dialux_results = np.array(dialux_data_dict[ambient_dialux_data][id])

r = simulation_results  # resultado estático par a t = 0
key_values = [(x, y) for x in r.keys() for y in r[x].keys()]
res = [round(r[point[0]][point[1]][0]) for point in key_values]
result_simulator = np.array(res)
erro1_list = np.subtract(dialux_results, result_simulator)
erro_medio = mean(erro1_list)
m_erro1 = [abs(e) / dialux_results[n] for n, e in enumerate(erro1_list)]
erro1 = sum(m_erro1) / len(erro1_list)
x = [n + 1 for n in range(len(result_simulator))]
sqrt_x = int(sqrt(len(x)))

l1 = plt.plot(x, dialux_results)
l2 = plt.plot(x, result_simulator)
l3 = plt.plot(x, result_simulator + erro_medio)
plt.legend(['DiaLux','Simulator + Erro médio' ,'Simulator'])
plt.xlabel('Plane Point')
plt.ylabel('Iluminance')
plt.show()
print('erro: ', erro1)

fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
abs_erro = np.array([abs(e) for e in erro1_list])
E = abs_erro.reshape(sqrt_x, sqrt_x)
X = np.arange(0, sqrt_x, 1)
Y = np.arange(0, sqrt_x, 1)
X, Y = np.meshgrid(X, Y)
surf = ax.plot_surface(X, Y, E, cmap=cm.coolwarm,
                       linewidth=0, antialiased=False)
fig.colorbar(surf, shrink=0.5, aspect=5)

plt.show()
