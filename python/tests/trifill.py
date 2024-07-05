import numpy as np

###

def tri_fill(a, b, c):
    a, b, c = sorted([a, b, c], key=lambda vert: vert[1])

    ca = [c[0] - a[0], c[1] - a[1]]
    ba = [b[0] - a[0], b[1] - a[1]]
    cb = [c[0] - b[0], c[1] - b[1]]

    edge1 = [a[0], float("inf") if ca[1] == 0 else ca[0] / ca[1]] # (vertex a, inverse slope a --> c)
    edge2 = [a[0], float("inf") if ba[1] == 0 else ba[0] / ba[1]] # (vertex a, inverse slope a --> b)
    edge3 = [b[0], float("inf") if cb[1] == 0 else cb[0] / cb[1]] # (vertex b, inverse slope b --> c)

    swap = b[0] < a[0] + ba[1] * edge1[1] # b.x < a.x + (c.x - a.x)(b.x - a.x)/(c.y - a.y)
    if swap: edge1, edge2 = edge2, edge1
    for y in range(int(a[1]), int(b[1])): # a.y --> b.y
        for x in range(int(edge1[0]), int(edge2[0])): # p1.x --> p2.x
            yield (x, y)

        edge1[0] += edge1[1]
        edge2[0] += edge2[1]

    if swap: edge1 = edge3
    else: edge2 = edge3
    for y in range(int(b[1]), int(c[1])): # b.y --> c.y
        for x in range(int(edge1[0]), int(edge2[0])): # p1.x --> p2.x
            yield (x, y)

        edge1[0] += edge1[1]
        edge2[0] += edge2[1]

###

def tri_fill_bary(a, b, c):
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

###

from PIL import Image, ImageDraw
import random

img = Image.new("RGB", (1920, 1080), color=(255, 255, 255))
draw = ImageDraw.Draw(img)

tex = Image.open("/home/pi/TextureLib/brick.jpg").convert("RGB")
tex_map = tex.load()

uv_a = np.array([0.00, 0.5])
uv_b = np.array([0.00, 0.0])
uv_c = np.array([0.33, 0.0])

dev = 200
hdev = dev / 2
for tri in range(0, 250):
    center = np.array([random.randint(0, img.size[0]), random.randint(0, img.size[1])], dtype="float64")

    a = center + np.array([random.randint(0, dev), random.randint(0, dev)], dtype="float64") - hdev
    b = center + np.array([random.randint(0, dev), random.randint(0, dev)], dtype="float64") - hdev
    c = center + np.array([random.randint(0, dev), random.randint(0, dev)], dtype="float64") - hdev

    try:
        for pos, bary in tri_fill_bary(a, b, c):
            if pos[0] > 0 and pos[0] < img.size[0] and pos[1] > 0 and pos[1] < img.size[1]:
                uv = uv_a * bary[0] + uv_b * bary[1] + uv_c * bary[2]
                tex_pos = (int(uv[0] * (tex.size[0] - 1)), int(uv[1] * (tex.size[1] - 1)))
                img.putpixel(pos, tex_map[tex_pos])#(int(bary[0] * 255), int(bary[1] * 255), int(bary[2] * 255)))

    except Exception as e:
        print("Oops!", e)
        continue

    draw.line([tuple(a), tuple(b)], fill="black", width=2)
    draw.line([tuple(b), tuple(c)], fill="black", width=2)
    draw.line([tuple(c), tuple(a)], fill="black", width=2)

    draw.ellipse([tuple(a - 5), tuple(a + 5)], outline="black", width=2, fill="red")
    draw.ellipse([tuple(b - 5), tuple(b + 5)], outline="black", width=2, fill="green")
    draw.ellipse([tuple(c - 5), tuple(c + 5)], outline="black", width=2, fill="blue")

    print(tri)

img.save("trifill.png")
