from ..mesh import Mesh
from .. import utils
import numpy as np

def Extrude(path=[(0, 0.666), (-0.5, -0.333), (0.5, -0.333)], depth=0.5):
    """ Shape generator for creating an extrusion. """
    extrude_vertices = []
    extrude_normals = []
    extrude_uvs = []
    extrude_faces = []

    offset = depth / 2
    triangles = utils.triangulate(path)

    extrude_vertices += [[*vert, offset] for vert in path] # Front face vertices
    extrude_vertices += [[*vert, -offset] for vert in path] # Back face vertices

    # Edge normals
    for index, a in enumerate(path):
        b = path[(index + 1) % len(path)]
        normal = [b[1] - a[1], a[0] - b[0]]
        dist = np.sqrt(normal[0] * normal[0] + normal[1] * normal[1])
        extrude_normals.append([*normal, 0])

    extrude_normals.append([0, 0, 1]) # Front face normal
    extrude_normals.append([0, 0, -1]) # Back face normal

    for index in range(0, len(path)):
        current_front_vertex = index
        next_front_vertex = (current_front_vertex + 1) % len(path)
        next_back_vertex = next_front_vertex + len(path)
        current_back_vertex = index + len(path)

        extrude_faces.append([
            [ current_front_vertex, -1, index ],
            [  current_back_vertex, -1, index ],
            [     next_back_vertex, -1, index ]
        ])

        extrude_faces.append([
            [     next_back_vertex, -1, index ],
            [    next_front_vertex, -1, index ],
            [ current_front_vertex, -1, index ]
        ])

    for triangle in triangles:
        # Front facing triangle
        extrude_faces.append([
            [triangle[0], -1, len(path)],
            [triangle[1], -1, len(path)],
            [triangle[2], -1, len(path)]
        ])

        # Backward facing triangle
        extrude_faces.append([
            [triangle[2] + len(path), -1, len(path) + 1],
            [triangle[1] + len(path), -1, len(path) + 1],
            [triangle[0] + len(path), -1, len(path) + 1]
        ])

    return Mesh(vertices=extrude_vertices, normals=extrude_normals, uvs=extrude_uvs, faces=extrude_faces)
