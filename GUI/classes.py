import pygame
import constantes as cst

class Scroller(pygame.surface.Surface):
    #A class that contains coding blocks and is able
    #to scroll up and down
    def __init__(self,size,x,yoffset,bg):
        super().__init__(size)
        self.blocks = [] # List of blocks
        # FORMAT :
        # List of all rows
        # Rows are lists of blocks
        # [ [First row First block, First row second block,..] , [Second row First block,..] ...]
        self.scroll_y = 0 # Storing the amount of y offset due tu scrolling
        self.x = x  # X position of the Scroller in main
        self.yoffset = yoffset # Y position offset
        self.size = size 
        self.bg = bg # Background image

    def update_blocks_snappoints(self):
        # Functions that makes sure Snap blocks are only there at the
        # end of a row or at the end of a column
        up = []
        for i in range(len(self.blocks)):
            if self.blocks[i]==[]:
                continue
            # Ignore potential empty lists
            if 'side' in self.blocks[i][0].snappoints:
                # If the first block takes other block on it's right
                line = []
                for j in self.blocks[i]:
                    if not isinstance(j,SNAP_Block):
                        line.append(j)
                line.append(SNAP_Block(0,0,0))
                up.append(line)
                # Only save non snap blocks in the row and if necessary adds one at the end
            elif not isinstance(self.blocks[i][0],SNAP_Block):
                up.append([self.blocks[i][0],SNAP_Block(0,0,0)])
            # If the block does not take side blocks, it is appened
        up.append([SNAP_Block(0,0,0)])
        # Adds a snap point below the last block
        self.blocks = up


    def draw(self,window):
        # Draws self to a given window
        self.blit(self.bg,(0,0))
        # Laying the background
        self.update_blocks_snappoints()
        # Updating snap points
        self.blocks[0][0].draw(self)
        # Drawing the START block
        cursorx,cursory = self.blocks[0][0].x, self.blocks[0][0].y+self.blocks[0][0].height+cst.y_spacing
        # Set the drawing cursor to the initial position (below start block)
        cursorx_ini = cursorx
        # Saves the X coordinate of the start of rows
        for line in self.blocks[1:]:
            max_y_size = 0
            # Variable to set the Y jump between rows
            for block in line:
                block.x = cursorx
                block.y = cursory
                block.draw(self)
                # Placing block at the cursor
                cursorx+= block.width + cst.x_spacing
                # Moving the cursor X-wise
                if block.height > max_y_size:
                    max_y_size = block.height
            cursorx = cursorx_ini
            # Resetting the X coordinate of the cursor
            cursory += max_y_size + cst.y_spacing
            # Moving the cursor Y-wise
        window.blit(self,(self.x,self.yoffset-self.scroll_y))
        #Drawing self onto the given window
    
    def scroll(self,amount):
        # Changes the scrolling amount if in range of the maximum scrolling
        if 0<=self.scroll_y + amount < (self.size[1]-cst.screen_height):
            self.scroll_y += amount
    
    def remove(self,element):
        # Removes a specific element from self.blocks
        # If there are other blocs on the row, they are removed
        for i in range(len(self.blocks)):
            if self.blocks[i][0]==element:
                # If the target is the first of a row, it is removed entirely
                self.blocks.pop(i)
                break
            elif element in self.blocks[i]:
                # If the target is inside a row, removes only the target
                self.blocks[i].remove(element)
                break

    def global_coord_to_local(self,pos,y=None):
        # Translate global coordinates to local coordinates
        if type(pos)==tuple:
            return (pos[0]-self.x,pos[1]-self.yoffset+self.scroll_y)
        elif type(pos)==int and type(y)==int:
            return (pos-self.x,y-self.yoffset+self.scroll_y)

    def local_coord_to_global(self,pos,y=None):
        # Translate local coordinates to global coordinates
        if type(pos)==tuple:
            return (pos[0]+self.x,pos[1]+self.yoffset-self.scroll_y)
        elif type(pos)==int and type(y)==int:
            return (pos+self.x,y+self.yoffset-self.scroll_y)

    def get_hitbox(self):
        # Returns a pygame.rect representing the hitbox of self
        return self.get_rect().move(self.x,self.yoffset-self.scroll_y)

    def replace(self,target, item):
        # Replace a target by a given item in self.blocks
        for i in range(len(self.blocks)):
            for j in range(len(self.blocks[i])):
                if self.blocks[i][j]==target:
                    self.blocks[i][j] = item

class Block():
    def __init__(self,image,xpos,ypos,id):
        self.image = image # Visual appearance 
        self.clicked = False
        self.rect = self.image.get_rect()
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.y = ypos
        self.x = xpos
        # X and Y position of the block
        self.id = id
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
        self.x=pos[0]
        self.y = pos[1]


class IF_Block(Block):
    def __init__(self,xpos,ypos,id):
        super().__init__(pygame.transform.scale(pygame.image.load(cst.IF_path).convert_alpha(),(100,50)),xpos,ypos,id)
        self.snappoints=['below','side']

class SNAP_Block(Block):
    def __init__(self,xpos,ypos,id):
        super().__init__(pygame.transform.scale(pygame.image.load(cst.IF_SNAP_path).convert_alpha(),(100,50)),xpos,ypos,id)
        self.is_movable = False
    
class START_Block(Block):
    def __init__(self,xpos,ypos,id):
        super().__init__(pygame.transform.scale(pygame.image.load(cst.START_path).convert_alpha(),(100,50)),xpos,ypos,id)
        self.is_movable = False
        self.snappoints = ['below']