import time

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sb
from matplotlib import cm
from math import acos, degrees, cos, radians, sin, pi, sqrt, asin, atan2
from luminarie import Luminarie
from plane import Axis
from ambient import Ambient


class Simulator:
    def __init__(self, ambient: Ambient, randomness=False, allow_high_order=False, neighbor_num=0):
        self.total_time = ambient.total_time if ambient.total_time is not None else None
        self.neighbor_num = neighbor_num
        self.horizontal_angles_reach = set()
        self.vertical_angles_reach = set()
        self.pair_angles_reach = set()
        self.walls = ambient.walls
        self.with_reflection = any(w.refletance > 0 for w in self.walls)
        self.luminaries = ambient.luminaries
        self.plane = ambient.floor
        self.ambient = ambient
        self.sample_frequency = ambient.sample_frequency
        self.sensor = ambient.sensor
        self.results = dict()
        self.randomness = randomness
        self.allow_high_order = allow_high_order
        self.elapsed_time_vector = self._get_elapsed_time()
        # for idx in range(len(self.walls) - 1):
        #     if self.walls[idx] != self.walls[idx + 1]:
        #         assert False

    # @staticmethod

    def _get_angles(self, dx: float, dy: float, dz: float):
        dist = (dx ** 2) + (dy ** 2) + (dz ** 2)
        dist = sqrt(dist)
        if dist == 0:
            return 0, None
        a = degrees(acos(dz / dist))
        if self.ambient.refletance_aperture is None:
            return dist, a
        if self.ambient.refletance_aperture[0] <= a <= self.ambient.refletance_aperture[1]:
            return None, None
        return dist, a

    @staticmethod
    def random_value_generator():
        return 0.05 * np.random.normal(loc=0.0, scale=1.0)

    def get_angles_knn(self, x: float, y: float, lumie: Luminarie):
        dx = lumie.position['x'] - x
        dy = lumie.position['y'] - y
        dz = lumie.position['z'] - self.ambient.floor_level['z']
        dist = (dx ** 2) + (dy ** 2) + (dz ** 2)
        dist = sqrt(dist)

        t = degrees(acos(dz / dist))
        t = t if t > 0 or t != 360 else 360 - abs(t)
        p = degrees(atan2(dy, dx))
        p = p if p > 0 else 360 - abs(p)

        p_angles = [key for key in lumie.light_distribution.keys()]
        any_key = p_angles[-1]
        t_angles = [key for key in lumie.light_distribution[any_key].keys()]
        ids_p, ids_t = self.do_knn(p, t, p_angles, t_angles, self.neighbor_num)
        return ids_p, ids_t, dist

    def __calculate_direct_iluminance(self, x, y, time: float) -> float:
        e = 0
        noisy = 0
        if self.randomness:
            noisy = self.random_value_generator()
        for lum in self.luminaries:
            d = lum.position['z']
            factor = lum.potency_factor * (1 + np.sign(sin(2 * pi * time * lum.wave_frequency)))
            if self.neighbor_num > 0:
                phi, theta, dist = self.get_angles_knn(x, y, lum)
                ilu = self.knn_iluminace(lum.light_distribution, phi, theta, self.neighbor_num)
                omega = sum([th * diff for th, diff in theta]) / sum([d for _, d in theta])
            else:
                phi, theta, dist, omega = self.get_angles(x, y, lum)
                ilu = lum.light_distribution[phi][theta]
            cosphi = cos(radians(omega))
            ilu = (ilu * cosphi) / (dist ** 2)
            e += ilu * (factor + noisy)
        return e

    def __calculate_reflected_iluminance(self, x, y, time):
        e = 0
        noisy = 0
        if self.randomness:
            noisy = self.random_value_generator()

        for index in range(len(self.walls)):
            w = self.walls[index]
            constant_axis, c = self.walls[index].constant_axis
            wall_iluminance = self.walls[index].get_wall_iluminance(high_order=self.allow_high_order)
            wall_ilu = wall_iluminance[time]
            for a in wall_ilu.keys():
                for b in wall_ilu[a].keys():
                    if constant_axis is Axis.X.value:
                        dx = c - x
                        dy = a - y
                        dz = b - self.ambient.floor_level['z']
                    elif constant_axis is Axis.Y.value:
                        dx = a - x
                        dy = c - y
                        dz = b - self.ambient.floor_level['z']

                    dist, alpha = self._get_angles(dx, dy, dz)
                    if dist == 0:
                        continue
                    if (dx == 0) or (dy == 0) or (dz == 0):
                        continue
                    if dist >= max(self.plane.sizes.values()):
                        continue
                    if dist <= max(self.plane.discretization.values()):
                        continue
                    if dist <= max([w.min_discretization for w in self.walls]):
                        continue
                    ilu = wall_ilu[a][b]
                    scale = (1 + noisy) * cos(radians(alpha))
                    e += ilu * scale / (dist ** 2)
        return e

    def _get_elapsed_time(self):
        if self.sample_frequency is None or self.total_time is None:
            return [0]
        frequencies = []
        for lum in self.luminaries:
            frequencies.append(lum.wave_frequency)
        dt = 1 / self.sample_frequency
        if self.total_time is None:
            freq = min(frequencies)
            t = 1 / freq
        else:
            t = self.total_time

        n = round(t / dt)
        tau = [k * dt for k in range(n + 1)]
        return tau

    def simulate(self):
        start_time = time.time()
        simulation_light_distribution = {dt: None for dt in self.elapsed_time_vector}
        for dt in self.elapsed_time_vector:
            plane_dict = {x: {y: 0 for y in self.plane.points['y']} for x in self.plane.points['x']}
            for x in self.plane.plane_iluminance.keys():
                for y in self.plane.plane_iluminance[x].keys():
                    print(f'Calculating Iluminance for point x = {x}, y = {y} at time = {dt}\n')
                    ilu = self.__calculate_direct_iluminance(x, y, dt)
                    plane_dict[x][y] += ilu
                    self.plane.plane_iluminance[x][y] += ilu
                    print(f'Direct Iluminace = {ilu}')
                    if not self.with_reflection:
                        continue
                    # if x < self.plane.discretization['x'] or y < self.plane.discretization['y']:
                    #     continue
                    # if x > self.plane.sizes['x'] - self.plane.discretization['x'] \
                    #         or y > self.plane.sizes['y'] - self.plane.discretization['y']:
                    #     continue
                    plane_dict[x][y] += self.__calculate_reflected_iluminance(x, y, dt)
                    print(f'Indirect Iluminace = {ilu}')
            simulation_light_distribution[dt] = plane_dict
        end_time = time.time()
        print(f'Execution time: {end_time - start_time}')
        self.results = simulation_light_distribution
        return simulation_light_distribution

    def f(self, dt, with_numpy=True):
        if with_numpy:
            z_axis = np.array([self.results[dt][x][y]
                               for x in self.plane.points['x']
                               for y in self.plane.points['y']])
            z_axis = z_axis.reshape((len(self.plane.points['x']), len(self.plane.points['y'])))
            return z_axis.T
        else:
            z_values = [self.results[dt][x][y]
                        for x in self.plane.points['x']
                        for y in self.plane.points['y']]
            return z_values

    def plotting(self, dt=0, graph_type='surface'):
        z_axis = self.f(dt)
        if graph_type == 'heatmap':
            ax = sb.heatmap(z_axis)
            ax.invert_yaxis()
            ax.set_title(f'Mapa de Calor para t = {round(dt * 100000, 4)} us')
            ax.set_xlabel('X points')
            ax.set_ylabel('Y points')
            plt.show()
            plt.pause(0.1)
            plt.close()
        if graph_type == 'surface':
            fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
            n = len(self.plane.points['x'])
            X = np.arange(0, 1, 1 / n)
            Y = np.arange(0, 1, 1 / n)
            X, Y = np.meshgrid(X, Y)
            surf = ax.plot_surface(X, Y, z_axis, cmap='viridis',
                                   edgecolor='none',
                                   linewidth=0, antialiased=False)
            ax.set_title('Simulador - Distribuição de Iluminância no Ambiente')
            ax.set_xlabel('X')
            ax.set_ylabel('Y')
            ax.set_zlabel('Illuminance[lx]')
            fig.colorbar(surf, shrink=0.5, aspect=5)

            plt.show()

    def animate(self):
        for dt in self.results.keys():
            self.plotting(dt)

    @staticmethod
    def do_knn(p, t, ps, ts, N):
        nearest_ps = []
        nearest_ts = []
        N = min([len(ps), len(ts), N])
        already_chosen_ps = []
        already_chosen_ts = []
        for k in range(0, N):
            dif_i, i = min([(abs(p - p_angle), n) for n, p_angle in enumerate(ps) if p_angle not in already_chosen_ps],
                           key=lambda a: a[0])
            dif_j, j = min([(abs(t - t_angle), n) for n, t_angle in enumerate(ts) if t_angle not in already_chosen_ts],
                           key=lambda a: a[0])
            already_chosen_ps.append(ps[i])
            already_chosen_ts.append(ts[j])
            nearest_ps.append((ps[i], dif_i))
            nearest_ts.append((ts[j], dif_j))

        return nearest_ps, nearest_ts

    def knn_iluminace(self, light_distribution, phi, theta, N):
        i = 0
        angles_combinations = list(zip(phi, theta))
        total_weight = sum([sqrt((p[1] ** 2) + (t[1] ** 2)) for p, t in angles_combinations])
        for ph, th in angles_combinations:
            w = sqrt((ph[1] ** 2) + (th[1] ** 2)) / total_weight
            i += (light_distribution[ph[0]][th[0]] * w)
        return i

    def get_angles(self, x: float, y: float, lumie: Luminarie):
        dx = lumie.position['x'] - x
        dy = lumie.position['y'] - y
        dz = lumie.position['z'] - self.ambient.floor_level['z']
        dist = (dx ** 2) + (dy ** 2) + (dz ** 2)
        dist = sqrt(dist)

        t = degrees(acos(dz / dist))
        t = t if t > 0 or t != 360 else 360 - abs(t)
        p = degrees(atan2(dy, dx))
        p = p if p > 0 else 360 - abs(p)
        o = degrees((acos(dz / dist)))
        o = o if o > 0 or o != 360 else 360 - abs(o)
        p_angles = [key for key in lumie.light_distribution.keys()]
        _, idx_p = min([(abs(p - p_angle), n) for n, p_angle in enumerate(p_angles)], key=lambda a: a[0])
        p = p_angles[idx_p]
        t_angles = [key for key in lumie.light_distribution[p].keys()]
        _, idx_t = min([(abs(t - t_angle), n) for n, t_angle in enumerate(t_angles)], key=lambda a: a[0])
        t = t_angles[idx_t]
        self.vertical_angles_reach.add(t)
        self.horizontal_angles_reach.add(p)
        self.pair_angles_reach.add((t, p))
        return p, t, dist, o
