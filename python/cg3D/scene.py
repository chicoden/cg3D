""" Scene library. """

class Scene(object):
    def __init__(self, meshes={}, lights={}):
        self.meshes = meshes
        self.lights = lights

    def add_mesh(self, mesh_id, mesh):
        self.meshes.update([(mesh_id, mesh)])

    def delete_mesh(self, mesh_id):
        del self.meshes[mesh_id]

    def add_light(self, light_id, light):
        self.lights.update([(light_id, light)])

    def delete_light(self, light_id):
        del self.lights[light_id]
