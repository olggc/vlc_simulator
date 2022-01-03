from luminaries import Luminaries
from plane import Plane
from simulator import Simulator
from sensor import Sensor
from wall import Walls

path = 'LEDblue.txt'
# lums_position = [
#     {'x': 0.49, 'y': 0.24, 'z': 1},
#     {'x': 0.24, 'y': 0.74, 'z': 1},
#     {'x': 0.74, 'y': 0.74, 'z': 1}
# ]
lums_position = [
    {'x': 0.5, 'y': 0.5, 'z': 1}
]
wave_frequency = [2000, 3000, 4000]

lums = []
for n, pos in enumerate(lums_position):
    lum = Luminaries(ies_file_path=path, wave_frequency=wave_frequency[n], position=pos)
    lums.append(lum)

num = 6
sizes = {'x': 1, 'y': 1, 'z': 1}
constant_axis = {'z': 0}
plane = Plane(number_of_divisions=num, sizes=sizes, constant_axis=constant_axis)
wall = Walls(plane=plane, luminaire=lums[0], refletance=0.8)
sensor_position = {'x': 0.5, 'y': 0.5, 'z': 0}
sensor = Sensor(position=sensor_position)

sample_frequency = 100000
planes = [plane]
simulator = Simulator(lums, plane, sensor, sample_frequency)
simulator.simulate()
