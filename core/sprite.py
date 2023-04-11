import pygame as pg

class Sprite:

    def __init__(self,path:str):
        self.raw_surface  = pg.image.load(path)
        self.transformed_surface = self.raw_surface.copy()

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

    def transform_by_width( self,new_w ):
        current_w = self.raw_surface.get_width()
        new_h = self.raw_surface.get_height() * (new_w / current_w)

        self.transformed_surface = pg.transform.scale(self.raw_surface,(new_w,new_h))

    def transform_by_rel( self,rel_x,rel_y ):
        new_w,new_h = self.raw_surface.get_size()
        new_w *= rel_x
        new_h *= rel_y

        self.transformed_surface = pg.transform.scale(self.raw_surface,(new_w,new_h))

    def flip( self,flip_x=False,flip_y=False ):
        self.transformed_surface = pg.transform.flip(self.transformed_surface,flip_x, flip_y)