import pygame
from pygame.locals import *
from constantes import *
from classes import *

pygame.init()
win = pygame.display.set_mode((screen_width,screen_height))

scroll_win = pygame.surface.Surface((300,screen_height))

scroll_y = 0

i_a = scroll_win.get_rect()
x1 = i_a[0]
x2 = x1 + i_a[2]
a, b = (255, 0, 0), (60, 255, 120)
y1 = i_a[1]
y2 = y1 + i_a[3]
h = y2-y1
rate = (float((b[0]-a[0])/h),
         (float(b[1]-a[1])/h),
         (float(b[2]-a[2])/h)
         )
for line in range(y1,y2):
     color = (min(max(a[0]+(rate[0]*line),0),255),
              min(max(a[1]+(rate[1]*line),0),255),
              min(max(a[2]+(rate[2]*line),0),255)
              )
     pygame.draw.line(scroll_win, color, (x1, line),(x2, line))



bg = pygame.image.load(BG_generic_path).convert()
bg = pygame.transform.scale(bg,(screen_width,screen_height))

snap = Block(600,100,'if_snap',0)

win.blit(bg,(0,0))

clock = pygame.time.Clock()

pygame.display.flip()
run = True

blocks = pygame.sprite.Group()
origins = pygame.sprite.Group()
snappoints = pygame.sprite.Group()

origins.add(Block(100,100,'if',0))
snappoints.add(snap)


drag_offsetx = 0
drag_offsety = 0


while run:
    for event in pygame.event.get():
        print(event)
        print(len(blocks))
        if event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
            run = False
        elif event.type == MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            x,y = pos
            if event.button == 3:
                blocks.add(Block(x,y,'if',len(blocks)+1))
            elif event.button == 1:
                for block in reversed(blocks.sprites()):
                    if block.rect.collidepoint(pos):
                        drag_offsetx = block.rect.x - x
                        drag_offsety = block.rect.y - y
                        block.clicked = True
                        break
                for origin in origins:
                    if origin.rect.collidepoint(pos):
                        block = Block(x,y,'if',len(blocks)+1)
                        blocks.add(block)
                        drag_offsetx = origin.rect.x - x
                        drag_offsety = origin.rect.y - y
                        block.clicked = True
            elif event.button == 4: scroll_y = min(scroll_y + 15, 0)
            elif event.button == 5: scroll_y = max(scroll_y - 15, -300)
        elif event.type == MOUSEBUTTONUP:
            for block in blocks:
                block.clicked = False

    for block in blocks:
        if block.clicked:
            pos = pygame.mouse.get_pos()
            if snap.rect.collidepoint(pos):
                block.rect.x, block.rect.y = snap.rect.x, snap.rect.y
            else:
                block.rect.x, block.rect.y = pos[0] + drag_offsetx, pos[1] + drag_offsety

    
    win.blit(bg,(0,0))
    win.blit(scroll_win,(screen_width-300,scroll_y))
    snappoints.draw(win)
    origins.draw(win)
    blocks.draw(win)
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()