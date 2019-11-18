import pygame
from pygame.locals import *
from constantes import *
from classes import *

win = pygame.display.set_mode((screen_width,screen_height))
bg = pygame.image.load(BG_generic_path).convert()
bg2 = pygame.image.load(BG_generic_path).convert()
bg = pygame.transform.scale(bg,(screen_width,screen_height))

scroll_win = Scroller((300,screen_height*2),screen_width-300,0,bg2)

#scroll_win.blocks.append(IF_Block(100,100,0))



clock = pygame.time.Clock()

run = True

blocks = []

origin = IF_Block(100,100,0)

blocks.append(origin)

def draw_screen():
    win.blit(bg,(0,0))
    scroll_win.draw(win)
    for block in blocks:
        block.draw(win)

def add_tuple(a,b):
    return(a[0]+b[0],a[1]+b[1])

while run:
    for event in pygame.event.get():
        pos = pygame.mouse.get_pos()
        if event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
            run = False
        elif event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                for block in blocks:
                    print(block.rect.collidepoint(pos))
                    if block.rect.collidepoint(pos):
                        print("block clicked")
                        block.clicked = True
                        block.x,block.y = pos[0] - block.width//2, pos[1] - block.height//2
                        break
            elif event.button == 4: scroll_win.scroll(10)
            elif event.button == 5: scroll_win.scroll(-10)
        elif event.type == MOUSEBUTTONUP:
            if event.button == 1:
                for block in blocks:
                    block.clicked = False
                    if block.snapped:
                        blocks.remove(block)
                        scroll_win.blocks.append(block)
                        scroll_win.blocks[-1].write_pos(add_tuple(scroll_win.global_coord_to_local(pos),(-block.width//2,-block.height//2)))
                    else:
                        blocks.remove(block)
    for block in blocks:
        if block.clicked:
            if scroll_win.get_hitbox().collidepoint(pos):
                block.snapped = True
                print("snapped")
            else:
                block.snapped = False
                print("not snapped")
            pos = pygame.mouse.get_pos()
            block.x,block.y = pos[0] - block.width//2, pos[1] - block.height//2
    
    if len(blocks)==0:
        new = IF_Block(100,100,0)
        blocks.append(new)


    draw_screen()
    pygame.display.flip()
    clock.tick(60)

pygame.quit()