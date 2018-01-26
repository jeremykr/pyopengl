#version 330 core

in VertexData {
    vec3 pos;
    vec2 uv;
    vec4 normal;
} v;

uniform mat4 M, V;
uniform vec3 LightDirection;
uniform vec3 LightColour;
uniform vec3 ViewPosition;
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
    float Id = 0.0;
    float Is = 0.0;
    if (illum > 0) {
        // Calculate diffuse shading
        vec4 L = -normalize(vec4(LightDirection, 0));
        vec4 N = normalize(M * v.normal);
        Id = clamp(dot(L, N), 0, 1);

        if (illum == 2 && Id > 0) {
            // Calculate Blinn-Phong shading
            vec4 V = normalize(vec4(ViewPosition, 0));
            vec4 H = normalize(L + V);
            Is = pow(max(dot(H, N), 0), Ns);
        }
    }
    color = Kd * (Ka*Ia + Kd*Id*LightColour + Ks*Is*LightColour);
}