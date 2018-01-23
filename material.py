import numpy as np

class Material:
    def __init__(self):
        self.name = "Default material"
        # specular exponent, usually between 0 and 1000
        self.Ns = 100.0
        # ambience
        self.Ka = np.ones(3, dtype="float32")
        # diffusion
        self.Kd = np.full(3, 0.5, dtype="float32")
        # specular reflectivity
        self.Ks = np.full(3, 0.5, dtype="float32")
        # light emission
        self.Ke = np.zeros(3, dtype="float32")
        # optical density / index of refraction
        self.Ni = 1.0
        # dissolve / opacity,
        # with 1 being completely opaque and 0 being transparent
        self.d = 1.0

        # Taken from https://people.cs.clemson.edu/~dhouse/courses/405/docs/brief-mtl-file-format.html
        
        # 0 -- Constant colour illumination model.
        #       color = Kd

        # 1 -- Diffuse model using Lambertian shading.
        # The color includes an ambient and diffuse shading term for each light source.
        #       color = KaIa + Kd { SUM j=1..ls, (N * Lj)Ij }

        # 2 -- Diffuse & specular model with Lambertian and Blinn-Phong shading.
        # The color includes an ambient constant term and a diffuse and specular shading term for each light source.
        #       color = KaIa + Kd { SUM j=1..ls, (N*Lj)Ij } + Ks { SUM j=1..ls, ((H*Hj)^Ns)Ij }

        self.illum = 2

    # Loads information from a .mtl file into a Material object.
    @staticmethod
    def fromMtl(filename):
        data = []
        with open(filename) as f:
            data = [line.strip() for line in f.readlines()]

        m = Material()

        for line in data:
            if line.startswith("newmtl "):
                m.name = line[7:]
            elif line.startswith("K"):
                vec = np.array([float(x) for x in line[3:].split()])
                if line.startswith("Ka "): m.Ka = vec
                elif line.startswith("Kd "): m.Kd = vec
                elif line.startswith("Ks "): m.Ks = vec
                elif line.startswith("Ke "): m.Ke = vec
            elif line.startswith("Ni "):
                m.Ni = float(line[3:])
            elif line.startswith("d "):
                m.d = float(line[2:])
            elif line.startswith("illum "):
                m.illum = int(line[6:])

        return m