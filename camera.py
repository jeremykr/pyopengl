import numpy as np
from matrix_utils import *
from numpy.linalg import inv
from pyquaternion import *

class PerspectiveCamera:
    def __init__(self):
        self.view_width = 800
        self.view_height = 600
        self.far_plane = 1000.0
        self.near_plane = 0.05
        self.fov = 60
        self.aspect_ratio = self.view_width / self.view_height

        self.pos = np.zeros(3, dtype="float32")
        self.quat = Quaternion()

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

    def getViewMatrix(self):
        return (
            self.quat.inverse.transformation_matrix *
            inv(translationMatrix(self.pos))
        )

    def move(self, d):
        self.pos += self.quat.rotate(d)

    def rotate(self, deg, axis):
        r = np.deg2rad(deg)
        axis = self.quat.rotate(axis)
        self.quat = Quaternion(axis=axis, angle=r) * self.quat

    def setPosition(self, p):
        self.pos = p
