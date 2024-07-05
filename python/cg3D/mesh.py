""" Meshes library. """

from .material import Material
from . import transform
from . import utils
import numpy as np

class Mesh(object):
    """
    Mesh class.

    Structure of mesh faces:

    [[  v1, vt1, vn1 ],
     [  v2, vt2, vn2 ],
     [  v3, vt3, vn3 ]]

    v1, v2, v3 are indices to the face's vertices.
    vt1, vt2, vt3 are the indices to the face's vertices' uvs.
    vn1, vn2, vn3 are indices to the face's vertices' normals.

    Note: faces must be triangles, however, Model() will automatically triangulate polygons.
    It is only guaranteed to work on convex polygons though!
    """

    def __init__(self, vertices=[], normals=[], uvs=[], faces=[], material=Material()):
        self.vertices = np.array([[*vertex, 1] for vertex in vertices], dtype="float64")
        self.normals = np.array([[*normal, 0] for normal in normals], dtype="float64")
        self.uvs = np.array(uvs, dtype="float64")
        self.faces = np.array(faces, dtype="int64")
        self.material = material
        self.model_mat = transform.Identity()

    def calculate_normals(self):
        """ Calculates face normals. Face vertices must be listed counterclockwise. """
        face_normals = []
        for index, face in enumerate(self.faces):
            a = self.vertices[face[0][0]][:3]
            b = self.vertices[face[1][0]][:3]
            c = self.vertices[face[2][0]][:3]

            face_normal = np.cross(b - a, c - a)
            if np.sum(np.abs(face_normal)) > 0:
                face_normal = utils.normalize(face_normal)
                face_normals.append([*face_normal, 0])

                normal_index = len(face_normals) - 1
                self.faces[index][0][2] = normal_index
                self.faces[index][1][2] = normal_index
                self.faces[index][2][2] = normal_index

        self.normals = np.array(face_normals, dtype="float64")

    # smooth_normals() --- Very costly!
    # calculate_uvs(mode=Planar,Cubic,Cylindrical,Spherical)

    def add_vertex(self, vertex):
        self.vertices = np.append(self.vertices, np.array([[*vertex, 1]], dtype="float64"), axis=0)

    def delete_vertex(self, index):
        self.vertices = np.delete(self.vertices, index, axis=0)

    def get_vertex(self, index):
        return self.vertices[index]

    def add_normal(self, normal):
        self.normals = np.append(self.normals, np.array([[*normal, 0]], dtype="float64"), axis=0)

    def delete_normal(self, index):
        self.normals = np.delete(self.normals, index, axis=0)

    def get_normal(self, index):
        return self.normals[index]

    def add_uv(self, uv):
        self.uvs = np.append(self.uvs, np.array([uv], dtype="float64"), axis=0)

    def delete_uv(self, index):
        self.uvs = np.delete(self.uvs, index, axis=0)

    def get_uv(self, index):
        return self.uvs[index]

    def add_face(self, face):
        self.faces = np.append(self.faces, np.array([face], dtype="int64"), axis=0)

    def delete_face(self, index):
        self.faces = np.delete(self.faces, index, axis=0)

    def get_face(self, index):
        return self.faces[index]

    def transform(self, transform):
        """ Applies a 4x4 transformation matrix to the mesh. """
        self.model_mat = np.dot(transform, self.model_mat)
