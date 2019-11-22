import pygame
import pygame.locals as cst
import GUI.models.Blocks
import GUI.models.Windows
import GUI.models.config
pygame.init()

#Create main window
win = pygame.display.set_mode((GUI.models.config.screen_width,GUI.models.config.screen_height))

#Load backgrounds for the main window and scroller
bg = pygame.transform.scale(pygame.image.load(GUI.models.config.BG_generic_path).convert(),(GUI.models.config.screen_width,GUI.models.config.screen_height))
bg2 = pygame.image.load(GUI.models.config.BG_generic_path).convert()

#Create scroller and initialising it with a START block
scroll_win = GUI.models.Windows.Scroller((700,GUI.models.config.screen_height),0,0,bg2)
scroll_win.blocks.append([GUI.models.Blocks.START_BLOCK(20,20)])
drawer = GUI.models.Windows.Block_drawer((300,GUI.models.config.screen_height),700,0,bg2,[GUI.models.Blocks.IF_BLOCK,GUI.models.Blocks.WHILE_BLOCK,GUI.models.Blocks.ELSE_BLOCK,GUI.models.Blocks.END_BLOCK,
GUI.models.Blocks.PLUS_BLOCK,GUI.models.Blocks.MINUS_BLOCK,GUI.models.Blocks.DIV_BLOCK,GUI.models.Blocks.X_BLOCK,GUI.models.Blocks.PL_BLOCK,GUI.models.Blocks.PR_BLOCK,
GUI.models.Blocks.EQUAL_BLOCK,GUI.models.Blocks.DIF_BLOCK,GUI.models.Blocks.SUPL_BLOCK,GUI.models.Blocks.SUP_BLOCK,GUI.models.Blocks.INFL_BLOCK,GUI.models.Blocks.INF_BLOCK,
GUI.models.Blocks.AFFECTATION_BLOCK,GUI.models.Blocks.PRINT_BLOCK,GUI.models.Blocks.A_BLOCK,GUI.models.Blocks.B_BLOCK,GUI.models.Blocks.C_BLOCK,
GUI.models.Blocks.D_BLOCK,GUI.models.Blocks.E_BLOCK,GUI.models.Blocks.F_BLOCK])

#Create global printer
global_printer = GUI.models.Windows.Printer((GUI.models.config.screen_width-GUI.models.config.startPrinter,GUI.models.config.screen_height-GUI.models.config.heightBlocWriter),GUI.models.config.startPrinter,0)
global_printer.addLine("Welcome !",GUI.models.config.white)

#Input zone for text
blocWriter = GUI.models.Windows.BlocWriter((GUI.models.config.screen_width-GUI.models.config.startPrinter,GUI.models.config.heightBlocWriter),GUI.models.config.startPrinter,GUI.models.config.screen_height-GUI.models.config.heightBlocWriter)

is_draging = False #Initialising a variable to track whether a block is being dragged or not
blocks = [] #List of blocks in the main window


def writeAffection(line):
    global_printer.addLine(line,GUI.models.config.white)

def writePrint(line):
    global_printer.addLine(line,GUI.models.config.red)

def draw_screen(update):
    """Drawing all items in order (bg to fg)."""
    win.blit(bg,(0,0))
    scroll_win.draw(win)
    drawer.draw(win,update)
    global_printer.draw(win)
    blocWriter.draw(win)
    for block in blocks:
        block.draw(win)

def add_tuple(a,b):
    """Quick functions for adding tuples."""
    return(a[0]+b[0],a[1]+b[1])

def check_pick_up_in_scroller(scroller,pos):
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
            elif block.rect.collidepoint(scroller.global_coord_to_local(pos)) and isinstance(block,GUI.models.Blocks.START_BLOCK):
                return True

def check_pick_up_in_drawer(scroller,pos):
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
            return True
        
    return False
def check_drop_down_in_scroller(scroller,pos):
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
                        if isinstance(snap,GUI.models.Blocks.SNAP_BLOCK): #If the block is a snap point and the cursor is over it
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