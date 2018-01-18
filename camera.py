import numpy as np
from matrix_utils import *

class PerspectiveCamera:
    def __init__(self):
        self.view_width = 800
        self.view_height = 600
        self.far_plane = 1000.0
        self.near_plane = 0.01
        self.fov = 60
        self.aspect_ratio = self.view_width / self.view_height
        
        self.viewMatrix = np.identity(4, dtype="float32")
        self.rotMatrix = np.identity(4, dtype="float32")

        n = self.near_plane
        f = self.far_plane
        t = np.tan(np.deg2rad(self.fov)/2) * n
        r = t * self.aspect_ratio

        self.projMatrix = np.matrix([
            [n/r, 0, 0, 0],
            [0, n/t, 0, 0],
            [0, 0, -(f+n)/(f-n), -2*f*n/(f-n)],
            [0, 0, -1, 0]
        ], dtype="float32")

    def moveRelative(self, d):
        d = np.array([d[0], d[1], d[2], 0])
        self.viewMatrix = (
            np.linalg.inv(self.rotMatrix) *
            np.linalg.inv(translationMatrix(d)) *
            self.viewMatrix
        )

    def setPosition(self, p):
        p = -np.array(p)
        self.viewMatrix = np.matrix([
            [1, 0, 0, p[0]],
            [0, 1, 0, p[1]],
            [0, 0, 1, p[2]],
            [0, 0, 0, 1]
        ], dtype="float32")
