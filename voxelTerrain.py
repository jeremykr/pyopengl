from model import *
import pygame as pg

class VoxelTerrain(Model):
    def __init__(self, textureFilename):
        surface = pg.image.load(textureFilename)
        width = surface.get_width()
        height = surface.get_height()
        texData = pg.image.tostring(surface, "RGBA", True)

        texData = np.array([i for i in texData]) / 255

        tex = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, tex)
        glTexImage2D(
            GL_TEXTURE_2D,  # target
            0,              # mipmap level
            GL_RGBA32F,     # internal format
            width,          # image width
            height,          # image height
            0,              # border
            GL_RGBA,        # OpenGL format
            GL_FLOAT,       # type
            texData         # texture data
        )

        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)

        terrainScale = 1 / 15
        # define the space between points
        offset = 1/(width-1)
        vertexData = np.empty(width * height * 3, dtype="float32")
        for y in range(height):
            for x in range(width):
                i = y * width * 3 + x * 3
                vertexData[i] = x * offset
                vertexData[i+1] = texData[y * width * 4 + x * 4] * terrainScale
                vertexData[i+2] = y * offset

        super().__init__(vertexData, [3])

        self.drawMode = GL_POINTS

    def draw(self, camera, light):
        glActiveTexture(GL_TEXTURE0)
        super().draw(camera, light)

    def setShaders(self, vshader, gshader, fshader):
        self.pid = makeProgram({
            GL_VERTEX_SHADER : vshader,
            GL_GEOMETRY_SHADER : gshader,
            GL_FRAGMENT_SHADER : fshader
        })
        return self
        