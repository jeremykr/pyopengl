#version 330 core

in vec3 fvert;

uniform sampler2D tex;
uniform mat4 M;
out vec4 color;

void main() {
    color = texture2D(tex, vec2(fvert.x, fvert.z));
}