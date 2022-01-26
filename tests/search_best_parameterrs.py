import json
from math import sqrt
from statistics import mean

import numpy as np
import matplotlib.pyplot as plt
from numpy.core import std
from sklearn.metrics import accuracy_score, mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.multioutput import MultiOutputRegressor
from sklearn.neural_network import MLPRegressor

filename = 'data/output.json'
with open(filename, 'r') as fp:
    data = json.load(fp)
filename = 'data/temporal_results.json'
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
param3 = {'estimator__activation': 'logistic', 'estimator__batch_size': 20, 'estimator__early_stopping': True,
          'estimator__hidden_layer_sizes': 180, 'estimator__learning_rate': 'adaptive',
          'estimator__n_iter_no_change': 40, 'estimator__solver': 'adam', 'estimator__validation_fraction': 0.2}
# param1 = {'activation': 'logistic', 'batch_size': 20, 'early_stopping': True, 'hidden_layer_sizes': (140,),
#           'learning_rate': 'adaptive', 'n_iter_no_change': 40, 'solver': 'adam', 'validation_fraction': 0.15}
# param2 = {'activation': 'logistic', 'batch_size': 10, 'early_stopping': True, 'hidden_layer_sizes': (11, 11),
#           'learning_rate': 'adaptive', 'n_iter_no_change': 40, 'solver': 'adam', 'validation_fraction': 0.15}
# mlp = MultiOutputRegressor(MLPRegressor(max_iter=1000))
# print(mlp.get_params().keys())
# params = mlp.get_params().keys()
# param_grid = {
#     'hidden_layer_sizes': [180],
#     'activation': ['logistic'],
#     'batch_size': [20],
#     'learning_rate': ['adaptive'],
#     'n_iter_no_change': [40],
#     'solver': ['adam'],
#     'early_stopping': [True],
#     'validation_fraction': [0.2],
#     'learning_rate_init': [0.001],
#     'verbose': [True]}
#

# param_grid2 = {}
# for key in param_grid.keys():
#     new_key = 'estimator__' + str(key)
#     param_grid2[new_key] = param_grid[key]
#
# searcher = GridSearchCV(mlp, param_grid2, cv=5, scoring='neg_mean_absolute_error', verbose=True, n_jobs=-1)
#
# grid_result = searcher.fit(x_train1, y_train1)
#
# best_params = grid_result.best_params_
# print(best_params)
mlpr = MultiOutputRegressor(MLPRegressor(max_iter=1000, batch_size=20, early_stopping=True, hidden_layer_sizes=180,
                                         learning_rate='adaptive', n_iter_no_change=40, solver='adam',
                                         validation_fraction=0.2,learning_rate_init=0.001))
# mlpr = MLPRegressor(max_iter=1000, batch_size=20, early_stopping=True, hidden_layer_sizes=140,
#                                          learning_rate='adaptive', n_iter_no_change=40, solver='adam',
#                                          validation_fraction=0.15)
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
print("Mean Absolute Error: ", mae_mlpr)
print("Mean Squared Error: ", mse_mlpr)
print("R2 score: ", r2s_mlpr)
print(f"Mean Distance Error: {mean_distance_error}, Std: {std_distance_error}")
print("Max Distance Error: ", max_distance_error)

y = mlpr.predict(x_test1[0].reshape(1, -1))
print(f'\n Predicted: {y}, Real: {y_test1[0]}')
