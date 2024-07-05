from ..mesh import Mesh

def Cuboid(height=1, width=1, depth=1):
    """ Shape generator for creating a cuboid. """
    hh = height / 2
    hw = width / 2
    hd = depth / 2

    cuboid_vertices = [
        [  hw,  hh,  hd ], # R U F
        [  hw, -hh,  hd ], # R D F
        [  hw, -hh, -hd ], # R D B
        [  hw,  hh, -hd ], # R U B
        [ -hw,  hh,  hd ], # L U F
        [ -hw, -hh,  hd ], # L D F
        [ -hw, -hh, -hd ], # L D B
        [ -hw,  hh, -hd ]  # L U B
    ]

    cuboid_normals = [
        [  1,  0,  0 ], # R
        [ -1,  0,  0 ], # L
        [  0,  1,  0 ], # U
        [  0, -1,  0 ], # D
        [  0,  0,  1 ], # F
        [  0,  0, -1 ]  # B
    ]

    cuboid_uvs = [
        [ 0, 0 ], # T L
        [ 0, 1 ], # B L
        [ 1, 1 ], # B R
        [ 1, 0 ]  # T R
    ]

    cuboid_faces = [
        # Right Face
        [[ 0, 0, 0 ],
         [ 1, 1, 0 ],
         [ 2, 2, 0 ]],

        [[ 2, 2, 0 ],
         [ 3, 3, 0 ],
         [ 0, 0, 0 ]],

        # Left Face
        [[ 7, 0, 1 ],
         [ 6, 1, 1 ],
         [ 5, 2, 1 ]],

        [[ 5, 2, 1 ],
         [ 4, 3, 1 ],
         [ 7, 0, 1 ]],

        #  Up Face
        [[ 7, 0, 2 ],
         [ 4, 1, 2 ],
         [ 0, 2, 2 ]],

        [[ 0, 2, 2 ],
         [ 3, 3, 2 ],
         [ 7, 0, 2 ]],

        # Down Face
        [[ 5, 0, 3 ],
         [ 6, 1, 3 ],
         [ 2, 2, 3 ]],

        [[ 2, 2, 3 ],
         [ 1, 3, 3 ],
         [ 5, 0, 3 ]],

        # Front Face
        [[ 4, 0, 4 ],
         [ 5, 1, 4 ],
         [ 1, 2, 4 ]],

        [[ 1, 2, 4 ],
         [ 0, 3, 4 ],
         [ 4, 0, 4 ]],

        # Back Face
        [[ 3, 0, 5 ],
         [ 2, 1, 5 ],
         [ 6, 2, 5 ]],

        [[ 6, 2, 5 ],
         [ 7, 3, 5 ],
         [ 3, 0, 5 ]]
    ]

    return Mesh(vertices=cuboid_vertices, normals=cuboid_normals, uvs=cuboid_uvs, faces=cuboid_faces)
