from dataclasses import dataclass
from math import acos, atan, degrees, cos, radians, sin, pi, sqrt, asin, atan2
from typing import List, Dict
from numpy import sign
from luminarie import Luminarie
from plane import Plane, Axis
from wall import Wall
from sensor import Sensor
from typing import Optional
from ambient import Ambient


class Simulator:
    def __init__(self, luminaries: List[Luminarie], plane: Plane, walls: Optional[List[Wall]], sensor: Sensor,
                 sample_frequency: Optional[int], ambient: Ambient):
        self.horizontal_angles_reach = []
        self.vertical_angles_reach = []
        self.pair_angles_reach = []
        self.walls = walls
        self.luminaries = luminaries
        self.plane = plane
        self.ambient = ambient
        self.sample_frequency = sample_frequency
        self.sensor = sensor
        self.elapsed_time_vector = self._get_elapsed_time()

    # @staticmethod

    def _get_angles(self, dx: float, dy: float, dz: float):
        dist = (dx ** 2) + (dy ** 2) + (dz ** 2)
        dist = sqrt(dist)
        if dist == 0:
            return None, None
        a = degrees(asin(dz / dist))
        if self.ambient.refletance_aperture is None:
            return dist, a
        if self.ambient.refletance_aperture[0] <= a <= self.ambient.refletance_aperture[1]:
            return None, None
        return dist, a

    def get_angles(self, x: float, y: float, lumie: Luminarie, sensor: Sensor):
        dx = lumie.position['x'] - x
        dy = lumie.position['y'] - y
        dz = lumie.position['z'] - sensor.position['z']
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
        self.vertical_angles_reach.append(t)
        self.horizontal_angles_reach.append(p)
        self.pair_angles_reach.append((t, p))
        return p, t, dist

    def __calculate_direct_iluminance(self, lum: Luminarie, plane: Plane, sensor: Sensor, time: float):

        plane_direct_iluminance = {x: {y: 0 for y in plane.points['y']} for x in plane.points['x']}
        factor = 0  # 0.5 * (sign(sin(2 * pi * time * lum.wave_frequency)) + 1) # uncomment this to temporal simulation
        for x in plane.points['x']:
            for y in plane.points['y']:
                phi, theta, dist = self.get_angles(x, y, lum, sensor)
                if phi > lum.max_phi or theta > lum.max_theta:
                    continue
                ilu = lum.light_distribution[phi][theta]
                e = ilu / (dist ** 2)
                plane_direct_iluminance[x][y] = e * (1 + factor)

        return plane_direct_iluminance

    def __calculate_reflected_iluminance(self, wall: Wall, x, y, time):
        constant_axis, c = wall.plane.constant_axis
        factor = 0  # 0.5 * (sign(sin(2 * pi * time * lum.wave_frequency)) + 1) # uncomment this to temporal simulation
        wall_ilu = wall.wall_iluminace[time]
        e = 0
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
                elif constant_axis is Axis.Z.value:
                    dx = a - x
                    dy = b - y
                    dz = c - self.ambient.floor_level['z']

                if dz == self.ambient.floor_level['z']:
                    continue
                dist, alpha = self._get_angles(dx, dy, dz)
                if dist is None:
                    continue
                ilu = wall_ilu[a][b]
                e += ilu * cos(radians(alpha)) * (1 + factor) / (4 * pi * (dist ** 2))
        return e

    def _get_elapsed_time(self):
        if self.sample_frequency is None:
            return [0]
        frequencies = []
        for lum in self.luminaries:
            frequencies.append(lum.wave_frequency)
        dt = 1 / self.sample_frequency
        freq = min(frequencies)
        t = 1 / freq

        n = round(t / dt)
        time = [k * dt for k in range(n)]
        return time

    def simulate(self):
        simulation_light_distribution = {dt: None for dt in self.elapsed_time_vector}
        for dt in self.elapsed_time_vector:
            for lum in self.luminaries:
                plane_iluminance = self.__calculate_direct_iluminance(lum, self.plane, self.sensor, dt)
                self.plane.set_plane_iluminace(plane_iluminance)
                if simulation_light_distribution[dt] is None:
                    simulation_light_distribution[dt] = plane_iluminance
                else:
                    for x in simulation_light_distribution[dt].keys():
                        for y in simulation_light_distribution[dt][x].keys():
                            point_ilu = plane_iluminance[x][y]
                            simulation_light_distribution[dt][x][y] += point_ilu
            reflected_light_distribution = {a: {b: 0 for b in self.plane.points['x']} for a in self.plane.points['y']}
            simulation_reflected_light_distribution = {dt: reflected_light_distribution.copy() for dt in self.elapsed_time_vector}
            for wall in self.walls:
                for x in simulation_light_distribution[dt].keys():
                    for y in simulation_light_distribution[dt][x].keys():
                        reflected_light = self.__calculate_reflected_iluminance(wall, x, y, dt)
                        reflected_light_distribution[x][y] += reflected_light
                        simulation_reflected_light_distribution[dt][x][y] += reflected_light
            for time in simulation_light_distribution.keys():
                for x in simulation_light_distribution[time].keys():
                    for y in simulation_light_distribution[time][x].keys():
                        simulation_light_distribution[dt][x][y] += simulation_reflected_light_distribution[dt][x][y]
        return simulation_light_distribution
