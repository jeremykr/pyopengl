from scene import *
from voxelTerrain import *

class Scene2(Scene):
    def __init__(self):
        super().__init__()

        self.camera = PerspectiveCamera()
        self.camera.setPosition([0, 0, 2])

        self.light = Light(
            direction=[1, -0.8, -0.3],
            colour=[1, 1, 1]
        )

        pg.mouse.set_visible(False)
        # Lock input to the application
        pg.event.set_grab(True)

        terrain = VoxelTerrain("images/BergenHeightMap.png")
        terrain.setShaders("shaders/voxelTerrain.vs", "shaders/voxelTerrain.fs")
        terrain.scale(5)
        self.objs["terrain"] = terrain

    def update(self, dt):
        keys = pg.key.get_pressed()
        mouseX, mouseY = pg.mouse.get_rel()

        # Rotate camera
        camRotSpeed = 50*dt
        mouseSens = 0.1
        self.camera.rotate(-mouseX * mouseSens, [0,1,0])
        self.camera.rotate(-mouseY * mouseSens, [1,0,0])
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