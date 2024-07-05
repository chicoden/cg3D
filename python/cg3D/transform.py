""" Library of transformation matrix generators. """

import numpy as np

def Identity():
    return np.array([[ 1, 0, 0, 0 ],
                     [ 0, 1, 0, 0 ],
                     [ 0, 0, 1, 0 ],
                     [ 0, 0, 0, 1 ]], dtype="float64")

def Scale(sx=1, sy=1, sz=1):
    return np.array([[ sx,  0,  0,  0 ],
                     [  0, sy,  0,  0 ],
                     [  0,  0, sz,  0 ],
                     [  0,  0,  0,  1 ]], dtype="float64")

def Shear(sxy=0, sxz=0, syx=0, syz=0, szx=0, szy=0):
    return np.array([[   1, syx, szx,   0 ],
                     [ sxy,   1, szy,   0 ],
                     [ sxz, syz,   1,   0 ],
                     [   0,   0,   0,   0 ]], dtype="float64")

def Translate(tx=0, ty=0, tz=0):
    return np.array([[  1,  0,  0, tx ],
                     [  0,  1,  0, ty ],
                     [  0,  0,  1, tz ],
                     [  0,  0,  0,  1 ]], dtype="float64")

def RotateAboutX(rx=0, in_radians=False):
    rad = rx if in_radians else np.radians(rx)
    c, s = np.cos(rad), np.sin(rad)

    return np.array([[  1,  0,  0,  0 ],
                     [  0,  c,  s,  0 ],
                     [  0, -s,  c,  0 ],
                     [  0,  0,  0,  1 ]], dtype="float64")

def RotateAboutY(ry=0, in_radians=False):
    rad = ry if in_radians else np.radians(ry)
    c, s = np.cos(rad), np.sin(rad)

    return np.array([[  c,  0, -s,  0 ],
                     [  0,  1,  0,  0 ],
                     [  s,  0,  c,  0 ],
                     [  0,  0,  0,  1 ]], dtype="float64")

def RotateAboutZ(rz=0, in_radians=False):
    rad = rz if in_radians else np.radians(rz)
    c, s = np.cos(rad), np.sin(rad)

    return np.array([[  c, -s,  0,  0 ],
                     [  s,  c,  0,  0 ],
                     [  0,  0,  1,  0 ],
                     [  0,  0,  0,  1 ]], dtype="float64")


def RotateAboutAxis(ax=1, ay=0, az=0, r=0, in_radians=False):
    theta = np.arctan2(az, ax)
    phi = np.arctan2(ay, np.sqrt(ax * ax + az * az))

    theta_rot = RotateAboutY(theta, in_radians=True)
    phi_rot = RotateAboutZ(phi, in_radians=True)
    axis_rot = RotateAboutX(r, in_radians=in_radians)

    return np.dot(theta_rot, np.dot(phi_rot, np.dot(axis_rot, np.dot(phi_rot.T, theta_rot.T))))

def TransformRelative(transform=Identity(), ox=0, oy=0, oz=0):
    return np.dot(Translate(ox, oy, oz), np.dot(transform, Translate(-ox, -oy, -oz)))

def Perspective(fov=90, aspect=1, near=0.01, far=100, in_radians=False):
    rad = fov if in_radians else np.radians(fov)

    f = 1 / np.tan(rad / 2)
    q = 1 / (near - far)

    return np.array([[ f / aspect,          0,           0,          0 ],
                     [          0,          f,           0,          0 ],
                     [          0,          0,           q,   near * q ],
                     [          0,          0,          -1,          0 ]], dtype="float64")

def Orthographic(fov=2, aspect=1, near=0.01, far=100):
    f = 2 / fov
    q = 1 / (near - far)

    return np.array([[ f / aspect,          0,           0,          0 ],
                     [          0,          f,           0,          0 ],
                     [          0,          0,           q,   near * q ],
                     [          0,          0,           0,          1 ]], dtype="float64")

def Combine(*transforms):
    """ Combines a list of transformation matrices. """
    mat = Identity()
    for transform in transforms:
        mat = np.dot(transform, mat)

    return mat

def Tabulate(mat):
    """ Generates a pretty ASCII table from a matrix of values. """
    str_mat = [[str(element) for element in row] for row in mat]
    cell_width = max([len(str_element) for str_row in str_mat for str_element in str_row])

    divider = ("+-" + ("-" * cell_width + "-+-") * len(mat[0]))[0:-1]
    table = divider

    for str_row in str_mat:
        table += ("\n| " + "".join([" " * (cell_width - len(str_element)) + str_element + " | " for str_element in str_row]))[0:-1]
        table += "\n" + divider

    return table
