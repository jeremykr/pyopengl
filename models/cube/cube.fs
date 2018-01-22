#version 330 core

in VertexData {
    vec2 uv;
    vec4 normal;
} v;

uniform mat4 M;
uniform vec3 LightDirection;
uniform vec3 LightColour;
uniform float Ns;
uniform float Ni;
uniform vec3 Ka;
uniform vec3 Ks;
uniform vec3 Kd;
uniform vec3 Ke;
uniform int illum;

out vec3 color;

void main() {
    float Ia = 0.05;
    // TODO: Implement Blinn-Phong shading
    if (illum > 0) {
        vec4 L = vec4(LightDirection, 1);
        vec4 N = M * v.normal;
        float cosTheta = clamp(-dot(L, N), 0, 1);
        color = Ka*Ia + Kd * LightColour * cosTheta;
    } else {
        color = Kd;
    }
}