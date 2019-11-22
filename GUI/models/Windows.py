import pygame
import GUI.models.config
import GUI.models.Blocks

class Scroller(pygame.surface.Surface):
    #A class that contains coding blocks and is able
    #to scroll up and down
    def __init__(self,size,x,y,bg):
        super().__init__((size[0],2000))
        self.blocks = [] # List of blocks
        # FORMAT :
        # List of all rows
        # Rows are lists of blocks
        # [ [First row First block, First row second block,.] , [Second row First block,.] ..]
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
                    if not isinstance(j,GUI.models.Blocks.SNAP_BLOCK):
                        line.append(j)
                line.append(GUI.models.Blocks.SNAP_BLOCK(0,0))
                up.append(line)
                # Only save non snap blocks in the row and if necessary adds one at the end
            elif not isinstance(self.blocks[i][0],GUI.models.Blocks.SNAP_BLOCK):
                up.append([self.blocks[i][0]])
            # If the block does not take side blocks, it is appened
        up.append([GUI.models.Blocks.SNAP_BLOCK(0,0)])
        # Adds a snap point below the last block
        self.blocks = up

    def update_length(self):
        res = self.blocks[0][0].y+self.blocks[0][0].height+GUI.models.config.y_spacing
        for line in self.blocks:
            max_y_size = 0
            for block in line:
                if block.height > max_y_size:
                    max_y_size = block.height
            res+= max_y_size + GUI.models.config.y_spacing
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
        cursorx,cursory = self.blocks[0][0].x, self.blocks[0][0].y+self.blocks[0][0].height+GUI.models.config.y_spacing
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
                cursorx+= block.width + GUI.models.config.x_spacing
                # Moving the cursor X-wise
                if block.height > max_y_size:
                    max_y_size = block.height
            cursorx = cursorx_ini
            # Resetting the X coordinate of the cursor
            cursory += max_y_size + GUI.models.config.y_spacing
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

    def get_list(self):
        res = []
        for line in self.blocks:
            L = []
            for block in line:
                if not isinstance(block,GUI.models.Blocks.SNAP_BLOCK):
                    L.append(block)
            res.append(L)
        return res

class Printer(pygame.surface.Surface):
    '''A surface used to display lines.'''
    def __init__(self,size,xPos,yPos):
        super().__init__(size)
        self.xPos = xPos; self.yPos = yPos
        self.size = size #Set size - should not be moved not resized
        self.backgroundColor = (0,0,0) #Black
        #Set font - TODO : find a nicer font (to match the block)
        self.fontSize = GUI.models.config.fontSize
        self.fontName = GUI.models.config.fontPath
        self.font = pygame.font.Font(self.fontName, self.fontSize) 
        
        self.text = [] #FIFO to contains both the text and its color
        self.maxLine = 10 #We won't display more than maxLine lines at the same time
        self.xOffSet = 15 #Off set the text from the side of the window

    def draw(self,window):
        self.fill((0,0,0)) #Get a whole black background
        yPos = self.xOffSet #So that the first line is at a corner
        for entry in self.text:
            (line,color)=entry
            textDisp = self.font.render('> '+line,True,color)
            textRect = textDisp.get_rect().move(self.xOffSet,yPos) #Create and move rect to the position required
            self.blit(textDisp,textRect)
            yPos += self.fontSize + self.xOffSet #We move down to the next line
        window.blit(self,(self.xPos,self.yPos))

    def addLine(self,line,color):
        self.text.append((line,color))
        if len(self.text)>self.maxLine:
            self.text.pop(0)
        #We use text as a FIFO

class Block_drawer(Scroller):
    '''This class is a scrollable window that stores blocks.'''
    def __init__(self,size,x,y,bg,classes):
        super().__init__(size,x,y,bg)
        self.classes = classes
        self.blocks = []

    def rebuild_blocks(self):
        surplus = self.blocks[len(self.classes):]
        self.blocks = []
        for i in self.classes:
            self.blocks.append(i(0,0))
        self.blocks += surplus

    def draw(self,window):
        self.rebuild_blocks()
        self.blit(self.bg,(0,0))
        cursorx,cursory = 20,20
        cursorx_ini = 20
        block_cursor = 0
        max_y = 0
        l = len(self.blocks)
        while block_cursor<l:
            if cursorx + GUI.models.config.x_spacing_drawer + self.blocks[block_cursor].width < self.size[0]:
                self.blocks[block_cursor].x = cursorx
                self.blocks[block_cursor].y = cursory
                self.blocks[block_cursor].draw(self)
                if self.blocks[block_cursor].height > max_y:
                    max_y = self.blocks[block_cursor].height
                cursorx += GUI.models.config.x_spacing_drawer + self.blocks[block_cursor].width
                block_cursor+=1
            else:
                cursory += max_y + GUI.models.config.y_spacing_drawer
                cursorx = cursorx_ini
                max_y = 0
        window.blit(self,(self.x,self.y),area = pygame.rect.Rect((0,self.scroll_y),self.size))


class BlocWriter(pygame.surface.Surface):
    '''A surface used to create text line bloc.'''
    def __init__(self,size,xPos,yPos):
        super().__init__(size)
        self.xPos = xPos
        self.yPos = yPos
        self.size = size #Set size - should not be moved
        self.inputBoxSize = (10,10)
        self.textColor = (255,255,255) #White
        self.backgroundColor = (0,0,0) #Black
        self.inputBoxColor = (0,0,255) #Blue
        self.fontSize = GUI.models.config.fontSize
        self.fontName = GUI.models.config.fontPath
        self.rect = pygame.Rect(self.xPos,self.yPos,self.size[0],self.size[1])
        # TODO : find a nicer font (to match the bloc)
        self.font = pygame.font.Font(self.fontName, self.fontSize) 
        self.defaultText = 'Enter calculation' #The default message to invite the user to type
        self.text = self.defaultText
        self.active = False

    def write(self,event):
        '''Used to write to the box. Event is used to get key input.'''
        if self.active:
            if event.key == pygame.K_RETURN:
                # TODO : handle bloc creation
                # print("Create : {}".format(self.text))
                pos = pygame.mouse.get_pos()
                newBlock = GUI.models.Blocks.INPUT_BLOCK(pos[0],pos[1],self.text)
                self.text = self.defaultText
                return newBlock
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                self.text += event.unicode

    def setActive(self,event):
        '''Used to define whether or not the user is clicking on the window'''
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = True
                if self.text == self.defaultText:
                    self.text=''
            else:
                self.active = False

    def draw(self,window):
        '''Draw the surface'''
        self.fill((125,125,125)) #Get a whole grey background
        textDisp = self.font.render(self.text,True,self.textColor)
        textRect = textDisp.get_rect().move(0,0) #Create and move rect to the position required
        self.blit(textDisp,textRect)
        window.blit(self,(self.xPos,self.yPos))
