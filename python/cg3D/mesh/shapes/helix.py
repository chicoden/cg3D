from ..mesh import Mesh
from ... import utils

def Helix(radius=1, thickness=0.5, turns=3, pitch=1, sides=12, ringrots=12):
    """ Shape generator for creating a helix. """
    helix_vertices = []
    helix_normals = []
    helix_uvs = []
    helix_faces = []

    path = []
    rotation = utils.TAU / ringrots
    for turn in range(0, ringrots):
        angle = rotation * turn
        path.append([utils.cos(angle), utils.sin(angle), 0])

    return Mesh(vertices=helix_vertices, normals=helix_normals, uvs=helix_uvs, faces=helix_faces)
