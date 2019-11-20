import pygame
import pygame.locals as cst
from models.config import screen_height,screen_width,BG_generic_path
import models.Blocks
import models.Windows

pygame.init() 

#Create main window
win = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption('Game')

#Load backgrounds for the main window and scroller
bg2 = pygame.image.load(BG_generic_path).convert()
bg = pygame.transform.scale(pygame.image.load(BG_generic_path).convert(),(screen_width,screen_height))

#Pygame clock to limit framerate
clock = pygame.time.Clock()

#Variable for exiting the program
run = True

window = models.Windows.Printer((500,500))
window.addLine("Hello world !")
window.addLine(",djaoidja")
window.addLine("45646546")
window.addLine("Hello world !")
window.addLine(",djaoidja")
window.addLine("45646546")
window.addLine("Hello world !")
window.addLine(",djaoidja")
window.addLine("45646546")
window.addLine("10")
window.addLine("11")

def draw_screen():
    win.blit(bg,(0,0))
    window.draw(win)


while run:
    for event in pygame.event.get():
        #Looking at all event that occured since last frame
        pos = pygame.mouse.get_pos()
        if event.type == cst.QUIT or event.type == cst.KEYDOWN and event.key == cst.K_ESCAPE:
            run = False
            #Quit the game if ESC or the red cross is pressed
    draw_screen()
    #Draw the screen
    pygame.display.flip()
    #Refresh the display
    clock.tick(60)
    #Limit framerate to 60

pygame.quit()
#Quit the program