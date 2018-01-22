#version 330 core

layout(location = 0) in vec3 pos;
layout(location = 1) in vec2 uv;
layout(location = 2) in vec3 normal;

out VertexData {
    vec2 uv;
    vec4 normal;
} v;

uniform mat4 M, V, P;

void main() {
    gl_Position = P * V * M * vec4(pos, 1.0);
    
    v.uv = uv;
    v.normal = normalize(vec4(normal, 0));
}