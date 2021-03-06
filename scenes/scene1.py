from scene import *

class Scene1(Scene):
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

        # Create scene objects
        self.objs["triangle"] = Triangle()
        self.objs["triangle"].pos[2] = -3

        cube = Model \
            .fromObj("models/cube/cube.obj") \
            .setShaders("models/cube/cube.vs", "models/cube/cube.fs")
        cube.setPosition([0, 0, -10])
        self.objs["cube"] = cube

        teacup = Model \
            .fromObj("models/teacup/Teacup.obj") \
            .setShaders("models/teacup/teacup.vs", "models/teacup/teacup.fs")
        teacup.setPosition([2,-2,0])
        teacup.material = Material.fromMtl("models/teacup/Teacup.mtl")
        self.objs["teacup"] = teacup

        text = Model \
            .fromObj("models/text/text.obj") \
            .setShaders("models/text/text.vs", "models/text/text.fs")
        text.setPosition([-2,2,0])
        text.material = Material.fromMtl("models/text/text.mtl")
        self.objs["text"] = text
        text.rotate(90, [1,0,0])

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

        self.objs["cube"].rotate(40 * dt, [0,1,0])
        self.objs["teacup"].rotate(40 * dt, [1,1,1])
        self.objs["text"].rotate(60 * dt, [0,0,1])