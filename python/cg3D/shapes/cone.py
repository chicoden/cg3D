from ..mesh import Mesh
from .. import utils
import numpy as np

def Cone(height=1, base=0.5, sides=12):
    """ Shape generator for creating a cone. """
    cone_vertices = []
    cone_normals = []
    cone_uvs = []
    cone_faces = []

    normal = utils.normalize([ 1 / base, 1 / height ])

    angle_step = utils.TAU / sides
    half_angle_step = angle_step / 2
    angle = 0

    u_step = 1 / sides
    u = 0

    top_vertex = sides
    bottom_vertex = top_vertex + 1

    for side in range(0, sides):
        c, s = np.cos(angle), np.sin(angle)

        normal_angle = angle + half_angle_step
        normal_c, normal_s = np.cos(normal_angle), np.sin(normal_angle)

        # Side vertex
        cone_vertices.append([ c * base, 0, s * base ])

        # Side normal
        cone_normals.append([ normal_c * normal[0], normal[1], normal_s * normal[0] ])

        # Side UVs
        cone_uvs.append([ u, 0 ])
        cone_uvs.append([ u, 1 ])

        current_vertex = side
        next_vertex = (side + 1) % sides

        current_top_uv = side * 2
        current_bottom_uv = current_top_uv + 1
        next_top_uv = current_bottom_uv + 1
        next_bottom_uv = next_top_uv + 1

        side_normal = side
        bottom_normal = sides

        # Side face
        cone_faces.append([
            [     top_vertex,       next_top_uv, side_normal ],
            [    next_vertex,    next_bottom_uv, side_normal ],
            [ current_vertex, current_bottom_uv, side_normal ]
        ])

        # Bottom face
        cone_faces.append([
            [    next_vertex,    next_top_uv, bottom_normal ],
            [  bottom_vertex, next_bottom_uv, bottom_normal ],
            [ current_vertex, current_top_uv, bottom_normal ]
        ])

        angle += angle_step
        u += u_step

    # Top and bottom vertices
    cone_vertices.append([ 0, height, 0 ])
    cone_vertices.append([ 0,      0, 0 ])

    cone_uvs.append([ 1, 0 ])
    cone_uvs.append([ 1, 1 ])

    # Bottom normal
    cone_normals.append([ 0, -1, 0 ])

    return Mesh(vertices=cone_vertices, normals=cone_normals, uvs=cone_uvs, faces=cone_faces)
