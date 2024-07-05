""" Camera library. """

from . import transform
import numpy as np

PERSPECTIVE = 0
ORTHOGRAPHIC = 1

class PerspectiveCamera(object):
    """ Perspective camera class. """
    def __init__(self, fov=90, near=0.01, far=100, in_radians=False):
        self.view_mat = transform.Identity()
        self.proj_mat = transform.Identity()

        self.fov = fov if in_radians else np.radians(fov)

        self.near = near
        self.far = far

        self.camera_type = PERSPECTIVE

        super().__init__()

    def _set_proj(self, aspect):
        self.proj_mat = transform.Perspective(self.fov, aspect, self.near, self.far, in_radians=True)

    def transform(self, transform):
        """ Applies a 4x4 transformation matrix to the camera. """
        self.view_mat = np.dot(np.linalg.inv(transform), self.view_mat)

class OrthographicCamera(object):
    """
    Orthographic camera class.
    Note: an orthographic camera's fov is a height measurement and not an angle.
    """
    def __init__(self, fov=2, near=0.01, far=100):
        self.view_mat = transform.Identity()
        self.proj_mat = transform.Identity()

        self.fov = fov

        self.near = near
        self.far = far

        self.camera_type = ORTHOGRAPHIC

        super().__init__()

    def _set_proj(self, aspect):
        self.proj_mat = transform.Orthographic(self.fov, aspect, self.near, self.far)

    def transform(self, transform):
        """ Applies a 4x4 transformation matrix to the camera. """
        self.view_mat = np.dot(np.linalg.inv(transform), self.view_mat)

def Camera(camera_type=PERSPECTIVE, *args, **kwargs):
    """ General camera constructor. """
    if camera_type == PERSPECTIVE:
        return PerspectiveCamera(*args, **kwargs)

    elif camera_type == ORTHOGRAPHIC:
        return OrthographicCamera(*args, **kwargs)
