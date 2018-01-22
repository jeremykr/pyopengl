import struct
from matrix_utils import *

class Light:
    def __init__(self, direction, colour):
        self.direction = normalize(direction)
        self.colour = np.array(colour, dtype="float32")