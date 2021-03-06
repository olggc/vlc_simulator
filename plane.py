import enum
from typing import Dict, List


class Axis(enum.Enum):
    X = 'x'
    Y = 'y'
    Z = 'z'


class Plane:
    def __init__(self, number_of_divisions, sizes, constant_axis, refletance=None):
        self.__axis = [axis.value for axis in Axis]
        self.half_board = dict()
        self.discretization = dict()
        self.__constant_axis: Dict[str, float] = constant_axis
        self._number_of_divisions: int = number_of_divisions
        self._sizes: Dict[str, float] = sizes
        self._points: Dict[str, float] = self.__calculate_plane_points()
        self.__area: float = self.__calculate_area()
        self.__incident_luminance: Dict = self.__default_luminance()
        self.__refletance: float = refletance

    def __calculate_plane_points(self, half_board=True):
        points = {axis: [] for axis in self.__axis if axis not in self.__constant_axis.keys()}
        if half_board:
            for axis in points.keys():
                if axis in self.__constant_axis.keys():
                    continue
                self.discretization[axis] = self._sizes[axis] / self._number_of_divisions
                half = self.discretization[axis] / 2
                self.half_board[axis] = half
                self.discretization[axis] = (self._sizes[axis] - self.discretization[axis]) / self._number_of_divisions
                points[axis] = [(k * self.discretization[axis]) + half for k in
                                range(self._number_of_divisions + 1)]
        else:
            for axis in points.keys():
                if axis in self.__constant_axis.keys():
                    continue
                self.discretization[axis] = self._sizes[axis] / self._number_of_divisions
                points[axis] = [k * self.discretization[axis] for k in
                                range(self._number_of_divisions + 1)]
        return points

    def __calculate_area(self):
        area = 1
        for axis in self._sizes.keys():
            size_magnitude = self._sizes[axis]
            if axis in self.__constant_axis.keys():
                continue
            area *= size_magnitude
        return area

    def __default_luminance(self):
        free_axis = [axis for axis in self.__axis if axis not in self.__constant_axis.keys()]
        points_per_axis: List[List[float]] = [self._points[axis] for axis in free_axis]

        lum = {x: {y: 0 for y in points_per_axis[1]} for x in points_per_axis[0]}
        return lum

    def set_plane_iluminace(self, plane_iluminance):
        self.__incident_luminance = plane_iluminance

    @property
    def plane_iluminance(self):
        return self.__incident_luminance

    @property
    def points(self):
        return self._points

    @property
    def area(self):
        return self.__area

    @property
    def diferential_area(self):
        area = 1
        for axis in self._sizes.keys():
            if axis in self.__constant_axis.keys():
                continue
            size = self._sizes[axis] / self._number_of_divisions
            area *= size
        return area

    @property
    def sizes(self):
        return self._sizes

    @property
    def free_axis(self):
        return [axis.value for axis in Axis if axis.value not in self.__constant_axis.keys()]

    @property
    def constant_axis(self):
        return self.__constant_axis

    @property
    def iluminance(self):
        return self.__incident_luminance

    @property
    def points(self):
        return self._points
