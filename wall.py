from copy import deepcopy
from dataclasses import dataclass
from math import sqrt, acos, degrees, atan2, sin, pi, cos, radians, asin
from typing import Dict, Optional, List
from numpy import sign

from luminarie import Luminarie
from plane import Plane, Axis


@dataclass
class Wall:
    __plane: Plane
    __iluminance_per_point: Dict

    def __init__(self, plane: Plane, luminaire: List[Luminarie], refletance: Optional[float] = None,
                 sample_frequency: Optional[int] = None, total_time=None, wall_id: str = None):
        self.__total_time = total_time
        self.__sample_frequency = None if sample_frequency is None else sample_frequency
        self.__ellapsed_time_vector = self.__get_elapsed_time([lum.wave_frequency for lum in luminaire])
        self.__refletance = 0 if refletance is None else refletance
        self.__plane = plane
        self.__wall_index = '' if wall_id is None else wall_id
        self.__constant_axis = plane.constant_axis
        self.__iluminance_per_point = self.__set_wall_iluminance(luminaire) if refletance != 0 else None
        self.__high_order_iluminance = deepcopy(self.__iluminance_per_point)

    @property
    def refletance(self):
        return self.__refletance

    @property
    def wall_index(self):
        return self.__wall_index

    @property
    def min_discretization(self):
        return min(self.plane.discretization.values())

    @property
    def constant_axis(self):
        constant = [axis.value for axis in Axis if axis.value in self.__constant_axis.keys()]
        return constant[0], self.__constant_axis[constant[0]]

    def __get_elapsed_time(self, frequencies: List[int]):
        if self.__sample_frequency is None:
            return [0]
        dt = 1 / self.__sample_frequency
        if self.__total_time is None:
            freq = min(frequencies)
            t = 1 / freq
        else:
            t = self.__total_time
        n = round(t / dt)
        time = [k * dt for k in range(n + 1)]
        return time

    def get_angles(self, x: float, y: float, z: float, lumie: Luminarie):
        dx = lumie.position['x'] - x
        dy = lumie.position['y'] - y
        dz = lumie.position['z'] - z
        dist = (dx ** 2) + (dy ** 2) + (dz ** 2)
        dist = sqrt(dist)

        t = degrees(acos(dz / dist))
        t = t if t > 0 or t != 360 else 360 - abs(t)
        p = degrees(atan2(dy, dx))
        p = p if p > 0 else 360 - abs(p)
        o = degrees(asin(dz / dist))
        o = o if o > 0 or o != 360 else 360 - abs(o)
        p_angles = [key for key in lumie.light_distribution.keys()]
        _, idx_p = min([(abs(p - p_angle), n) for n, p_angle in enumerate(p_angles)], key=lambda a: a[0])
        p = p_angles[idx_p]
        t_angles = [key for key in lumie.light_distribution[p].keys()]
        _, idx_t = min([(abs(t - t_angle), n) for n, t_angle in enumerate(t_angles)], key=lambda a: a[0])
        t = t_angles[idx_t]
        return p, t, dist, o

    def _get_angles(self, dx, dy, dz):
        distance = (dx ** 2) + (dy ** 2) + (dz ** 2)
        distance = sqrt(distance)
        theta = degrees(acos(dz / distance))
        theta = theta if theta > 0 or theta != 360 else 360 - abs(theta)
        phi = degrees(atan2(dy, dx))
        phi = phi if phi > 0 else 360 - abs(phi)
        return phi, theta, distance

    def __calculate_direct_iluminance(self, lum: Luminarie, x: float, y: float, z: float, time: float):
        w = pi * time * lum.wave_frequency
        factor = lum.potency_factor * (1 + sign(sin(2 * w)))  # uncomment this to temporal simulation
        phi, theta, dist, omega = self.get_angles(x, y, z, lum)
        if phi > lum.max_phi or theta > lum.max_theta:
            return 0
        ilu = lum.light_distribution[phi][theta]
        scale = self.refletance * cos(radians(omega)) * self.plane.diferential_area
        e = ilu * scale / (4 * pi * (dist ** 2))
        return e * (1 + factor)

    def __set_wall_iluminance(self, luminarie: List[Luminarie]):
        free_axis = self.plane.free_axis
        constant_axis, c = self.constant_axis
        axis_a = free_axis[0]
        axis_b = free_axis[1]
        timed_iluminance_dict = {dt: None for dt in self.__ellapsed_time_vector}
        for dt in timed_iluminance_dict:
            iluminance_dict = self.generate_illuminance_dict_shell(axis_a, axis_b)
            for lum in luminarie:
                for a in iluminance_dict.keys():
                    for b in iluminance_dict[a].keys():
                        if constant_axis is Axis.X.value:
                            x = c
                            y = a
                            z = b
                        elif constant_axis is Axis.Y.value:
                            x = a
                            y = c
                            z = b
                        elif constant_axis is Axis.Z.value:
                            x = a
                            y = b
                            z = c

                        iluminance_dict[a][b] += self.__calculate_direct_iluminance(lum, x, y, z, dt)
            timed_iluminance_dict[dt] = iluminance_dict
        return timed_iluminance_dict

    def _calculate_second_order_ilu(self, ilu, x, y, z, dt):
        for a in self.wall_iluminace[dt]:
            for b in self.wall_iluminace[dt][a].keys():
                x1, y1, z1 = self._convert_plane_point_to_vector((a, b), self.constant_axis)
                dx = x1 - x
                dy = y1 - y
                dz = z1 - z
                ilu2 = self.__calculate_second_order_ilu(dx, dy, dz, ilu)
                self.__high_order_iluminance[dt][a][b] += ilu2

    def calculate_second_order_ilu(self, other_walls):
        for wall in other_walls:
            for dt in wall.wall_iluminace.keys():
                for a in self.wall_iluminace[dt].keys():
                    for b in self.wall_iluminace[dt][a].keys():
                        i = self.wall_iluminace[dt][a][b]
                        x0, y0, z0 = self._convert_plane_point_to_vector((a, b), wall.constant_axis)
                        self._calculate_second_order_ilu(i, x0, y0, z0, dt)

    def __calculate_second_order_ilu(self, dx, dy, dz, ilu):
        phi, theta, distance = self._get_angles(dx, dy, dz)
        scale = self.refletance
        a = dz / distance
        e = (ilu * scale * a) / (4 * pi * (distance ** 2))
        return e

    def _convert_plane_point_to_vector(self, point: tuple, const_axis):
        constant_axis, c = const_axis
        a, b = point
        if constant_axis is Axis.X.value:
            x = c
            y = a
            z = b
        elif constant_axis is Axis.Y.value:
            x = a
            y = c
            z = b
        elif constant_axis is Axis.Z.value:
            x = a
            y = b
            z = c
        return x, y, z

    def generate_illuminance_dict_shell(self, axis_a, axis_b):
        dict_shell = {
            a: {b: 0 for b in
                self.plane.points[axis_b] if b < self.plane.sizes[axis_b]}
            for a in self.plane.points[axis_a] if a < self.plane.sizes[axis_a]}
        return dict_shell

    @property
    def plane(self):
        return self.__plane

    @property
    def wall_iluminace(self):
        return self.__iluminance_per_point

    def get_wall_iluminance(self, high_order=False):
        if not high_order:
            return self.wall_iluminace
        else:
            return self.__high_order_iluminance

    # def __eq__(self, other: "Wall"):
    #     return self.wall_index == other.wall_index

    def __eq__(self, other: "Wall"):
        for dt in self.wall_iluminace.keys():
            for x in self.wall_iluminace[dt].keys():
                for y in self.wall_iluminace[dt][x].keys():
                    a = self.wall_iluminace[dt][x][y]
                    b = other.wall_iluminace[dt][x][y]
                    if a != b:
                        return False
        return True
