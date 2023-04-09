import numpy
import random
import sys
from PIL import Image

def find_coeffs(pa, pb):
    matrix = []
    for p1, p2 in zip(pa, pb):
        matrix.append([p1[0], p1[1], 1, 0, 0, 0, -p2[0]*p1[0], -p2[0]*p1[1]])
        matrix.append([0, 0, 0, p1[0], p1[1], 1, -p2[1]*p1[0], -p2[1]*p1[1]])

    A = numpy.matrix(matrix, dtype=float)
    B = numpy.array(pb).reshape(8)

    res = numpy.dot(numpy.linalg.inv(A.T * A) * A.T, B)
    return numpy.array(res).reshape(8)

pic = "./pic.png"
res = "./pic_res.png"

import sys
from PIL import Image

img = Image.open(pic)
width, height = img.size
m = -0.5
xshift = abs(m) * width
new_width = width + int(round(xshift))

coeffs = find_coeffs(
        [(0, 0), (256, 0), (256, 256), (0, 256)],
        [(0, 0), (256, 0), (new_width, height), (xshift, height)])

img.transform((width, height), Image.PERSPECTIVE, coeffs,
        Image.BICUBIC).save(res)



exit()