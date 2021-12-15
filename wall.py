from dataclasses import dataclass
from math import sqrt, acos, degrees, atan, radians, cos
from typing import Dict, Optional

from luminaries import Luminaries
from plane import Plane, Axis


@dataclass
class Walls:
    __plane: Plane
    __iluminance_per_point: Dict

    def __init__(self, plane: Plane, luminaire: Luminaries, refletance: Optional[float] = None):
        self.__refletance = refletance if refletance is not None else 0
        self.__plane = plane
        self.__iluminance_per_point = self.__set_wall_iluminance(luminaire)

    @property
    def refletance(self):
        return self.__refletance

    def __set_wall_iluminance(self, luminarie: Luminaries):
        free_axis = self.plane.free_axis
        constant_axis, c = self.plane.constant_axis
        axis_a = free_axis[0]
        axis_b = free_axis[1]
        iluminance_dict = {a: {b: None for b in self.plane.points[axis_b]} for a in self.plane.points[axis_a]}
        for a in self.plane.points[axis_a]:
            for b in self.plane.points[axis_b]:
                if constant_axis is Axis.X.value:
                    da = luminarie.position[constant_axis] - a
                    db = luminarie.position[axis_a] - b
                    dc = luminarie.position[axis_b] - c
                    pos = {constant_axis: a, axis_a: b, axis_b: c}
                elif constant_axis is Axis.Y.value:
                    da = luminarie.position[axis_a] - a
                    db = luminarie.position[constant_axis] - b
                    dc = luminarie.position[axis_b] - c
                    pos = {axis_a: a, constant_axis: b, axis_b: c}
                elif constant_axis is Axis.Z.value:
                    da = luminarie.position[axis_a] - a
                    db = luminarie.position[axis_b] - b
                    dc = luminarie.position[constant_axis] - c
                    pos = {axis_a: a, axis_b: b, constant_axis: c}

                dist = sqrt((da ** 2) + (db ** 2) + (dc ** 2))
                ang_a = degrees(acos(dc / dist))  # vertical angles
                ang_a = ang_a if ang_a > 0 else 360 - abs(ang_a)
                ang_b = abs(degrees(atan(da / db)))  # horizontal angles
                ang_b = ang_b if ang_b > 0 else 360 - abs(ang_b)

                candidates_ang_b = [ang for ang in luminarie.light_distribution.keys()]
                idx_ang_b, _ = min([(i, abs(ang_b - ang)) for i, ang in enumerate(candidates_ang_b)],
                                   key=lambda b: b[1])
                ang_b = candidates_ang_b[idx_ang_b]

                candidates_ang_a = [ang for ang in luminarie.light_distribution[ang_b].keys()]
                idx_ang_a, _ = min([(i, abs(ang_a - ang)) for i, ang in enumerate(candidates_ang_a)],
                                   key=lambda a: a[1])
                ang_a = candidates_ang_a[idx_ang_a]
                scale_factor = self.refletance * cos(radians(ang_a)) / (dist ** 2)

                new_light_distribution = {t: {p: None for p in candidates_ang_a} for t in candidates_ang_b}
                for theta in luminarie.light_distribution.keys():
                    for phi in luminarie.light_distribution[theta].keys():
                        new_lum = luminarie.light_distribution[theta][phi] * scale_factor
                        new_light_distribution[theta][phi] = new_lum

                lum = Luminaries(wave_frequency=luminarie.wave_frequency, position=pos, lums=new_light_distribution)
                if iluminance_dict[a][b] is None:
                    iluminance_dict[a][b] = lum

        return iluminance_dict

    @property
    def plane(self):
        return self.__plane

    @property
    def wall_iluminace(self):
        return self.__iluminance_per_point
