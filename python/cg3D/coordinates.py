""" Coordinate system classes and conversion utilities. """

import math

RADIANS = 0
DEGREES = 1

class Cartesian(object):
    """ Class for cartesian coordinates. """
    def __init__(self, x, y, z, angle_mode=DEGREES):
        self.x = x
        self.y = y
        self.z = z

        self.angle_mode = angle_mode

        super().__init__()

    def to_cartesian(self):
        return Cartesian(self.x, self.y, self.z, self.angle_mode)

    def to_cylindrical(self):
        theta = math.atan2(self.z, self.x)
        rho = math.sqrt(self.x * self.x + self.z * self.z)

        theta = theta if self.angle_mode == RADIANS else math.degrees(theta)

        return Cylindrical(theta, self.y, rho, self.angle_mode)
    
    def to_spherical(self):
        theta = math.atan2(self.z, self.x)
        rho = math.sqrt(self.x * self.x + self.z * self.z)
        phi = math.atan2(self.y, rho)
        rho = math.sqrt(rho * rho + self.y * self.y)

        theta = theta if self.angle_mode == RADIANS else math.degrees(theta)
        phi = phi if self.angle_mode == RADIANS else math.degrees(phi)

        return Spherical(theta, phi, rho, self.angle_mode)

    def __str__(self):
        return "Cartesian(x={0}, y={1}, z={2}, angle_mode={3})".format(self.x, self.y, self.z, "RADIANS" if self.angle_mode == RADIANS else "DEGREES")

    def __repr__(self):
        return self.__str__()

class Cylindrical(object):
    """ Class for cylindrical coordinates. """
    def __init__(self, theta, y, rho, angle_mode=DEGREES):
        self.theta = theta
        self.y = y
        self.rho = rho

        self.angle_mode = angle_mode

        super().__init__()

    def to_cartesian(self):
        theta = self.theta if self.angle_mode == RADIANS else math.radians(self.theta)

        cos_theta = math.cos(theta)
        sin_theta = math.sin(theta)

        return Cartesian(cos_theta * self.rho, self.y, sin_theta * self.rho, self.angle_mode)

    def to_cylindrical(self):
        return Cylindrical(self.theta, self.y, self.rho, self.angle_mode)
    
    def to_spherical(self):
        phi = math.atan2(self.y, self.rho)
        rho = math.sqrt(self.rho * self.rho + self.y * self.y)

        phi = phi if self.angle_mode == RADIANS else math.degrees(phi)

        return Spherical(self.theta, phi, rho, self.angle_mode)

    def __str__(self):
        return "Cylindrical(theta={0}, y={1}, rho={2}, angle_mode={3})".format(self.theta, self.y, self.rho, "RADIANS" if self.angle_mode == RADIANS else "DEGREES")

    def __repr__(self):
        return self.__str__()

class Spherical(object):
    """ Class for spherical coordinates. """
    def __init__(self, theta, phi, rho, angle_mode=DEGREES):
        self.theta = theta
        self.phi = phi
        self.rho = rho

        self.angle_mode = angle_mode

        super().__init__()

    def to_cartesian(self):
        theta = self.theta if self.angle_mode == RADIANS else math.radians(self.theta)
        phi = self.phi if self.angle_mode == RADIANS else math.radians(self.phi)

        cos_theta = math.cos(theta)
        sin_theta = math.sin(theta)

        cos_phi = math.cos(phi)
        sin_phi = math.sin(phi)

        x = cos_theta * cos_phi * self.rho
        y = sin_phi * self.rho
        z = sin_theta * cos_phi * self.rho

        return Cartesian(x, y, z, self.angle_mode)

    def to_cylindrical(self):
        phi = self.phi if self.angle_mode == RADIANS else math.radians(self.phi)

        sin_phi = math.sin(phi)

        y = sin_phi * self.rho
        rho = math.sqrt(self.rho * self.rho - y * y)

        return Cylindrical(self.theta, y, rho, self.angle_mode)
    
    def to_spherical(self):
        return Spherical(self.theta, self.phi, self.rho, self.angle_mode)

    def __str__(self):
        return "Spherical(theta={0}, phi={1}, rho={2}, angle_mode={3})".format(self.theta, self.phi, self.rho, "RADIANS" if self.angle_mode == RADIANS else "DEGREES")

    def __repr__(self):
        return self.__str__()
