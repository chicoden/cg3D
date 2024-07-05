#"""
from cg3D.mesh import *
from pygame.locals import *
from OpenGL.GLU import *
from OpenGL.GL import *
import pygame
import random

mesh = Cuboid()#Extrude(path=[(0, 0.666), (-0.5, -0.333), (0.5, -0.333)], depth=0.25)
colors = [(random.randint(0, 255) / 255, random.randint(0, 255) / 255, random.randint(0, 255) / 255) for face in mesh.faces]

def drawMesh():
    global mesh

    glColor3fv((0, 1, 0))
    glBegin(GL_TRIANGLES)
    color_index = 0
    for face in mesh.faces:
        glColor3fv(colors[color_index])
        for indices in face:
            vert_index = indices[0]
            glVertex3fv(mesh.get_vertex(vert_index)[0:3])

        color_index += 1
    glEnd()

    glBegin(GL_LINES)
    glColor3fv((0, 0, 1))
    for face in mesh.faces:
        center = [0, 0, 0]
        for vertex in face:
            center[0] += mesh.get_vertex(vertex[0])[0]
            center[1] += mesh.get_vertex(vertex[0])[1]
            center[2] += mesh.get_vertex(vertex[0])[2]

        center[0] /= 3
        center[1] /= 3
        center[2] /= 3

        glVertex3fv(center)
        glVertex3fv([center[0] + 0.25 * mesh.get_normal(face[0][2])[0],
                     center[1] + 0.25 * mesh.get_normal(face[0][2])[1],
                     center[2] + 0.25 * mesh.get_normal(face[0][2])[2]])

    glEnd()

pygame.init()
display = (800, 600)
pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
pygame.display.set_caption('Mesh Test')

gluPerspective(45, display[0] / display[1], 0.1, 50)
glTranslatef(0, 0, -5)

glEnable(GL_DEPTH_TEST)
glEnable(GL_CULL_FACE)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    glRotatef(3, 1, 1, 1)
    drawMesh()
    pygame.display.flip()
    pygame.time.wait(10)
#"""

"""
from cg3D.mesh import *

mesh = Cone()#Cylinder(height=1, radius=0.5, sides=36)
file = open('/home/pi/model.obj', 'w')
data = ''

for v in mesh.vertices:
    data += 'v {} {} {}\n'.format(*v[:-1:])

for vt in mesh.uvs:
    data += 'vt {} {}\n'.format(*vt)

for vn in mesh.normals:
    data += 'vn {} {} {}\n'.format(*vn[:-1:])

for f in mesh.faces:
    f = [[index + 1 if index is not None else '' for index in vertex] for vertex in f]
    data += 'f {} {} {}\n'.format('{}/{}/{}'.format(*f[0]), '{}/{}/{}'.format(*f[1]), '{}/{}/{}'.format(*f[2]))

print(data[0:-1])
file.write(data[0:-1])
file.close()
"""
