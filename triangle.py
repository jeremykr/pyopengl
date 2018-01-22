from OpenGL.GL import *
import numpy as np
from shader_utils import *
from matrix_utils import *
from ctypes import *

class Triangle:
    def __init__(self):
        self.pos = np.array([0, 0, 0], dtype="float32")
        self.scale = np.array([1, 1, 1], dtype="float32")
        vbuf_data = np.array([
            -1, -1, 0,
            1, -1, 0,
            0, 1, 0
        ], dtype="float32")

        vaid = glGenVertexArrays(1)
        glBindVertexArray(vaid)
        self.vbuf = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbuf)
        glBufferData(GL_ARRAY_BUFFER, vbuf_data, GL_STATIC_DRAW)

        self.pid = makeProgram({
            GL_VERTEX_SHADER : "triangle.vs",
            GL_FRAGMENT_SHADER : "triangle.fs"
        })

        del vbuf_data, vaid

    def draw(self, viewMatrix, projMatrix, light):
        glUseProgram(self.pid)
        
        modelMatrix = translationMatrix(self.pos) * scaleMatrix(self.scale)
        mvp = projMatrix * viewMatrix * modelMatrix
        mid = glGetUniformLocation(self.pid, "MVP")
        glUniformMatrix4fv(mid, 1, GL_TRUE, mvp)

        glEnableVertexAttribArray(0)
        glEnable(GL_DEPTH_TEST)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbuf)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, c_void_p(0))
        glDrawArrays(GL_TRIANGLES, 0, 3)
        glDisable(GL_DEPTH_TEST)
        glDisableVertexAttribArray(0)