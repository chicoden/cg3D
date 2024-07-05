""" Material library. """

from . import utils
from PIL import Image
import numpy as np

CLAMP = 0
WRAP = 1

class Texture(object):
    """ Texture class. """
    def __init__(self, path, mode=CLAMP):
        self.image = Image.open(path)
        if self.image.mode != "RGB":
            self.image = self.image.convert("RGB")

        self.buffer = np.array(self.image, dtype="float64") / 255
        self.mode = mode
        super().__init__()

    def sample(self, u, v):
        """ Sample the texture at (u, v). u and v are from 0 to 1. """
        u = utils.clamp(u, 0, 1) if self.mode == CLAMP else utils.wrap(u, 0, 1)
        v = utils.clamp(v, 0, 1) if self.mode == CLAMP else utils.wrap(v, 0, 1)
        x, y = int((self.image.size[0] - 1) * u), int((self.image.size[1] - 1) * v)
        return self.buffer[y][x]

    def __str__(self):
        return "<texture map at {}>".format(hex(id(self)))

    def __repr__(self):
        return self.__str__()

class Material(object):
    """ Material class. """
    def __init__(self, ambient=(0, 0, 0), diffuse=(255, 255, 255), specular=(0, 0, 0), gloss=0, map_ambient=None, map_diffuse=None, map_specular=None, map_gloss=None, map_bump=None):
        self.ambient = np.array(ambient, dtype="float64") / 255
        self.diffuse = np.array(diffuse, dtype="float64") / 255
        self.specular = np.array(specular, dtype="float64") / 255
        self.gloss = gloss

        self.map_ambient = map_ambient
        self.map_diffuse = map_diffuse
        self.map_specular = map_specular
        self.map_gloss = map_gloss
        self.map_bump = map_bump

        super().__init__()
