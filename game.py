import pygame as pg
from OpenGL.GL import *
import numpy as np
from triangle import *
from camera import *
from model import *
from light import *

from scenes.scene1 import *

class Game:
    def __init__(self):
        self.scenes = []
        self.currentScene = None
        self.clock = pg.time.Clock()
        self.fps = 60
        self.screenWidth = 0
        self.screenHeight = 0

    def startup(self):
        pg.init()
        self.screenWidth = 800
        self.screenHeight = 600
        pg.display.set_mode(
            (self.screenWidth, self.screenHeight), 
            pg.DOUBLEBUF | pg.OPENGL
        )
        pg.display.set_caption("Vegetables")
        glClearColor(0,0,0,0)

        ### Setup Scene 1 ###
        s1 = Scene1()
        self.scenes.append(s1)
        self.currentScene = s1

    def draw(self):
        # Clear
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        self.currentScene.draw()
        # Swap Pygame display
        pg.display.flip()

    def update(self, dt):
        self.currentScene.update(dt)

    def loop(self):
        # Game loop
        while True:
            # Handle events
            for event in pg.event.get():
                    if event.type == pg.QUIT:
                        return
                    if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                        return
            self.draw()
            dt = self.clock.tick(self.fps) / 1000.0
            self.update(dt)

        pg.quit()

    def cleanup(self):
        for scene in self.scenes: del scene

    def run(self):
        self.startup()
        self.loop()
        self.cleanup()