from ..mesh import Mesh
from .. import utils

def Torus(radius=1, thicknes=0.25, sides=12, tube_sides=12):
    """ Shape generator for creating a torus. """
    torus_vertices = []
    torus_normals = []
    torus_uvs = []
    torus_faces = []

    return Mesh(vertices=torus_vertices, normals=torus_normals, uvs=torus_uvs, faces=torus_faces)
