import cg3D

renderer = cg3D.Renderer()
camera = cg3D.Camera()#cg3D.Camera(cg3D.ORTHOGRAPHIC, fov=10)
scene = cg3D.Scene()

camera.transform(cg3D.Translate(0, 0, 5))

light = cg3D.DirectionalLight(color=(255, 255, 255))
scene.add_light("keylight", light)

#############################################################################################################
import math

def f(x, y, z):
    return x * x + y * y + z * z - 0.1 * (math.sin(6 * x) + math.cos(6 * y) + math.sin(6 * z)) - 1
    #return x * x + y * y + z * z - 1

def df(x, y, z):
    return [2 * x - 0.6 * math.cos(6 * x), 2 * y + 0.6 * math.sin(6 * y), 2 * z - 0.6 * math.cos(6 * z)]
    #return [2 * x, 2 * y, 2 * z]

mesh = cg3D.Implicit(f, df)
#mesh = cg3D.Cone(sides=100)
mesh.material = cg3D.Material(ambient=(10, 10, 10), diffuse=(255, 100, 0), specular=(255, 255, 255), gloss=20)
mesh.transform(cg3D.RotateAboutAxis(1, -1, 1, -30))

scene.add_mesh("mesh1", mesh)
#############################################################################################################

renderer.render(scene, camera)
renderer.save("test.png")
