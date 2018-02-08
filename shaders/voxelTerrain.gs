# version 330 core

layout(points) in;
layout(triangle_strip, max_vertices = 14) out;

in vec3 vert[];
out vec3 fvert;

uniform mat4 M, V, P;

void main() {
    float o = 1.0/255; //offset
    fvert = vert[0];

    vec4 in0 = gl_in[0].gl_Position;
    mat4 MVP = P * V * M;

    gl_Position = in0 + MVP * vec4(-o, o, o, 0);
    EmitVertex();
    gl_Position = in0 + MVP * vec4(o, o, o, 0);
    EmitVertex();
    gl_Position = in0 + MVP * vec4(-o, -o, o, 0);
    EmitVertex();
    gl_Position = in0 + MVP * vec4(o, -o, o, 0);
    EmitVertex();
    gl_Position = in0 + MVP * vec4(o, -o, -o, 0);
    EmitVertex();
    gl_Position = in0 + MVP * vec4(o, o, o, 0);
    EmitVertex();
    gl_Position = in0 + MVP * vec4(o, o, -o, 0);
    EmitVertex();
    gl_Position = in0 + MVP * vec4(-o, o, o, 0);
    EmitVertex();
    gl_Position = in0 + MVP * vec4(-o, o, -o, 0);
    EmitVertex();
    gl_Position = in0 + MVP * vec4(-o, -o, o, 0);
    EmitVertex();
    gl_Position = in0 + MVP * vec4(-o, -o, -o, 0);
    EmitVertex();
    gl_Position = in0 + MVP * vec4(o, -o, -o, 0);
    EmitVertex();
    gl_Position = in0 + MVP * vec4(-o, o, -o, 0);
    EmitVertex();
    gl_Position = in0 + MVP * vec4(o, o, -o, 0);
    EmitVertex();

    EndPrimitive();
}
