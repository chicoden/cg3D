from ..mesh import Mesh
from ... import utils

def Sphere(radius=1, sides=12, slices=12):
    """ Shape generator for creating a sphere. """
    sphere_vertices = []
    sphere_normals = []
    sphere_uvs = []
    sphere_faces = []

    return Mesh(vertices=sphere_vertices, normals=sphere_normals, uvs=sphere_uvs, faces=sphere_faces)
