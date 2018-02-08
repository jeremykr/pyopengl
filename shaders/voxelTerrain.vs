#version 330 core

layout(location = 0) in vec3 pos;

uniform mat4 M, V, P;

out vec3 vert;

void main() {
    vert = pos;
    gl_Position = P * V * M * vec4(pos, 1.0);
}