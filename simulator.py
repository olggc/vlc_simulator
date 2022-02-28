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
    def __init__(self, ambient: Ambient, randomness=False, allow_high_order=False):
        self.total_time = ambient.total_time if ambient.total_time is not None else None
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
        a = degrees(asin(dz / dist))
        if self.ambient.refletance_aperture is None:
            return dist, a
        if self.ambient.refletance_aperture[0] <= a <= self.ambient.refletance_aperture[1]:
            return None, None
        return dist, a

    @staticmethod
    def random_value_generator():
        return 0.05 * np.random.normal(loc=0.0, scale=1.0)

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

        p_angles = [key for key in lumie.light_distribution.keys()]
        _, idx_p = min([(abs(p - p_angle), n) for n, p_angle in enumerate(p_angles)], key=lambda a: a[0])
        p = p_angles[idx_p]
        t_angles = [key for key in lumie.light_distribution[p].keys()]
        _, idx_t = min([(abs(t - t_angle), n) for n, t_angle in enumerate(t_angles)], key=lambda a: a[0])
        t = t_angles[idx_t]
        self.vertical_angles_reach.add(t)
        self.horizontal_angles_reach.add(p)
        self.pair_angles_reach.add((t, p))
        return p, t, dist

    def __calculate_direct_iluminance(self, x, y, time: float) -> float:
        e = 0
        noisy = 0
        if self.randomness:
            noisy = self.random_value_generator()
        for lum in self.luminaries:
            factor = 0.05 * np.sign(sin(2 * pi * time * lum.wave_frequency))
            phi, theta, dist = self.get_angles(x, y, lum)
            if phi > lum.max_phi or theta > lum.max_theta:
                continue
            ilu = lum.light_distribution[phi][theta]
            ilu = ilu / (dist ** 2)
            e += ilu * (1 + factor + noisy)
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
                    ilu = wall_ilu[a][b]
                    e += ilu * (1 + noisy) * cos(radians(alpha)) / (dist ** 2)
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
                    plane_dict[x][y] += self.__calculate_reflected_iluminance(x, y, dt)
                    print(f'Indirect Iluminace = {ilu}')
            simulation_light_distribution[dt] = plane_dict
        end_time = time.time()
        print(f'Execution time: {end_time - start_time}')
        self.results = simulation_light_distribution
        return simulation_light_distribution

    def f(self, dt):
        z_axis = np.array([self.results[dt][x][y]
                           for x in self.plane.points['x']
                           for y in self.plane.points['y']])
        z_axis = z_axis.reshape((len(self.plane.points['x']), len(self.plane.points['y'])))
        return z_axis.T

    def plotting(self, dt=0, graph_type='surface'):
        z_axis = self.f(dt)
        if graph_type == 'heatmap':
            ax = sb.heatmap(z_axis)
            ax.invert_yaxis()
            ax.set_title('Simulator Iluminance[cd] Room Heatmap')
            ax.set_xlabel('X points')
            ax.set_ylabel('Y points')
            plt.show()
        if graph_type == 'surface':
            fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
            n = len(self.plane.points['x'])
            X = np.arange(0, n, 1)
            Y = np.arange(0, n, 1)
            X, Y = np.meshgrid(X, Y)
            surf = ax.plot_surface(X, Y, z_axis, cmap='viridis',
                                   edgecolor='none',
                                   linewidth=0, antialiased=False)
            ax.set_title('Simulator Iluminance[cd] Room Distribution')
            ax.set_xlabel('X points')
            ax.set_ylabel('Y points')
            ax.set_zlabel('Illuminance[cd]')
            fig.colorbar(surf, shrink=0.5, aspect=5)

            plt.show()

    def animate(self):
        for dt in self.results.keys():
            self.plotting(dt)
