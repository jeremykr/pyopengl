import pygame as pg
from OpenGL.GL import *
import numpy as np
from triangle import *
from camera import *
from model import *
from light import *

# Generic class for defining a drawable scene that can
# be displayed and controlled in the main game window.
class Scene:
    def __init__(self):
        self.objs = {}
        self.camera = None
        self.light = None

    def draw(self):
        # Draw objects
        for o in self.objs.values(): 
            o.draw(
                self.camera,
                self.light
            )

    def update(self, dt):
        raise NotImplementedError

    def setup(self):
        raise NotImplementedError