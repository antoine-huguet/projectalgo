import pygame
from pygame.locals import * 
from constantes import *


class Scroller(pygame.surface.Surface):
    def __init__(self,size,x,yoffset,bg):
        super().__init__(size)
        self.blocks = []
        self.scroll_y = 0
        self.x = x
        self.yoffset = yoffset
        self.size = size
        self.bg = bg

    def draw(self,window):
        self.blit(self.bg,(0,0))
        for block in self.blocks:
            block.draw(self)
        window.blit(self,(self.x,self.yoffset-self.scroll_y))
    
    def scroll(self,amount):
        if 0<=self.scroll_y + amount < (self.size[1]-screen_height):
            self.scroll_y += amount
    

    def global_coord_to_local(self,pos,y=None):
        if type(pos)==tuple:
            return (pos[0]-self.x,pos[1]-self.yoffset+self.scroll_y)
        elif type(pos)==int and type(y)==int:
            return (pos-self.x,y-self.yoffset+self.scroll_y)

    def local_coord_to_global(self,pos,y=None):
        if type(pos)==tuple:
            return (pos[0]+self.x,pos[1]+self.yoffset-self.scroll_y)
        elif type(pos)==int and type(y)==int:
            return (pos+self.x,y+self.yoffset-self.scroll_y)

    def get_hitbox(self):
        return self.get_rect().move(self.x,self.yoffset-self.scroll_y)

class Block():
    def __init__(self,image,xpos,ypos,id):
        self.image = image
        self.clicked = False
        self.snapped = True
        self.rect = self.image.get_rect()
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.y = ypos
        self.x = xpos
        self.id = id
        self.snappoints = []
        self.is_movable = True
    
    def draw(self,window):
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        window.blit(self.image,(self.x,self.y))
        #drawing hitbox for debbuging purposes
        #pygame.draw.rect(window,(255,0,0),self.rect,2)

    def write_pos(self,pos):
        self.x=pos[0]
        self.y = pos[1]


class IF_Block(Block):
    def __init__(self,xpos,ypos,id):
        super().__init__(pygame.transform.scale(pygame.image.load(IF_path).convert_alpha(),(100,50)),xpos,ypos,id)
        self.snappoints=['below','side']

class IF_SNAP_Block(Block):
    def __init__(self,xpos,ypos,id):
        super().__init__(pygame.transform.scale(pygame.image.load(IF_SNAP_path).convert_alpha(),(100,50)),xpos,ypos,id)
    
class START_Block(Block):
    def __init__(self,xpos,ypos,id):
        super().__init__(pygame.transform.scale(pygame.image.load(START_path).convert_alpha(),(100,50)),xpos,ypos,id)
        self.is_movable = False
        self.snappoints = ['below']