from ..mesh import Mesh
from .. import utils
import numpy as np

def Cylinder(height=1, radius=0.5, sides=12):
    """ Shape generator for creating a cylinder. """
    cylinder_vertices = []
    cylinder_normals = []
    cylinder_uvs = []
    cylinder_faces = []

    hh = height / 2
    edge_vertices = sides * 2

    angle_step = utils.TAU / sides
    half_angle_step = angle_step / 2
    angle = 0

    u_step = 1 / sides
    u = 0

    top_vertex = edge_vertices
    bottom_vertex = top_vertex + 1

    top_normal = sides
    bottom_normal = top_normal + 1

    for side in range(0, sides):
        c, s = np.cos(angle), np.sin(angle)

        normal_angle = angle + half_angle_step
        normal_c, normal_s = np.cos(normal_angle), np.sin(normal_angle)

        # Side vertices
        cylinder_vertices.append([ c * radius,  hh, s * radius ])
        cylinder_vertices.append([ c * radius, -hh, s * radius ])

        # Side normal
        cylinder_normals.append([ normal_c, 0, normal_s ])

        # Side UVs
        cylinder_uvs.append([ u, 0 ])
        cylinder_uvs.append([ u, 1 ])

        current_top_vertex = side * 2
        current_bottom_vertex = current_top_vertex + 1
        next_top_vertex = (current_bottom_vertex + 1) % edge_vertices
        next_bottom_vertex = (next_top_vertex + 1) % edge_vertices

        current_top_uv = current_top_vertex
        current_bottom_uv = current_top_uv + 1
        next_top_uv = current_bottom_uv + 1
        next_bottom_uv = next_top_uv + 1

        side_normal = side

        # Top face
        cylinder_faces.append([
            [         top_vertex, next_bottom_uv, top_normal ],
            [    next_top_vertex,    next_top_uv, top_normal ],
            [ current_top_vertex, current_top_uv, top_normal ]
        ])

        # Side face
        cylinder_faces.append([
            [       next_top_vertex,       next_top_uv, side_normal ],
            [    next_bottom_vertex,    next_bottom_uv, side_normal ],
            [ current_bottom_vertex, current_bottom_uv, side_normal ]
        ])

        cylinder_faces.append([
            [ current_bottom_vertex, current_bottom_uv, side_normal ],
            [    current_top_vertex,    current_top_uv, side_normal ],
            [       next_top_vertex,       next_top_uv, side_normal ]
        ])

        # Bottom face
        cylinder_faces.append([
            [    next_bottom_vertex,    next_top_uv, bottom_normal ],
            [         bottom_vertex, next_bottom_uv, bottom_normal ],
            [ current_bottom_vertex, current_top_uv, bottom_normal ]
        ])

        angle += angle_step
        u += u_step

    # Top and bottom vertices
    cylinder_vertices.append([ 0,  hh, 0 ])
    cylinder_vertices.append([ 0, -hh, 0 ])

    cylinder_uvs.append([ 1, 0 ])
    cylinder_uvs.append([ 1, 1 ])

    # Top and bottom normals
    cylinder_normals.append([ 0,  1, 0 ])
    cylinder_normals.append([ 0, -1, 0 ])

    return Mesh(vertices=cylinder_vertices, normals=cylinder_normals, uvs=cylinder_uvs, faces=cylinder_faces)
