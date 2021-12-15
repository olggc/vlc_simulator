from dataclasses import dataclass
from math import acos, atan, degrees, cos, radians, sin, pi, sqrt, asin, atan2
from typing import List, Dict
from numpy import sign
from luminaries import Luminaries
from plane import Plane, Axis
from wall import Walls
from sensor import Sensor


class Simulator:
    def __init__(self, luminaries: List[Luminaries], plane: Plane, walls: List[Walls], sensor: Sensor,
                 sample_frequency: int):
        self.horizontal_angles_reach = []
        self.vertical_angles_reach = []
        self.walls = walls
        self.luminaries = luminaries
        self.plane = plane
        self.sample_frequency = sample_frequency
        self.sensor = sensor
        self.elapsed_time_vector = self._get_elapsed_time()

    # @staticmethod
    def get_angles(self, x: float, y: float, lumie: Luminaries, sensor: Sensor):
        dx = lumie.position['x'] - x
        dy = lumie.position['y'] - y
        dz = lumie.position['z'] - sensor.position['z']
        dist = (dx ** 2) + (dy ** 2) + (dz ** 2)
        dist = sqrt(dist)

        t = degrees(asin(dz / dist))
        t = t if t > 0 else 360 - abs(t)
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
        return p, t, dist

    def __calculate_direct_iluminance(self, lum: Luminaries, plane: Plane, sensor: Sensor, time: float):

        plane_direct_iluminance = {x: {y: 0 for y in plane.points['y']} for x in plane.points['x']}
        factor = 0  # 0.5 * (sign(sin(2 * pi * time * lum.wave_frequency)) + 1) # uncomment this to temporal simulation
        for x in plane.points['x']:
            for y in plane.points['y']:
                phi, theta, dist = self.get_angles(x, y, lum, sensor)
                if phi > lum.max_phi or theta > lum.max_theta:
                    continue
                ilu = lum.light_distribution[phi][theta]
                cos_ang = cos(radians(theta))
                e = ilu * cos_ang / (dist ** 2)
                plane_direct_iluminance[x][y] = e * (1 + factor)

        return plane_direct_iluminance

    def __calculate_reflected_iluminance(self, wall: Walls, plane, time):
        plane_direct_iluminance = plane.plane_iluminance

        for a in plane_direct_iluminance.keys():
            for b in plane_direct_iluminance[a].keys():
                phi, the, dist = self.get_angles(a, b, wall.wall_iluminace)

    def _get_elapsed_time(self):
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
        x = 1
