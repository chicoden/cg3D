""" Contains most of the utilities. """

import numpy as np

TAU = 2 * np.pi

def clamp(x, rmin, rmax):
    """ Clamps x to between rmin and rmax. """
    return max(min_val, min(max_val, x))

def wrap(x, min_val, max_val):
    """ Wraps x between rmin and rmax. """
    return min_val + (x - min_val) % (max_val - min_val)

def normalize(v):
    """ Converts a vector to a unit vector while preserving direction. """
    return v / np.linalg.norm(v)

def reflect(l, n):
    """ Reflects vector l over vector n. """
    return 2 * np.dot(l, n) * n - l

def triangulate(poly):
    """ Earclipping method to triangulate simple polygons. """
    raise NotImplementedError

def tri_fill(a, b, c):
    """ Generator function for iterating over the pixels inside a triangle. """
    vert_bary = np.eye(3)
    a, b, c = sorted([[a, vert_bary[0]], [b, vert_bary[1]], [c, vert_bary[2]]], key=lambda vert: vert[0][1])

    ca = c[0] - a[0]
    ba = b[0] - a[0]
    cb = c[0] - b[0]

    edge1 = [a[0][0], a[1].copy(), 0, np.zeros(3)] # (a.pos.x, a.uv, 1 / slope(a --> c), uv step)
    edge2 = [a[0][0], a[1].copy(), 0, np.zeros(3)] # (a.pos.x, a.uv, 1 / slope(a --> b), uv step)
    edge3 = [b[0][0], b[1].copy(), 0, np.zeros(3)] # (b.pos.x, b.uv, 1 / slope(b --> c), uv step)

    if ca[1] != 0:
        edge1[3] = (c[1] - a[1]) / ca[1]
        edge1[2] = ca[0] / ca[1]

    if ba[1] != 0:
        edge2[3] = (b[1] - a[1]) / ba[1]
        edge2[2] = ba[0] / ba[1]

    if cb[1] != 0:
        edge3[3] = (c[1] - b[1]) / cb[1]
        edge3[2] = cb[0] / cb[1]

    swap = b[0][0] < a[0][0] + ba[1] * edge1[2]
    if swap: edge1, edge2 = edge2, edge1
    for y in range(int(a[0][1]), int(b[0][1])): # a.pos.y --> b.pos.y
        bary = edge1[1].copy()
        scan_width = edge2[0] - edge1[0]
        bary_step = edge2[1] - edge1[1]
        if scan_width > 0: bary_step /= scan_width
        for x in range(int(edge1[0]), int(edge2[0])):
            yield (x, y), bary
            bary += bary_step

        edge1[0] += edge1[2]
        edge1[1] += edge1[3]

        edge2[0] += edge2[2]
        edge2[1] += edge2[3]

    if swap: edge1 = edge3
    else: edge2 = edge3
    for y in range(int(b[0][1]), int(c[0][1])): # b.pos.y --> c.pos.y
        bary = edge1[1].copy()
        scan_width = edge2[0] - edge1[0]
        bary_step = edge2[1] - edge1[1]
        if scan_width > 0: bary_step /= scan_width
        for x in range(int(edge1[0]), int(edge2[0])):
            yield (x, y), bary
            bary += bary_step

        edge1[0] += edge1[2]
        edge1[1] += edge1[3]

        edge2[0] += edge2[2]
        edge2[1] += edge2[3]
