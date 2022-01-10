from typing import Dict

from scipy.signal import butter, sosfilt


class Filter:

    def __init__(self, filter_parameters, sample_rate, filter_id):
        self.filter = None
        self.filter_id = filter_id
        self.sample_rate = sample_rate
        self._generate_filter(filter_parameters)

    def filter_data(self, data):
        return sosfilt(self.filter, data)

    def _generate_filter(self, filter_parameters):
        self.low_cut = filter_parameters['low_cut']
        self.high_cut = filter_parameters['high_cut']
        self.order = filter_parameters['order']
        self.__init_filter()

    def __init_filter(self):
        nyq = 0.5 * self.sample_rate
        low = self.low_cut / nyq
        high = self.high_cut / nyq
        self.filter = butter(self.order, [low, high], analog=False,
                             btype='band', output='sos')


class Sensor:

    def __init__(self, position, filter_parameters, sample_rate):
        self.sensor_filters = []
        for filter_id in filter_parameters.keys():
            self.sensor_filters.append(Filter(filter_parameters=filter_parameters[filter_id],
                                              sample_rate=sample_rate,
                                              filter_id=filter_id))
        self.position: Dict[str, float] = position
