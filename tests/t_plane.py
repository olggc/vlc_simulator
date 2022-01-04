from luminaries import Luminarie
from plane import Plane

number_of_divisions = 5
constant_axis = {'z': 1}
sizes = {axis: 1 for axis in ('x', 'y', 'z') if axis not in constant_axis.keys()}
plane = Plane(number_of_divisions, sizes, constant_axis)

test_array = {
    'x': [0, 0.2, 0.4, 0.6, 0.8, 1.0],
    'y': [0, 0.2, 0.4, 0.6, 0.8, 1.0]
}
array_tested = plane.points
for axis in array_tested.keys():
    assert test_array[axis] == array_tested[axis]


number_of_divisions = 5
constant_axis = {'z': 1}
sizes = {axis: 3 for axis in ('x', 'y', 'z') if axis not in constant_axis.keys()}
plane = Plane(number_of_divisions, sizes, constant_axis)

assert plane.area == 9

path = 'LEDblue.txt'
lums = Luminarie(path)
x = 1

