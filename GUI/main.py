import pygame
from pygame.locals import *
from constantes import *
from classes import *

win = pygame.display.set_mode((screen_width,screen_height))

scroll_win = Scroller((300,screen_height))



bg = pygame.image.load(BG_generic_path).convert()
bg = pygame.transform.scale(bg,(screen_width,screen_height))

clock = pygame.time.Clock()

run = True

blocks = []

origin = IF_Block(100,100,0)

blocks.append(origin)

def draw_screen():
    win.blit(bg,(0,0))
    scroll_win.draw(win,screen_width-300,0)
    for block in blocks:
        block.draw(win)



while run:
    for event in pygame.event.get():
        #print(event)
        if event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
            run = False
        elif event.type == MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if event.button == 1:
                for block in blocks:
                    print(block.rect.collidepoint(pos))
                    if block.rect.collidepoint(pos):
                        print("block clicked")
                        block.clicked = True
                        block.x,block.y = pos[0] - block.width//2, pos[1] - block.height//2
                        break
        elif event.type == MOUSEBUTTONUP:
            for block in blocks:
                block.clicked = False
    for block in blocks:
        if block.clicked:
            pos = pygame.mouse.get_pos()
            block.x,block.y = pos[0] - block.width//2, pos[1] - block.height//2



    draw_screen()
    pygame.display.flip()
    clock.tick(60)

pygame.quit()