import json
import pickle
from datetime import time, date
from math import sqrt, pi, sin, cos
from random import randint
from statistics import mean, stdev

import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score, mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.multioutput import MultiOutputRegressor
from sklearn.neural_network import MLPRegressor


def predict_with_nn(nn, positions, plane, iluminance_data):
    predicted = []
    for x1, y1, th in positions:
        dist1 = sqrt(x1 * x1 + y1 * y1)
        dist2 = [sqrt(x2 * x2 + y2 * y2) / 100 for x2, y2 in plane]
        min_dist, i = min([(abs(d - dist1), k) for k, d in enumerate(dist2)], key=lambda v: v[0])
        ilu = iluminance_data[i]
        pos = nn.predict(ilu.reshape(1, -1))
        predicted.append(pos * 0.01)
    return predicted


def train_net(train, save_with_pickle, load_from_pickle):
    filename = 'data/output_100x100_lampeq.json'
    with open(filename, 'r') as fp:
        data = json.load(fp)
    filename = 'data/temporal_results_100x100_lampeq.json'
    with open(filename, 'r') as fp:
        plane = json.load(fp)

    matrix_data = []
    for f_id in data.keys():
        matrix_data.append(data[f_id])

    matrix_data = np.array(matrix_data)
    matrix_data = matrix_data.T
    expected_output = [[100 * float(x), 100 * float(y)] for x in plane.keys() for y in plane[x].keys()]
    x_train1, x_test1, y_train1, y_test1 = train_test_split(matrix_data, expected_output, train_size=0.85,
                                                            test_size=0.15,
                                                            random_state=0)
    if train:
        param3 = {'estimator__activation': 'logistic', 'estimator__batch_size': 20, 'estimator__early_stopping': True,
                  'estimator__hidden_layer_sizes': 180, 'estimator__learning_rate': 'adaptive',
                  'estimator__n_iter_no_change': 40, 'estimator__solver': 'adam', 'estimator__validation_fraction': 0.2}

        mlpr = MultiOutputRegressor(MLPRegressor(max_iter=1000, batch_size=20, early_stopping=True, hidden_layer_sizes=180,
                                                 learning_rate='adaptive', n_iter_no_change=40, solver='adam',
                                                 validation_fraction=0.2, learning_rate_init=0.001))

        mlpr.fit(x_train1, y_train1)
        ymlpr = mlpr.predict(x_test1)
        mae_mlpr = mean_absolute_error(y_test1, ymlpr)
        mse_mlpr = mean_squared_error(y_test1, ymlpr)
        r2s_mlpr = r2_score(y_test1, ymlpr)
        distance_error = np.subtract(y_test1, ymlpr)
        distance_error = [sqrt((point[0] ** 2) + (point[1] ** 2)) for point in distance_error]
        max_distance_error = max(distance_error)
        std_distance_error = stdev(distance_error)
        mean_distance_error = mean(distance_error)
        print("Mean Absolute Error: ", mae_mlpr)
        print("Mean Squared Error: ", mse_mlpr)
        print("R2 score: ", r2s_mlpr)
        print(f"Mean Distance Error: {mean_distance_error}, Std: {std_distance_error}")
        print("Max Distance Error: ", max_distance_error)

        y = mlpr.predict(x_test1[0].reshape(1, -1))
        print(f'\n Predicted: {y}, Real: {y_test1[0]}')
        if save_with_pickle:
            t = date.today()
            with open(f'nn_model_{t}.sav', 'wb') as fp:
                pickle.dump(mlpr, fp)
    if len(load_from_pickle) != 0:
        with open(load_from_pickle, 'rb') as fo:
            mlpr = pickle.load(load_from_pickle)
        ymlpr = mlpr.predict(x_test1)

    rand_range = 25
    rand_indices = [randint(0, len(y_test1)) for _ in range(rand_range)]
    x1, y1 = ([y_test1[i][0] for i in rand_indices], [y_test1[i][1] for i in rand_indices])
    x2, y2 = ([ymlpr[i][0] for i in rand_indices], [ymlpr[i][1] for i in rand_indices])
    plt.scatter(x1, y1, marker='o')
    plt.scatter(x2, y2, marker='x')
    plt.show()
    return mlpr, expected_output, matrix_data


def generateData():
    def do_model(x0, v_lin, v_ang):
        th = x0[2]
        vx = v_lin * cos(th)
        vy = v_lin * sin(th)
        return np.array([vx, vy, v_ang])

    v = 1
    r = 1
    w = v / r
    x = np.array([1, 0, 0])
    t = (2 * pi * r) / v
    dt = pi / 10
    tau = 0
    hs = []
    while tau < t:
        tau += dt
        x = x + do_model(x, v, w) * dt
        hs.append(x)
    return hs


if __name__ == "__main__":
    neural_net, plane, iluminatio_data = train_net(train=False,
                                                   load_from_pickle='nn_model_2022-04-13.sav',
                                                   save_with_pickle=False)
    # position_history = generateData()
    # predictions = predict_with_nn(neural_net, position_history, plane, iluminatio_data)
    # xs = []
    # ys = []
    # for pos in position_history:
    #     x = pos[0]
    #     y = pos[1]
    #     xs.append(x)
    #     ys.append(y)
    # xp = []
    # yp = []
    # for pred in predictions:
    #     x = pred[0][0]
    #     y = pred[0][1]
    #     xp.append(x)
    #     yp.append(y)
    # plt.scatter(xs, ys)
    # plt.scatter(xp, yp)
    # plt.show()
