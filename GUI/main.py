# -------------------------------------------------------------
# GUI example for visual programming using drag and drop blocks
# Based on the Pygame library
# (C) 2019 Centralesupélec Coding weeks
# Released under MIT license
# Github : https://github.com/antoine-huguet/projectalgo
# -------------------------------------------------------------

import pygame
import pygame.locals as cst
import models.Blocks
import models.Windows
import models.config
import random
pygame.init()

#Create main window
win = pygame.display.set_mode((models.config.screen_width,models.config.screen_height))
pygame.display.set_caption('Game')

#Load backgrounds for the main window and scroller
bg = pygame.transform.scale(pygame.image.load(models.config.BG_generic_path).convert(),(models.config.screen_width,models.config.screen_height))
bg2 = pygame.image.load(models.config.BG_generic_path).convert()

#Create scroller and initialising it with a START block
scroll_win = models.Windows.Scroller((700,models.config.screen_height),0,0,bg2)
scroll_win.blocks.append([models.Blocks.START_Block(20,20)])
drawer = models.Windows.Block_drawer((300,models.config.screen_height),700,0,bg2,[models.Blocks.IF_Block,models.Blocks.WHILE_BLOCK,models.Blocks.ELSE_Block,models.Blocks.END_BLOCK,
models.Blocks.PLUS_BLOCK,models.Blocks.MINUS_BLOCK,models.Blocks.DIV_BLOCK,models.Blocks.X_BLOCK,models.Blocks.PL_BLOCK,models.Blocks.PR_BLOCK,
models.Blocks.EQUAL_BLOCK,models.Blocks.DIF_BLOCK,models.Blocks.SUPL_BLOCK,models.Blocks.SUP_BLOCK,models.Blocks.INFL_BLOCK,models.Blocks.INF_BLOCK,
models.Blocks.AFFECTATION_BLOCK,models.Blocks.PRINT_BLOCK,models.Blocks.A_BLOCK,models.Blocks.B_BLOCK,models.Blocks.C_BLOCK,
models.Blocks.D_BLOCK,models.Blocks.E_BLOCK,models.Blocks.F_BLOCK])

#Create global printer
global_printer = models.Windows.Printer((models.config.screen_width-models.config.startPrinter,models.config.screen_height-models.config.heightBlocWriter),models.config.startPrinter,0)
global_printer.addLine("Welcome !",models.config.white)

#Input zone for text
blocWriter = models.Windows.BlocWriter((models.config.screen_width-models.config.startPrinter,models.config.heightBlocWriter),models.config.startPrinter,models.config.screen_height-models.config.heightBlocWriter)

run = True #Variable for exiting the program
is_draging = False #Initialising a variable to track whether a block is being dragged or not
blocks = [] #List of blocks in the main window

clock = pygame.time.Clock() #Pygame clock to limit framerate

def writeAffection(line):
    global_printer.addLine(line,models.config.white)

def writePrint(line):
    global_printer.addLine(line,models.config.red)

def draw_screen():
    """Drawing all items in order (bg to fg)."""
    win.blit(bg,(0,0))
    scroll_win.draw(win)
    drawer.draw(win)
    global_printer.draw(win)
    blocWriter.draw(win)
    for block in blocks:
        block.draw(win)

def add_tuple(a,b):
    """Quick functions for adding tuples."""
    return(a[0]+b[0],a[1]+b[1])

