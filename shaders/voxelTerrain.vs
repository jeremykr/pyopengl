#version 330 core

layout(location = 0) in vec2 pos;

uniform mat4 M, V, P;

void main() {
    gl_Position = P * V * M * vec4(pos.x, 0.0, pos.y, 1.0);
}