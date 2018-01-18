import numpy as np

def translationMatrix(p):
    return np.matrix([
        [1, 0, 0, p[0]],
        [0, 1, 0, p[1]],
        [0, 0, 1, p[2]],
        [0, 0, 0, 1]
    ], dtype="float32")

def rotationMatrix():
    pass

def scaleMatrix(s):
    return np.matrix([
        [s[0], 0, 0, 0],
        [0, s[1], 0, 0],
        [0, 0, s[2], 0],
        [0, 0, 0, 1]
    ], dtype="float32")