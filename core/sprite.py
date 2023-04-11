import pygame as pg
from PIL import Image
import numpy

class Sprite:

    def __init__(self,path:str):
        self.raw_surface  = pg.image.load(path)
        self.raw_pil_image = Image.open(path)
        self.transformed_pil_image = self.raw_pil_image.copy()
        self.transformed_surface = self.raw_surface.copy()
        self.r0 = [list(i) for i in [(50, 0), (256, 0), (256, 256), (0, 256)]]
        self.r1 = [list(i) for i in [(0, 0), (256, 0), (256, 256), (0, 256)]]


    def get_diff( self ):
        a = self.raw_surface.get_size()
        b = self.transformed_surface.get_size()

        return [b[0]/a[0],b[1]/a[1]]


    def transform( self,new_w,new_h ):
        self.transformed_surface = pg.transform.scale(self.raw_surface,(new_w,new_h))

    def transform_by_height( self,new_h ):
        current_h = self.raw_surface.get_height()
        new_w = self.raw_surface.get_width() * (new_h / current_h)

        self.transformed_surface = pg.transform.scale(self.raw_surface,(new_w,new_h))

    def transform_by_rel( self,rel_x,rel_y ):
        new_w,new_h = self.raw_surface.get_size()
        new_w *= rel_x
        new_h *= rel_y

        self.transformed_surface = pg.transform.scale(self.raw_surface,(new_w,new_h))


    def find_coeffs(self, pa, pb ) :
        matrix = []
        for p1, p2 in zip(pa, pb) :
            matrix.append([p1[0], p1[1], 1, 0, 0, 0, -p2[0] * p1[0], -p2[0] * p1[1]])
            matrix.append([0, 0, 0, p1[0], p1[1], 1, -p2[1] * p1[0], -p2[1] * p1[1]])

        A = numpy.matrix(matrix, dtype=float)
        B = numpy.array(pb).reshape(8)

        res = numpy.dot(numpy.linalg.inv(A.T * A) * A.T, B)
        return numpy.array(res).reshape(8)

    def keep_inside(self) :
        min_x = 0
        min_y = 0
        for x, y in self.r0 :
            if x < min_x :
                min_x = x
            if y < min_y :
                min_y = y

        for v in self.r0 :
            if min_x < 0 :
                v[0] -= min_x
            if min_y < 0 :
                v[1] -= min_y


    def to_surface( self,image: Image ) :
        mode = image.mode
        size = image.size
        data = image.tobytes()

        py_image = pg.image.fromstring(data, size, mode)
        return py_image


    def update(self) :
        img = self.raw_pil_image
        width, height = img.size
        coeffs = self.find_coeffs(self.r0, self.r1)
        self.keep_inside()
        img = img.transform((int(width * 1.5), int(height * 1.5)), Image.PERSPECTIVE, coeffs,
            Image.NEAREST)
        self.transformed_surface = self.to_surface(img)