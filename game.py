import pygame as pg
from OpenGL.GL import *
import numpy as np
from triangle import *
from camera import *

class Game:
    def __init__(self):
        self.objs = {}
        self.camera = PerspectiveCamera()
        self.clock = pg.time.Clock()
        self.fps = 60

    def startup(self):
        pg.init()
        pg.display.set_mode(
            (self.camera.view_width,self.camera.view_height), 
            pg.DOUBLEBUF | pg.OPENGL
        )
        pg.display.set_caption("Vegetables")
        glClearColor(0,0,0,0)

        self.objs["triangle"] = Triangle()
        self.objs["triangle"].pos[2] = -3

        self.camera.setPosition([0, 0, 2])

    def draw(self):
        # Clear
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        # Draw objects
        for o in self.objs.values(): o.draw(self.camera.viewMatrix, self.camera.projMatrix)
        # Swap Pygame display
        pg.display.flip()

    def update(self, dt):
        self.camera.moveRelative([0, 0, -dt])

    def loop(self):
        # Game loop
        while True:
            # Handle events
            for event in pg.event.get():
                    if event.type == pg.QUIT:
                        return
            self.draw()
            dt = self.clock.tick(self.fps) / 1000.0
            self.update(dt)

        pg.quit()

    def cleanup(self):
        pass

    def run(self):
        self.startup()
        self.loop()
        self.cleanup()