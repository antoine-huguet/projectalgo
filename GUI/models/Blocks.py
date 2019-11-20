import pygame
import models.config

class Block():
    def __init__(self,image,xpos,ypos):
        self.image = image # Visual appearance 
        self.clicked = False
        self.rect = self.image.get_rect()
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.y = ypos
        self.x = xpos
        # X and Y position of the block
        self.snappoints = []
        # List of all snappoints the block has
        self.is_movable = True
    
    def draw(self,window):
        # Draw self to a given window
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        window.blit(self.image,(self.x,self.y))

    def write_pos(self,pos):
        # Convinient method to write self.x and self.y
        self.x = pos[0]
        self.y = pos[1]

## --- All blocsk

#Start
class START_Block(Block):
    def __init__(self,xpos,ypos):
        super().__init__(pygame.transform.scale(pygame.image.load(models.config.START_path).convert_alpha(),(204,72)),xpos,ypos )
        self.is_movable = False
        self.snappoints = ['below']

#Snap
class SNAP_Block(Block):
    def __init__(self,xpos,ypos):
        super().__init__(pygame.transform.scale(pygame.image.load(models.config.SNAP_path).convert_alpha(),(72,72)),xpos,ypos)
        self.is_movable = False

#Controle
class IF_Block(Block):
    def __init__(self,xpos,ypos):
        super().__init__(pygame.transform.scale(pygame.image.load(models.config.IF_path).convert_alpha(),(100,72)),xpos,ypos)
        self.snappoints=['below','side']

class ELSE_Block(Block):
    def __init__(self,xpos,ypos):
        super().__init__(pygame.transform.scale(pygame.image.load(models.config.ELSE_path).convert_alpha(),(163,72)),xpos,ypos)
        self.snappoints=['below']

class END_BLOCK(Block):
    def __init__(self,xpos,ypos):
        super().__init__(pygame.transform.scale(pygame.image.load(models.config.END_path).convert_alpha(),(123,72)),xpos,ypos)
        self.snappoints=['below']

class WHILE_BLOCK(Block):
    def __init__(self,xpos,ypos):
        super().__init__(pygame.transform.scale(pygame.image.load(models.config.WHILE_path).convert_alpha(),(204,72)),xpos,ypos)
        self.snappoints=['below','side']

#Operators
class MINUS_BLOCK(Block):
    def __init__(self,xpos,ypos):
        super().__init__(pygame.transform.scale(pygame.image.load(models.config.MINUS_path).convert_alpha(),(40,72)),xpos,ypos)
        self.snappoints=['side']

class PLUS_BLOCK(Block):
    def __init__(self,xpos,ypos):
        super().__init__(pygame.transform.scale(pygame.image.load(models.config.PLUS_path).convert_alpha(),(40,72)),xpos,ypos)
        self.snappoints=['side']

class PL_BLOCK(Block):
    def __init__(self,xpos,ypos):
        super().__init__(pygame.transform.scale(pygame.image.load(models.config.PL_path).convert_alpha(),(40,72)),xpos,ypos)
        self.snappoints=['side']

class PR_BLOCK(Block):
    def __init__(self,xpos,ypos):
        super().__init__(pygame.transform.scale(pygame.image.load(models.config.PR_path).convert_alpha(),(40,72)),xpos,ypos)
        self.snappoints=['side']

class DIV_BLOCK(Block):
    def __init__(self,xpos,ypos):
        super().__init__(pygame.transform.scale(pygame.image.load(models.config.DIV_path).convert_alpha(),(40,72)),xpos,ypos)
        self.snappoints=['side']

class X_BLOCK(Block):
    def __init__(self,xpos,ypos):
        super().__init__(pygame.transform.scale(pygame.image.load(models.config.X_path).convert_alpha(),(40,72)),xpos,ypos)
        self.snappoints=['side']

class EQUAL_BLOCK(Block):
    def __init__(self,xpos,ypos):
        super().__init__(pygame.transform.scale(pygame.image.load(models.config.EQUAL_path).convert_alpha(),(40,72)),xpos,ypos)
        self.snappoints=['side']

#Variables
class A_BLOCK(Block):
    def __init__(self,xpos,ypos):
        super().__init__(pygame.transform.scale(pygame.image.load(models.config.A_path).convert_alpha(),(50,72)),xpos,ypos)
        self.snappoints=['side']

class B_BLOCK(Block):
    def __init__(self,xpos,ypos):
        super().__init__(pygame.transform.scale(pygame.image.load(models.config.B_path).convert_alpha(),(50,72)),xpos,ypos)
        self.snappoints=['side']

class C_BLOCK(Block):
    def __init__(self,xpos,ypos):
        super().__init__(pygame.transform.scale(pygame.image.load(models.config.C_path).convert_alpha(),(50,72)),xpos,ypos)
        self.snappoints=['side']

class D_BLOCK(Block):
    def __init__(self,xpos,ypos):
        super().__init__(pygame.transform.scale(pygame.image.load(models.config.D_path).convert_alpha(),(50,72)),xpos,ypos)
        self.snappoints=['side']

class E_BLOCK(Block):
    def __init__(self,xpos,ypos):
        super().__init__(pygame.transform.scale(pygame.image.load(models.config.E_path).convert_alpha(),(50,72)),xpos,ypos)
        self.snappoints=['side']

class F_BLOCK(Block):
    def __init__(self,xpos,ypos):
        super().__init__(pygame.transform.scale(pygame.image.load(models.config.F_path).convert_alpha(),(50,72)),xpos,ypos)
        self.snappoints=['side']

#Miscelianous
class AFFECTATION_BLOCK(Block):
    def __init__(self,xpos,ypos):
        super().__init__(pygame.transform.scale(pygame.image.load(models.config.AFFECTATION_path).convert_alpha(),(102,72)),xpos,ypos)
        self.snappoints=['side']

class PRINT_BLOCK(Block):
    def __init__(self,xpos,ypos):
        super().__init__(pygame.transform.scale(pygame.image.load(models.config.PRINT_path).convert_alpha(),(204,72)),xpos,ypos)
        self.snappoints=['side']

class INPUT_BLOCK(Block):
    '''Blocks that have been created from a user line input.'''
    def __init__(self,posX,posY,text):
        image = pygame.transform.scale(pygame.image.load(models.config.PRINT_path).convert_alpha(),(204,72)) #This doesn't matter as it is not used.
        super().__init__(image,posX,posY)
        self.text = text
        self.textColor = (255,255,255) #White
        self.backgroundColor = (59,103,142) #grey-blue
        self.fontSize = models.config.fontSize
        self.fontName = models.config.fontName
        self.font = pygame.font.Font(self.fontName, self.fontSize) 

    def __setSize__(self):
        self.height = 72 #Same as other blocks
        self.width = 15*len(self.text)

    def draw(self,window):
        # Overwrite the existing one
        textDisp = self.font.render(self.text,True,self.textColor,self.backgroundColor)
        textRect = textDisp.get_rect().move(self.x,self.y)
        window.blit(self.image,(self.x,self.y))