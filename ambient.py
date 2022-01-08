from luminarie import Luminarie
from typing import List, Optional
from wall import Wall
from plane import Plane
from sensor import Sensor


class Ambient:
    def __init__(self, ambient_settings):
        self.__total_time = None
        self.__floor_level = {'z': 0}
        self.__sample_frequency = None
        self.__room_sizes = None
        self.__lumies: List[Luminarie] = []
        self.__plane: Optional[Plane] = None
        self.__refletance_aperture = None
        self.__walls: List[Wall] = []
        self.__sensor: Optional[Sensor] = None
        self.__generate_ambient(ambient_settings)

    @property
    def sample_frequency(self):
        return self.__sample_frequency

    @property
    def floor_level(self):
        return self.__floor_level

    @property
    def refletance_aperture(self):
        return self.__refletance_aperture

    @property
    def room_sizes(self):
        return self.__room_sizes

    @property
    def luminaries(self):
        return self.__lumies

    @property
    def floor(self):
        return self.__plane

    @property
    def sensor(self):
        return self.__sensor

    @property
    def walls(self):
        return self.__walls

    @property
    def total_time(self):
        return self.__total_time

    def __generate_ambient(self, ambient_settings):
        self.__total_time = ambient_settings['total_simulation_time']
        aperture = ambient_settings['ambient']['refletance_aperture']
        self.__refletance_aperture = aperture if aperture is not None else self.__refletance_aperture
        self.__sample_frequency = ambient_settings['ambient']['sample_frequency']
        lums_position = ambient_settings['luminaries']['positions']
        for n, pos in enumerate(lums_position):
            lumie = Luminarie(ies_file_path=ambient_settings['luminaries']['ies_file_path'],
                              wave_frequency=ambient_settings['luminaries']['modulation_frequencies'][n], position=pos)
            self.__lumies.append(lumie)

        num = ambient_settings['ambient']['divisions_number']
        self.__room_sizes = ambient_settings['ambient']['room_sizes']
        constant_axis = {'z': ambient_settings['ambient']['floor_level']}
        self.__floor_level = constant_axis.copy()
        self.__plane = Plane(number_of_divisions=num, sizes=self.room_sizes, constant_axis=constant_axis)

        for const_axis in ambient_settings['ambient']['walls']:
            plane = Plane(number_of_divisions=num, sizes=self.room_sizes, constant_axis=const_axis)
            wall = Wall(plane=plane, luminaire=self.luminaries,
                        refletance=ambient_settings['ambient']['walls_refletance'],
                        sample_frequency=self.__sample_frequency, total_time=self.total_time)
            self.__walls.append(wall)

        self.__sensor = Sensor(position=ambient_settings['sensor_position'])
