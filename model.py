from OpenGL.GL import *
import numpy as np
from shader_utils import *
from matrix_utils import *
from ctypes import *
from material import *
from pyquaternion import *

# This class represents a generic 3D model defined by a vertex buffer
# which contains vertex, texture, and normal data.
class Model:
    def __init__(self, vertexData, vertexFormat, name=None):
        self.name = name
        self.vertexFormat = vertexFormat
        self.numVertices = int(vertexData.size / sum(vertexFormat))
        self.bufferStride = sizeof(c_float) * sum(vertexFormat)
        self.drawMode = GL_TRIANGLES

        self.material = Material()
        
        self.__pos = np.array([0, 0, 0], dtype="float32")
        self.__scale = np.array([1, 1, 1], dtype="float32")
        self.quat = Quaternion()

        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)
        self.vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)

        glBufferData(GL_ARRAY_BUFFER, vertexData, GL_STATIC_DRAW)

        offset = 0
        for i, size in enumerate(self.vertexFormat):
            glEnableVertexAttribArray(i)
            glVertexAttribPointer(
                i, 
                size, 
                GL_FLOAT, 
                GL_FALSE, 
                self.bufferStride, 
                c_void_p(sizeof(c_float)*offset)
            )
            offset += size

        glBindVertexArray(0)
        # needs to be initialized manually after creation
        self.pid = None

    # Move model in the direction and magnitude of vector `d`.
    def move(self, d):
        self.__pos += self.quat.rotate(d)

    # Rotate model by `deg` degrees around local axis `axis`.
    def rotate(self, deg, axis):
        r = np.deg2rad(deg)
        axis = self.quat.rotate(axis)
        self.quat = Quaternion(axis=axis, angle=r) * self.quat

    # Scale model using vector `s`, containing x, y, and z scale factors.
    def scale(self, s):
        self.__scale *= s

    # Set the absolute position `p` of the model in world coordinates.
    def setPosition(self, p):
        self.__pos = p

    def getModelMatrix(self):
        return (
            translationMatrix(self.__pos) * 
            self.quat.transformation_matrix * 
            scaleMatrix(self.__scale)
        )

    # Load and link the shaders for the model.
    # If a shader program already exists, make sure to
    # delete it before linking another one.
    def setShaders(self, vshader, fshader):
        self.pid = makeProgram({
            GL_VERTEX_SHADER : vshader,
            GL_FRAGMENT_SHADER : fshader
        })
        return self

    def draw(self, camera, light):
        glUseProgram(self.pid)

        # Send model, view, and projection matrices to pipeline
        uid = glGetUniformLocation(self.pid, "M")
        glUniformMatrix4fv(uid, 1, GL_TRUE, self.getModelMatrix())
        uid = glGetUniformLocation(self.pid, "V")
        glUniformMatrix4fv(uid, 1, GL_TRUE, camera.getViewMatrix())
        uid = glGetUniformLocation(self.pid, "P")
        glUniformMatrix4fv(uid, 1, GL_TRUE, camera.projMatrix)

        # Pass light direction vector to pipeline
        uid = glGetUniformLocation(self.pid, "LightDirection")
        glUniform3fv(uid, 1, light.direction)

        # Pass light colour vector to pipeline
        uid = glGetUniformLocation(self.pid, "LightColour")
        glUniform3fv(uid, 1, light.colour)

        # Pass eye/camera position to pipeline
        uid = glGetUniformLocation(self.pid, "ViewPosition")
        glUniform3fv(uid, 1, camera.pos)

        # Pass material information to pipeline
        uid = glGetUniformLocation(self.pid, "Ns")
        glUniform1f(uid, self.material.Ns)
        uid = glGetUniformLocation(self.pid, "Ni")
        glUniform1f(uid, self.material.Ni)
        uid = glGetUniformLocation(self.pid, "Ka")
        glUniform3fv(uid, 1, self.material.Ka)
        uid = glGetUniformLocation(self.pid, "Kd")
        glUniform3fv(uid, 1, self.material.Kd)
        uid = glGetUniformLocation(self.pid, "Ks")
        glUniform3fv(uid, 1, self.material.Ks)
        uid = glGetUniformLocation(self.pid, "Ke")
        glUniform3fv(uid, 1, self.material.Ke)
        uid = glGetUniformLocation(self.pid, "illum")
        glUniform1i(uid, self.material.illum)
    
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_CULL_FACE)

        glBindVertexArray(self.vao)
        glDrawArrays(self.drawMode, 0, self.numVertices)
        glBindVertexArray(0)

        glDisable(GL_DEPTH_TEST)
        glDisable(GL_CULL_FACE)
        glUseProgram(0)

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

        return Model(np.array(vdata, dtype="float32"), [3,2,3], name)
