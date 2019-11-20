# -------------------------------------------------------------
# GUI example for visual programming using drag and drop blocks
# Based on the Pygame library
# (C) 2019 Centralesupélec Coding weeks
# Released under MIT license
# Github : https://github.com/antoine-huguet/projectalgo
# -------------------------------------------------------------

import pygame
import pygame.locals as cst
from models.config import screen_height,screen_width,BG_generic_path
import models.Blocks
import models.Windows

#Create main window
win = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption('Game')

#Load backgrounds for the main window and scroller
bg = pygame.image.load(BG_generic_path).convert()
bg2 = pygame.image.load(BG_generic_path).convert()
bg = pygame.transform.scale(bg,(screen_width,screen_height))

#Create scroller and initialising it with a START block
scroll_win = models.Windows.Scroller((500,screen_height*2),0,200,bg2)
scroll_win.blocks.append([models.Blocks.START_Block(20,20)])

#Initialising a variable to track whether a block is being dragged or not
global is_draging 
is_draging = False

#Pygame clock to limit framerate
clock = pygame.time.Clock()

#Variable for exiting the program
run = True

#List of blocks in the main window
blocks = []

#Placing a test origin IF_block
origin = models.Blocks.IF_Block(100,100)
origin_else = models.Blocks.ELSE_Block(300,100)

blocks.append(origin)
blocks.append(origin_else)


def draw_screen():
    """
    Drawing all items in order (bg to fg)
    """
    win.blit(bg,(0,0))
    scroll_win.draw(win)
    for block in blocks:
        block.draw(win)

def add_tuple(a,b):
    """
    Quick functions for adding tuples
    """
    return(a[0]+b[0],a[1]+b[1])

def check_pick_up_in_scroller(scroller):
    """
    Check if a block is being picked up in the given scroller
    """
    for line in scroller.blocks:
        for block in line: #Looking at every blocks in the scroller
            if block.rect.collidepoint(scroller.global_coord_to_local(pos)) and block.is_movable:
                #If the mouse is over the block and the block is movable
                block.clicked = True #The block is now being clicked on
                global is_draging 
                is_draging = True # The mouse cursor is now draging a block 
                # Removing the block from the scroller and adding it to the main window
                scroller.remove(block) 
                blocks.append(block)

                #Updating the block coordinates to account for the changing frame of reference
                block.write_pos(add_tuple(scroller.local_coord_to_global(pos),(block.width//2,block.height//2)))

def check_pick_up_in_main():
    """
    Check if a block is being picked up in main
    """
    global is_draging
    global blocks
    for block in blocks: #Looking at all blocks in main
        if block.rect.collidepoint(pos): #If the mouse cursor is over it
            is_draging=True
            block.clicked = True
            #Now draging the block
            block.x,block.y = pos[0] - block.width//2, pos[1] - block.height//2
            #Snapping the middle of the block to the cursor
            break
            #Breaking to avoid picking up multiple blocks

def check_drop_down_in_scroller(scroller):
    """
    Check if a block is being dropped down in a scroller
    """
    global is_draging
    global blocks
    is_draging=False
    #Block is being dropped down
    for block in blocks:
        if block.clicked: 
            # Finding the clicked block
            block.clicked = False 
            target_not_found = True 
            # If no target snap point is found, the block is droppped
            for line in scroller.blocks:
                for snap in line: 
                    #Looking at all blocks in the scroller
                    if snap.rect.collidepoint(scroller.global_coord_to_local(pos)):
                        if isinstance(snap,models.Blocks.SNAP_Block):
                            # If the block is a snap point and the cursor is over it
                            scroller.replace(snap,block)
                        else:
                            scroller.insert(snap,block)
                        blocks.remove(block)
                        # Replacing the snap point with the block and removing the block from the main window
                        block.write_pos(add_tuple(scroller.global_coord_to_local(pos),(-block.width//2,-block.height//2)))
                        # Updating the block coordinates to account for the changing frame of reference
                        target_not_found = False
                        return
            if target_not_found:
                # If the block was dropped over no snap point
                blocks.remove(block)
                # The block is deleted

def update_dragged_position():
    """
    Update the position of dragged block to put it under the cursor
    """
    global blocks
    for block in blocks:
        if block.clicked:
            #For all clicked blocks
            pos = pygame.mouse.get_pos()
            block.x,block.y = pos[0] - block.width//2, pos[1] - block.height//2
            #The block coordinate are updated so that the middle of the block is under the cursor



while run:
    for event in pygame.event.get():
        #Looking at all event that occured since last frame
        pos = pygame.mouse.get_pos()
        #Getting mouse cursor coordinates
        if event.type == cst.QUIT or event.type == cst.KEYDOWN and event.key == cst.K_ESCAPE:
            run = False
            #Quit the game if ESC or the red cross is pressed
        elif event.type == cst.MOUSEBUTTONDOWN:
            if event.button == 1:
                #If the left mouse button is clicked (Rising edge)
                if scroll_win.get_hitbox().collidepoint(pos):
                    #If the cursor is over the scroller
                    check_pick_up_in_scroller(scroll_win)
                else:
                    check_pick_up_in_main()
            elif event.button == 4: scroll_win.scroll(-10) #If mousewheel up, scroll the scroller
            elif event.button == 5: scroll_win.scroll(10)
            #If mousewheel is moved, scroll the scroller
        elif event.type == cst.MOUSEBUTTONUP:
            if event.button == 1 and is_draging:
                # If the left mouse button is released (Falling edge)
                check_drop_down_in_scroller(scroll_win)

    update_dragged_position()
    #Updating the position of dragged blocks

    is_if = False
    is_else = False
    for i in blocks:
        if isinstance(i,models.Blocks.IF_Block):
            is_if = True
        if isinstance(i,models.Blocks.ELSE_Block): 
            is_else = True
    if not is_if:
        new = models.Blocks.IF_Block(100,100)
        blocks.append(new)
    if not is_else:
        new = models.Blocks.ELSE_Block(300,100)
        blocks.append(new)
    #Adding a new IF_Block if there are none in main, for test purposes

    draw_screen()
    #Draw the screen
    pygame.display.flip()
    #Refresh the display
    clock.tick(60)
    #Limit framerate to 60

pygame.quit()
#Quit the program