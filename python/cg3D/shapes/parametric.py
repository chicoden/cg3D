from ..mesh import Mesh

def Parametric(func, diff=None, u_min=0, v_min=0, u_max=1, v_max=1, u_res=50, v_res=50):
    """ Shape generator for creating a mesh of a parametric surface. """
    parametric_vertices = []
    parametric_normals = []
    parametric_uvs = []
    parametric_faces = []

    return Mesh(vertices=parametric_vertices, normals=parametric_normals, uvs=parametric_uvs, faces=parametric_faces)

"""
verts = []
v = settings.v_min
for t1 in range(0, settings.v_steps):
    u = settings.u_min
    slice = []
    for t2 in range(0, settings.u_steps):
        slice.append(ParametricSurface(u, v))
        u += settings.u_step

    verts += slice
    v += settings.v_step

cell_index = lambda x, y, r: y * r + x
faces = []
for i in range(0, settings.v_steps - 1):
    for j in range(0, settings.u_steps - 1):
        v1 = cell_index(j    , i    , settings.u_steps)
        v2 = cell_index(j    , i + 1, settings.u_steps)
        v3 = cell_index(j + 1, i + 1, settings.u_steps)
        v4 = cell_index(j + 1, i    , settings.u_steps)
        faces.append([v1, v2, v3])
        faces.append([v3, v4, v1])
"""
