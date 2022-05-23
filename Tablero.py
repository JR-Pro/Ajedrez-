import pygame
negro = (0,0,0)
blanco = (255,255,255)
pygame.init()

dimen = [600,600]
screen = pygame.display.set_mode(dimen)
pygame.display.set_caption("Ajedrez")

running = True
ancho = int(dimen[0] / 8)
alto = int(dimen[1] / 8)
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill(blanco)
    color = 0
    for i in range(0, dimen[0],ancho):
         for j in range(0, dimen[1],alto):
             if color % 2 == 0:
                pygame.draw.rect(screen, negro, [i, j, ancho, alto], 0)
             else:
                pygame.draw.rect(screen, blanco, [i, j, ancho, alto], 0)
             color += 1
         color += 1

    pygame.display.flip()

pygame.quit()

