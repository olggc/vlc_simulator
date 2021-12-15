from math import floor

from matplotlib import pyplot as plt
import numpy as np

results_dialux = np.array([12, 15, 16, 15, 14,
                           14, 15, 15, 18, 16,
                           15, 17, 18, 18, 17,
                           15, 18, 19, 18, 16,
                           12, 14, 16, 15, 14])
result_simulad = np.array([13.52, 15.88, 16.62, 15.99, 15.21,
                           15.12, 17.21, 18.34, 17.86, 17.04,
                           15.92, 17.91, 18.95, 18.56, 17.87,
                           15.14, 17.42, 18.62, 17.73, 17.02,
                           13.57, 15.44, 15.94, 15.98, 15.49])

round_result = [floor(r) for r in result_simulad]
erro1 = np.subtract(results_dialux, result_simulad)
erro1 = [abs(e) / results_dialux[n] for n, e in enumerate(erro1)]
erro1 = sum(erro1) / len(erro1)
erro2 = np.subtract(results_dialux, round_result)
erro2 = [abs(e) / results_dialux[n] for n, e in enumerate(erro2)]
erro2 = sum(erro2) / len(erro2)
x = [n + 1 for n in range(len(result_simulad))]

plt.plot(x, results_dialux)
plt.plot(x, result_simulad)
plt.xlabel('Plane Point')
plt.ylabel('Iluminance')
plt.show()
