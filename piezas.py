import pygame
import Tablero
tab = Tablero.ajadrez()
class piezas():
    def torre(self):
        torre_blanco1 = pygame.image.load("torre-blanca.png")
        posx = 200
        posy = 100
        running = True
        vel = 8
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            tab.screen.blit(torre_blanco1,(posx,posy))
            posx,posy = pygame.mouse.get_pos()
            posx = posx-100
            posy = posy-50

piezas.torre()
