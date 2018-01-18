import pygame as pg
from OpenGL.GL import *
import numpy as np
from triangle import *
from camera import *

class Game:
    def __init__(self):
        self.objs = {}
        self.camera = PerspectiveCamera()

    def startup(self):
        pg.init()
        pg.display.set_mode(
            (self.camera.view_width,self.camera.view_height), 
            pg.DOUBLEBUF | pg.OPENGL
        )
        pg.display.set_caption("Vegetables")
        glClearColor(0,0,0,0)

        triangle = Triangle()
        triangle.pos[2] = -2

        self.objs["triangle"] = triangle

    def draw(self):
        # Clear
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        # Draw objects
        for o in self.objs.values(): o.draw(self.camera.viewMatrix, self.camera.projMatrix)
        # Swap Pygame display
        pg.display.flip()

    def update(self):
        self.camera.pos[2] += 0.01
        self.camera.update()

    def loop(self):    
        # Game loop
        while True:
            # Handle events
            for event in pg.event.get():
                    if event.type == pg.QUIT:
                        return
            self.draw()
            self.update()

        pg.quit()

    def cleanup(self):
        pass

    def run(self):
        self.startup()
        self.loop()
        self.cleanup()