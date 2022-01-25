import json
from math import sqrt
from statistics import mean

import numpy as np
import matplotlib.pyplot as plt
from numpy.core import std
from sklearn.metrics import accuracy_score, mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.multioutput import MultiOutputRegressor
from sklearn.neural_network import MLPRegressor

filename = 'output.json'
with open(filename, 'r') as fp:
    data = json.load(fp)
filename = 'temporal_results.json'
with open(filename, 'r') as fp:
    plane = json.load(fp)

matrix_data = []
for f_id in data.keys():
    matrix_data.append(data[f_id])

matrix_data = np.array(matrix_data)
matrix_data = matrix_data.T
expected_output = [[100 * float(x), 100 * float(y)] for x in plane.keys() for y in plane[x].keys()]

x_train1, x_test1, y_train1, y_test1 = train_test_split(matrix_data, expected_output, train_size=0.85, test_size=0.15,
                                                        random_state=0)
min_errors = []
for bach_size in range(5, 25, 5):
    print(f'BACH SIZE: {bach_size}')
    errors = []
    for n in range(10, 120, 10):
        print(f'Neurons: {n}')
        mlpr = MultiOutputRegressor(MLPRegressor(hidden_layer_sizes=n, activation='logistic',
                                                 solver='adam', batch_size=10, learning_rate='adaptive',
                                                 early_stopping=True,
                                                 validation_fraction=0.15))
        mlpr.fit(x_train1, y_train1)
        ymlpr = mlpr.predict(x_test1)
        mae_mlpr = mean_absolute_error(y_test1, ymlpr)
        mse_mlpr = mean_squared_error(y_test1, ymlpr)
        r2s_mlpr = r2_score(y_test1, ymlpr)
        distance_error = np.subtract(y_test1, ymlpr)
        distance_error = [sqrt((point[0] ** 2) + (point[1] ** 2)) for point in distance_error]
        max_distance_error = max(distance_error)
        std_distance_error = std(distance_error)
        mean_distance_error = mean(distance_error)
        errors.append(mean_distance_error)
        print("Mean Absolute Error: ", mae_mlpr)
        print("Mean Squared Error: ", mse_mlpr)
        print("R2 score: ", r2s_mlpr)
        print(f"Mean Distance Error: {mean_distance_error}, Std: {std_distance_error}")
        print("Max Distance Error: ", max_distance_error)
        # plt.plot([i for i in range(len(distance_error))], distance_error)
        # plt.show()

    plt.plot([k for k in range(10, 120, 10)], errors)
    min_errors.append(min(errors))
    plt.show()

plt.plot([b for b in range(5, 25, 5)], min_errors)
plt.show()
