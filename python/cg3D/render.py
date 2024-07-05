""" Rendering library. """

from . import transform, utils
from PIL import Image
import numpy as np

PERSPECTIVE = 0
ORTHOGRAPHIC = 1

class Renderer(object):
    def __init__(self, resolution=(800, 600), bgcolor=(0, 0, 0)):
        self.bgcolor = np.array(bgcolor, dtype="uint8")

        self.resolution = resolution
        self.x_center = self.resolution[0] / 2
        self.y_center = self.resolution[1] / 2
        self.aspect = self.resolution[0] / self.resolution[1]

        self.canvas = np.zeros((self.resolution[1], self.resolution[0], 3), dtype="uint8") + self.bgcolor
        self.depth_buf = np.ones((self.resolution[1], self.resolution[0]), dtype="float64")

    def render(self, scene, camera):
        """ Renders the scene from the perspective of the camera onto the renderer's canvas. """
        camera._set_proj(self.aspect)
        cam_pos = -camera.view_mat.T[3][:3]
        for mesh in scene.meshes.values():
            world_vertices = np.dot(mesh.model_mat, mesh.vertices.T).T
            clip_vertices = np.dot(camera.proj_mat, np.dot(camera.view_mat, world_vertices.T))

            # Divide by w
            screen_vertices = clip_vertices
            screen_vertices[3] = 1 / screen_vertices[3]
            screen_vertices[0] *= screen_vertices[3]
            screen_vertices[1] *= screen_vertices[3]

            # NDC to screen coordinates
            screen_vertices[0] = self.x_center + screen_vertices[0] * self.resolution[0]
            screen_vertices[1] = self.y_center - screen_vertices[1] * self.resolution[1]

            # Untranspose
            screen_vertices = screen_vertices.T

            world_normals = np.dot(np.linalg.inv(mesh.model_mat).T, mesh.normals.T).T
            world_normals /= np.linalg.norm(world_normals, axis=1).reshape((len(world_normals), 1))

            for face_id, face in enumerate(mesh.faces):
                # Eliminate faces which are obviously not visible
                face_nor = (world_normals[face[0][2]][:3] + world_normals[face[1][2]][:3] + world_normals[face[2][2]][:3]) / 3
                if face_nor[2] > 0:
                    # Vertex A's attributes
                    a_inv_z = screen_vertices[face[0][0]][3]
                    a_depth = screen_vertices[face[0][0]][2]
                    a_pos = world_vertices[face[0][0]][:3]
                    #a_uv = mesh.uvs[face[0][1]]
                    a_nor = world_normals[face[0][2]][:3]

                    # Vertex B's attributes
                    b_inv_z = screen_vertices[face[1][0]][3]
                    b_depth = screen_vertices[face[1][0]][2]
                    b_pos = world_vertices[face[1][0]][:3]
                    #b_uv = mesh.uvs[face[1][1]]
                    b_nor = world_normals[face[1][2]][:3]

                    # Vertex C's attributes
                    c_inv_z = screen_vertices[face[2][0]][3]
                    c_depth = screen_vertices[face[2][0]][2]
                    c_pos = world_vertices[face[2][0]][:3]
                    #c_uv = mesh.uvs[face[2][1]]
                    c_nor = world_normals[face[2][2]][:3]

                    # Prepare vertex attributes for perspective correct interpolation
                    a_depth *= a_inv_z
                    a_pos *= a_inv_z
                    #a_uv *= a_inv_z
                    a_nor *= a_inv_z

                    b_depth *= b_inv_z
                    b_pos *= b_inv_z
                    #b_uv *= b_inv_z
                    b_nor *= b_inv_z

                    c_depth *= c_inv_z
                    c_pos *= c_inv_z
                    #c_uv *= c_inv_z
                    c_nor *= c_inv_z

                    for point, bary in utils.tri_fill(screen_vertices[face[0][0]][:2], screen_vertices[face[1][0]][:2], screen_vertices[face[2][0]][:2]):
                        x, y = int(point[0]), int(point[1])
                        if x >= 0 and x < self.resolution[0] and y >= 0 and y < self.resolution[1]:
                            # Interpolate
                            frag_depth = a_depth * bary[0] + b_depth * bary[1] + c_depth * bary[2]
                            frag_pos = a_pos * bary[0] + b_pos * bary[1] + c_pos * bary[2]
                            #frag_uv = a_uv * bary[0] + b_uv * bary[1] + c_uv * bary[2]
                            frag_nor = a_nor * bary[0] + b_nor * bary[1] + c_nor * bary[2]

                            # Perspective correction
                            frag_inv_z = a_inv_z * bary[0] + b_inv_z * bary[1] + c_inv_z * bary[2]
                            frag_depth /= frag_inv_z
                            frag_pos /= frag_inv_z
                            #frag_uv /= frag_inv_z
                            frag_nor /= frag_inv_z

                            if frag_depth < self.depth_buf[y][x]:
                                self.depth_buf[y][x] = frag_depth

                                frag_shade = np.zeros(3)
                                for light in scene.lights.values():
                                    frag_shade += light.illuminate(cam_pos, frag_pos, mesh.material, frag_nor)

                                self.canvas[y][x] = np.array(np.clip(frag_shade * 255, 0, 255), dtype="uint8")

                print("Face {0} of {1} complete.".format(face_id + 1, len(mesh.faces))) # DEBUG

    def save(self, path, fmt="png"):
        render_img = Image.fromarray(self.canvas)

        # Add on the extension if it isn't present
        if path.split(".")[-1].lower() != fmt.lower():
            path += "." + fmt.lower()

        render_img.save(path)

    def clear(self):
        """ Resets the canvas and depth buffer. """
        self.canvas = np.zeros((self.resolution[1], self.resolution[0], 3), dtype="uint8") + self.bgcolor
        self.depth_buf = np.ones((self.resolution[1], self.resolution[0]), dtype="float64")
