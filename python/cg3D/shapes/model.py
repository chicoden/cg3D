from ..mesh import Mesh

def Model(file_path):
    """ Shape generator for loading models in Wavefront OBJ format. """
    file = open(file_path, "r")
    lines = file.read().split("\n")
    file.close()

    v  = []
    vn = []
    vt = []
    f  = []

    for line in lines:
        tokens = [token for token in line.split(" ") if token != ""]
        if len(tokens) > 0:
            stack = tokens[0]
            if stack == "v":
                elements = [float(element) for element in tokens[1:4]]
                if len(elements) >= 3:
                    v.append(elements[:3])

            elif stack == "vt":
                elements = [float(element) for element in tokens[1:3]]
                if len(elements) >= 2:
                    vt.append(elements[:2])

            elif stack == "vn":
                elements = [float(element) for element in tokens[1:4]]
                if len(elements) >= 3:
                    vn.append(elements[:3])

            elif stack == "f":
                elements = [[int(sub_element) - 1 if sub_element != "" else -1 for sub_element in element.split("/")] for element in tokens[1:]]
                for index, sub_elements in enumerate(elements):
                    elements[index] += [-1 for undefined_sub_element in range(0, 3 - len(sub_elements))]

                if len(elements) == 3:
                    f.append(elements)

                # Triangulate if there are more than three vertices
                elif len(elements) > 3:
                    triangles = []
                    for idx, vert in enumerate(elements[1:-1]):
                        triangles.append([elements[0], vert, elements[idx + 2]])

                    f += triangles

    return Mesh(vertices=v, normals=vn, uvs=vt, faces=f)
