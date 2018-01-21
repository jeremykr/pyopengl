from OpenGL.GL import *
import numpy as np
from shader_utils import *
from matrix_utils import *
from ctypes import *

# This class represents a generic 3D model defined by a vertex buffer
# which contains vertex, texture, and normal data.
class Model:
    def __init__(self, name, vertexData):
        self.name = name
        self.numVertices = int(vertexData.size / 8)
        self.bufferStride = sizeof(c_float) * 8
        
        self.pos = np.array([0, 0, 0], dtype="float32")
        self.scale = np.array([1, 1, 1], dtype="float32")

        vaid = glGenVertexArrays(1)
        glBindVertexArray(vaid)
        self.vbuf = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbuf)
        glBufferData(GL_ARRAY_BUFFER, vertexData, GL_STATIC_DRAW)
        # needs to be initialized manually after creation
        self.pid = None

    # Load and link the shaders for the model.
    # If a shader program already exists, make sure to
    # delete it before linking another one.
    def setShaders(self, vshader, fshader):
        if self.pid:
            glDeleteProgram(self.pid)
        self.pid = makeProgram({
            GL_VERTEX_SHADER : vshader,
            GL_FRAGMENT_SHADER : fshader
        })
        return self

    def draw(self, viewMatrix, projMatrix):
        glUseProgram(self.pid)
        # Send model-view-projection (MVP) matrix to GPU
        modelMatrix = translationMatrix(self.pos) * scaleMatrix(self.scale)
        mvp = projMatrix * viewMatrix * modelMatrix
        mid = glGetUniformLocation(self.pid, "MVP")
        glUniformMatrix4fv(mid, 1, GL_TRUE, mvp)

        glEnableVertexAttribArray(0)
        glEnableVertexAttribArray(1)
        glEnableVertexAttribArray(2)

        glEnable(GL_DEPTH_TEST)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbuf)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, self.bufferStride, c_void_p(sizeof(c_float)*0))
        glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, self.bufferStride, c_void_p(sizeof(c_float)*3))
        glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, self.bufferStride, c_void_p(sizeof(c_float)*5))
        glDrawArrays(GL_TRIANGLES, 0, self.numVertices)
        glDisable(GL_DEPTH_TEST)

        glDisableVertexAttribArray(0)
        glDisableVertexAttribArray(1)
        glDisableVertexAttribArray(2)

    # Reads data from a Wavefront .obj file specified by `filename`
    # into a Model object.
    @staticmethod
    def fromObj(filename):
        data = []
        with open(filename) as f:
            data = [line.strip() for line in f.readlines()]
        
        name = "" # Model name from .obj file
        v = []  # Vertex coordinate data
        vt = [] # Texture data
        vn = [] # Normal data
        vdata = [] # Complete vertex data buffer

        for line in data:

            if line.startswith("o "):
                # Collect object name
                name = line[2:]

            elif line.startswith("v "):
                # Collect vertex coordinate data
                v.append(line.split()[1:])

            elif line.startswith("vt"):
                # Collect vertex texture data
                vt.append(line.split()[1:])

            elif line.startswith("vn"):
                # Collect vertex normal data
                vn.append(line.split()[1:])

            elif line.startswith("f "):
                # Organize values for vertex data
                triangle = line.split()[1:]
                for point in triangle:
                    point = [int(x)-1 for x in point.split("/")]
                    vdata += v[point[0]] + vt[point[1]] + vn[point[2]]

        return Model(name, np.array(vdata, dtype="float32"))
