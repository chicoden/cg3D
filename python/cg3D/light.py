""" Library of light classes. """

from . import utils
import numpy as np

DIRECTIONAL = 0
POINT = 1
SPOT = 2

class DirectionalLight(object):
    """ Directional light class. """
    def __init__(self, direction=(-1, 1, 1), color=(255, 255, 255)):
        self.direction = utils.normalize(np.array(direction, dtype="float64"))
        self.color = np.array(color, dtype="float64") / 255
        super().__init__()

    def illuminate(self, camera, point, material, normal):
        Ia = material.ambient * self.color

        lambertian = max(0, np.dot(self.direction, normal))
        Id = lambertian * material.diffuse * self.color

        r = utils.reflect(self.direction, normal)
        v = utils.normalize(camera - point)
        spec_a = max(0, np.dot(r, v))
        Is = spec_a**material.gloss * material.specular * self.color

        return Ia + Id + Is

    def isvisible(self):
        #raise NotImplementedError
        return True

class PointLight(object):
    """ Point light class. """
    def __init__(self, position=(0, 0, 0), constant=1, linear=0, quadratic=1.5, color=(255, 255, 255)):
        self.position = np.array(position, dtype="float64")

        self.constant = constant
        self.linear = linear
        self.quadratic = quadratic

        self.color = np.array(color, dtype="float64") / 255
        super().__init__()

    def illuminate(self, camera, point, material, normal):
        Ia = material.ambient * self.color

        l = self.position - point
        d = np.linalg.norm(l)
        l /= d

        att = utils.clamp(1 / (self.constant + self.linear * d + self.quadratic * d * d), 0, 1)

        lambertian = max(0, np.dot(l, normal))
        Id = lambertian * material.diffuse * self.color

        r = utils.reflect(l, normal)
        v = utils.normalize(camera - point)
        spec_a = max(0, np.dot(r, v))
        Is = spec_a**material.gloss * material.specular * self.color

        return Ia + (Id + Is) * att

    def isvisible(self):
        #raise NotImplementedError
        return True

class SpotLight(object):
    """ Spotlight class. """
    def __init__(self, position=(0, 0, 1), direction=(0, 0, -1), cutoff_inner=10, cutoff_outer=30, color=(255, 255, 255), in_radians=False):
        self.position = np.array(position, dtype="float64")
        self.direction = utils.normalize(np.array(direction, dtype="float64"))

        self.cutoff_inner = np.cos(cutoff_inner) if in_radians else np.cos(np.radians(cutoff_inner))
        self.cutoff_outer = np.cos(cutoff_outer) if in_radians else np.cos(np.radians(cutoff_outer))
        self.cutoff_delta = self.cutoff_outer - self.cutoff_inner

        self.color = np.array(color, dtype="float64") / 255
        super().__init__()

    def illuminate(self, camera, point, material, normal):
        Ia = material.ambient * self.color

        l = utils.normalize(self.position - point)
        theta = np.dot(self.direction, -l)
        att = utils.clamp((theta - self.cutoff_outer) / self.cutoff_delta, 0, 1)

        lambertian = max(0, np.dot(l, normal))
        Id = lambertian * material.diffuse * self.color

        r = utils.reflect(l, normal)
        v = utils.normalize(camera - point)
        spec_a = max(0, np.dot(r, v))
        Is = spec_a**material.gloss * material.specular * self.color

        return Ia + (Id + Is) * att

    def isvisible(self):
        #raise NotImplementedError
        return True

def Light(light_type=POINT, *args, **kwargs):
    """ General light constructor. """
    if light_type == DIRECTIONAL:
        return DirectionalLight(*args, **kwargs)

    elif light_type == POINT:
        return PointLight(*args, **kwargs)

    elif light_type == SPOT:
        return SpotLight(*args, **kwargs)
