from model import *
import pygame as pg

class VoxelTerrain(Model):
    def __init__(self, textureFilename):
        surface = pg.image.load(textureFilename)
        width = surface.get_width()
        height = surface.get_height()
        texData = pg.image.tostring(surface, "RGBA", True)

        # move pixel values from 0-255 to -128-127
        texData = np.array([i for i in texData]) - 128
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

        # define the space between points
        offset = 1/(width-1)
        vertexData = np.empty(width * height * 2, dtype="float32")
        for y in range(height):
            for x in range(width):
                vertexData[y * width * 2 + x * 2] = x * offset - 0.5
                vertexData[y * width * 2 + x * 2 + 1] = y * offset - 0.5

        super().__init__(vertexData, [2])

        self.drawMode = GL_POINTS
        