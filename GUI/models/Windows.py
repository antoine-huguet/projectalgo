import pygame
import models.config
import models.Blocks

class Scroller(pygame.surface.Surface):
    #A class that contains coding blocks and is able
    #to scroll up and down
    def __init__(self,size,x,y,bg):
        super().__init__((size[0],2000))
        self.blocks = [] # List of blocks
        # FORMAT :
        # List of all rows
        # Rows are lists of blocks
        # [ [First row First block, First row second block,..] , [Second row First block,..] ...]
        self.length = size[1]
        self.scroll_y = 0 # Storing the amount of y offset due tu scrolling
        self.x = x  # X position of the Scroller in main
        self.y = y # Y position offset
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
                    if not isinstance(j,models.Blocks.SNAP_Block):
                        line.append(j)
                line.append(models.Blocks.SNAP_Block(0,0))
                up.append(line)
                # Only save non snap blocks in the row and if necessary adds one at the end
            elif not isinstance(self.blocks[i][0],models.Blocks.SNAP_Block):
                up.append([self.blocks[i][0]])
            # If the block does not take side blocks, it is appened
        up.append([models.Blocks.SNAP_Block(0,0)])
        # Adds a snap point below the last block
        self.blocks = up

    def update_length(self):
        res = self.blocks[0][0].y+self.blocks[0][0].height+models.config.y_spacing
        for line in self.blocks:
            max_y_size = 0
            for block in line:
                if block.height > max_y_size:
                    max_y_size = block.height
            res+= max_y_size + models.config.y_spacing
        self.length = max(res,self.length)


    def draw(self,window):
        self.update_length()
        # Draws self to a given window
        self.blit(self.bg,(0,0))
        # Laying the background
        self.update_blocks_snappoints()
        # Updating snap points
        self.blocks[0][0].draw(self)
        # Drawing the START block
        cursorx,cursory = self.blocks[0][0].x, self.blocks[0][0].y+self.blocks[0][0].height+models.config.y_spacing
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
                cursorx+= block.width + models.config.x_spacing
                # Moving the cursor X-wise
                if block.height > max_y_size:
                    max_y_size = block.height
            cursorx = cursorx_ini
            # Resetting the X coordinate of the cursor
            cursory += max_y_size + models.config.y_spacing
            # Moving the cursor Y-wise
        window.blit(self,(self.x,self.y),area = pygame.rect.Rect((0,self.scroll_y),self.size))
        #Drawing self onto the given window
    
    def scroll(self,amount):
        # Changes the scrolling amount if in range of the maximum scrolling
        if 0<=self.scroll_y + amount < (self.length-self.size[1]):
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
            return (pos[0]-self.x,pos[1]-self.y+self.scroll_y)
        elif type(pos)==int and type(y)==int:
            return (pos-self.x,y-self.y+self.scroll_y)

    def local_coord_to_global(self,pos,y=None):
        # Translate local coordinates to global coordinates
        if type(pos)==tuple:
            return (pos[0]+self.x,pos[1]+self.y-self.scroll_y)
        elif type(pos)==int and type(y)==int:
            return (pos+self.x,y+self.y-self.scroll_y)

    def get_hitbox(self):
        # Returns a pygame.rect representing the hitbox of self
        return self.get_rect().move(self.x,self.y)

    def replace(self, target, item):
        # Replace a target by a given item in self.blocks
        for i in range(len(self.blocks)):
            for j in range(len(self.blocks[i])):
                if self.blocks[i][j]==target:
                    self.blocks[i][j] = item
    
    def insert(self, target, item):
        for i,line in enumerate(self.blocks):
            for j,block in enumerate(line):
                if block == target:
                    if j==0:
                        self.blocks.insert(i,[item])
                        return
                    else:
                        self.blocks[i].insert(j,item)
                        return

class Printer(pygame.surface.Surface):
    '''A surface used to display lines.'''
    def __init__(self,size,xPos,yPos):
        super().__init__(size)
        self.xPos = xPos
        self.yPos = yPos
        self.size = size #Set size - should not be moved
        self.textColor = (255,255,255) #White
        self.backgroundColor = (0,0,0) #Black
        self.fontSize = models.config.fontSize
        self.fontName = models.config.fontName
        # TODO : find a nicer font (to match the bloc)
        self.font = pygame.font.Font(self.fontName, self.fontSize) 
        self.text = [] #We use the list as a file, which is empty at first
        self.maxLine = 10 #We won't display more than maxLine lines at the same time
        self.xOffSet = 15 #Off set the text from the side of the window

    def draw(self,window):
        self.fill((0,0,0)) #Get a whole black background
        numberOfLines = len(self.text) # <=10
        yPos = self.xOffSet #So that the first line is at a corner
        for line in self.text:
            textDisp = self.font.render('> '+line,True,self.textColor)
            textRect = textDisp.get_rect().move(self.xOffSet,yPos) #Create and move rect to the position required
            self.blit(textDisp,textRect)
            yPos += self.fontSize + self.xOffSet #We move down to the next line
        window.blit(self,(self.xPos,self.yPos))

    def addLine(self,line):
        self.text.append(line)
        if len(self.text)>self.maxLine:
            self.text.pop(0)
        #We use text as a FIFO