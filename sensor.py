from typing import Dict


class Sensor:

    def __init__(self, position):
        self.position: Dict[str, float] = position
