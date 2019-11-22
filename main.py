#import codeAnalysis.block_to_code
import pygame
import pygame.locals as cst
import GUI.gui as gui
import GUI.models.Blocks
import GUI.models.Windows
import GUI.models.config
import codeAnalysis.block_to_code as btc
import codeProcessing as cp
import sys
import io

pygame.init()

pygame.display.set_caption('Game')
clock = pygame.time.Clock() #Pygame clock to limit framerate
run = True #Represent whether the programm is running or not
gui.draw_screen(True) #Draws the GUI for the first time, entirely

while run: #The loop that runs constantly
    redraw = False #If no block gets picked up there is no need to rebuild blocks
    for event in pygame.event.get():
        
        #Looking at all event that occured since last frame
        pos = pygame.mouse.get_pos()
        #Getting mouse cursor coordinates
        if event.type == cst.QUIT or event.type == cst.KEYDOWN and event.key == cst.K_ESCAPE:
            #Quit the game if ESC or the red cross is pressed
            run = False
        elif event.type == cst.MOUSEBUTTONDOWN:
            if event.button == 1: #If the left mouse button is clicked (Rising edge)
                gui.blocWriter.setActive(event) #Check whether the user clicked on the input box.
                if gui.scroll_win.get_hitbox().collidepoint(pos): #If the cursor is over the scroller
                    if gui.check_pick_up_in_scroller(gui.scroll_win,pos): 
                        code =cp.listBlock_to_code(gui.scroll_win.get_list())
                        #print(code)
                        old_stdout = sys.stdout # Memorize the default stdout stream
                        sys.stdout = buffer = io.StringIO()
                        try:
                            exec(code)
                            sys.stdout = old_stdout
                            whatWasPrinted = buffer.getvalue()
                            toPrint = whatWasPrinted.split('\n')
                            for i in toPrint:
                                if i:
                                    GUI.gui.global_printer.addLine(i,GUI.models.config.white)
                        except Exception as e: 
                            GUI.gui.global_printer.addLine(str(e),GUI.models.config.red)
                elif gui.drawer.get_hitbox().collidepoint(pos):
                    gui.check_pick_up_in_drawer(gui.drawer,pos)
                    redraw = True
            elif event.button == 4:
                gui.scroll_win.scroll(-20) #If mousewheel up, scroll the scroller
            elif event.button == 5:
                gui.scroll_win.scroll(20)  #If mousewheel is moved, scroll the scroller
        elif event.type == cst.MOUSEBUTTONUP:
            if event.button == 1 and gui.is_draging: #If the left mouse button is released (Falling edge)
                gui.check_drop_down_in_scroller(gui.scroll_win,pos) #Handles block being dropped 
        elif event.type == cst.KEYDOWN: #The user pressed a key
            newBlock = gui.blocWriter.write(event)
            if newBlock != None: #We have a new user input created bloc
                gui.blocks.append(newBlock) #Adds the input block to the list of blocks being dragged
                newBlock.clicked = True #Tags the block to notify it is being dragged
                gui.is_draging = True #Sets the dragging flag true
    gui.update_dragged_position() #Updating the position of dragged gui.blocks
    gui.draw_screen(redraw) #Draw the screen
    pygame.display.flip() #Refresh the display
    clock.tick(60) #Limit framerate to 60

pygame.quit()#Quit the program