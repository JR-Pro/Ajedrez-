import pygame
import Tablero
class piezas(Tablero):
    def torre():
        torre_blanco1 = pygame.image.load("Ajedrez/Ajedrez/torre-blanca.png")
        posx = 200
        posy = 100
        running = True
        vel = 8
        while running:
            Tablero.blit(torre_blanco1,(posx,posy))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            posx,posy = pygame.mouse.get_pos()
            posx = posx-100
            posy = posy-50

piezas.torre()
