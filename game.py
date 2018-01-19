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
        keys = pg.key.get_pressed()

        # Rotate camera
        camRotSpeed = 50*dt
        if keys[pg.K_LEFT]: self.camera.rotate(camRotSpeed, [0,1,0])
        if keys[pg.K_RIGHT]: self.camera.rotate(-camRotSpeed, [0,1,0])
        if keys[pg.K_UP]: self.camera.rotate(-camRotSpeed, [1,0,0])
        if keys[pg.K_DOWN]: self.camera.rotate(camRotSpeed, [1,0,0])
        if keys[pg.K_q]: self.camera.rotate(camRotSpeed, [0,0,1])
        if keys[pg.K_e]: self.camera.rotate(-camRotSpeed, [0,0,1])

        # Move camera
        moveDirection = [0, 0, 0]
        camMoveSpeed = 3 * dt
        if keys[pg.K_w]: moveDirection[2] += -1
        if keys[pg.K_s]: moveDirection[2] += 1
        if keys[pg.K_a]: moveDirection[0] += -1
        if keys[pg.K_d]: moveDirection[0] += 1
        if keys[pg.K_f]: moveDirection[1] += -1
        if keys[pg.K_r]: moveDirection[1] += 1
        moveDirection = normalize(moveDirection)
        self.camera.move(moveDirection * camMoveSpeed)

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