def check_pick_up_in_scroller(scroller):
    """Check if a block is being picked up in the given scroller."""
    for line in scroller.blocks:
        for block in line: #Looking at every blocks in the scroller
            print(type(block))
            if block.rect.collidepoint(scroller.global_coord_to_local(pos)) and block.is_movable:
                #If the mouse is over the block and the block is movable
                block.clicked = True #The block is now being clicked on
                global is_draging 
                is_draging = True # The mouse cursor is now draging a block 
                scroller.remove(block)
                blocks.append(block)
                # Removing the block from the scroller and adding it to the main window
                block.write_pos(add_tuple(scroller.local_coord_to_global(pos),(block.width//2,block.height//2)))
                #Updating the block coordinates to account for the changing frame of reference
                return False
            elif block.rect.collidepoint(scroller.global_coord_to_local(pos)) and isinstance(block,models.Blocks.START_Block):
                return True

def check_pick_up_in_drawer(scroller):
    """Check if a block is being picked up in the given scroller."""
    for block in scroller.blocks: #Looking at every blocks in the scroller
        if block.rect.collidepoint(scroller.global_coord_to_local(pos)) and block.is_movable:
            #If the mouse is over the block and the block is movable
            block.clicked = True #The block is now being clicked on
            global is_draging 
            is_draging = True # The mouse cursor is now draging a block 
            blocks.append(block)
            # Removing the block from the scroller and adding it to the main window
            block.write_pos(add_tuple(scroller.local_coord_to_global(pos),(block.width//2,block.height//2)))
            #Updating the block coordinates to account for the changing frame of reference

def check_pick_up_in_main():
    """Check if a block is being picked up in main."""
    global is_draging
    global blocks
    for block in blocks: #Looking at all blocks in main
        if block.rect.collidepoint(pos): #If the mouse cursor is over it
            is_draging=True #Now draging the block
            block.clicked = True
            block.x,block.y = pos[0] - block.width//2, pos[1] - block.height//2 #Snapping the middle of the block to the cursor
            break #Breaking to avoid picking up multiple blocks

def check_drop_down_in_scroller(scroller):
    """Check if a block is being dropped down in a scroller."""
    global is_draging
    global blocks
    is_draging=False #Block is being dropped down
    for block in blocks:
        if block.clicked: #Searching the clicker blocs
            block.clicked = False 
            target_not_found = True # If no target snap point is found, the block is droppped
            for line in scroller.blocks:
                for snap in line: 
                    #Looking at all blocks in the scroller
                    if snap.rect.collidepoint(scroller.global_coord_to_local(pos)):
                        if isinstance(snap,models.Blocks.SNAP_Block): #If the block is a snap point and the cursor is over it
                            scroller.replace(snap,block)
                        elif snap.is_movable:
                            scroller.insert(snap,block)
                        blocks.remove(block) # Replacing the snap point with the block and removing the block from the main window
                        block.write_pos(add_tuple(scroller.global_coord_to_local(pos),(-block.width//2,-block.height//2)))
                        #Updating the block coordinates to account for the changing frame of reference
                        target_not_found = False
                        return
            if target_not_found: #If the block was not dropped over a snap point
                blocks.remove(block) # The block is deleted

def update_dragged_position():
    """Update the position of dragged block to put it under the cursor."""
    global blocks
    for block in blocks:
        if block.clicked: #Only for clicked blocks
            pos = pygame.mouse.get_pos()
            block.x,block.y = pos[0] - block.width//2, pos[1] - block.height//2
            #The block coordinate are updated so that the middle of the block is under the cursor


while run: #The loop that runs constantly
    for event in pygame.event.get():
        #Looking at all event that occured since last frame
        pos = pygame.mouse.get_pos()
        #Getting mouse cursor coordinates
        if event.type == cst.QUIT or event.type == cst.KEYDOWN and event.key == cst.K_ESCAPE:
            #Quit the game if ESC or the red cross is pressed
            run = False
        elif event.type == cst.MOUSEBUTTONDOWN:
            if event.button == 1: #If the left mouse button is clicked (Rising edge)
                blocWriter.setActive(event) #Check whether the user clicked on the input box.
                if scroll_win.get_hitbox().collidepoint(pos): #If the cursor is over the scroller
                    if check_pick_up_in_scroller(scroll_win):
                        #TODO : code_utilisateur(scroller.blocks)
                        pass
                elif drawer.get_hitbox().collidepoint(pos):
                    check_pick_up_in_drawer(drawer)
            elif event.button == 4:
                scroll_win.scroll(-20) #If mousewheel up, scroll the scroller
            elif event.button == 5:
                scroll_win.scroll(20)  #If mousewheel is moved, scroll the scroller
        elif event.type == cst.MOUSEBUTTONUP:
            if event.button == 1 and is_draging: #If the left mouse button is released (Falling edge)
                check_drop_down_in_scroller(scroll_win)
        elif event.type == cst.KEYDOWN: #The user pressed a key
            newBlock = blocWriter.write(event)
            if newBlock != None: #We have a new user input created bloc
                blocks.append(newBlock)
                newBlock.clicked = True
                is_draging = True


    update_dragged_position() #Updating the position of dragged blocks
    draw_screen() #Draw the screen
    pygame.display.flip() #Refresh the display
    clock.tick(60) #Limit framerate to 60

pygame.quit()#Quit the program