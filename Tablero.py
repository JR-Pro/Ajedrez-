import pygame
from pygame.locals import *

class ajadrez():
    
    def herramientas(self):
        self.negro = (0,0,0)
        self.blanco =  (255,255,255)
        self.azul = (50,50,200)
        self.fondo = (24,25,30)
        self.dimen = (400,600)
        self.letras = ["A","B","C","D","F","G","H"]
        self.selec = (50,200,50)
        
    def dibujarTablero(self,screen, dimension, p_inicio, tamanio_fuente, fuente, seleccion):
        color = 0
        for i in range(8):
            for j in range(8):
                x = i * dimension + p_inicio[0]
                y = j * dimension + p_inicio[1]
                if color % 2 == 0:
                    pygame.draw.rect(screen,self.negro, [x, y, dimension, dimension], 0)
                else:
                    pygame.draw.rect(screen,self.blanco, [x, y, dimension, dimension], 0)
                if seleccion[0] == self.letras[i] and j == seleccion[1] - 1:
                    pygame.draw.rect(screen, self.selec , [x, y, dimension, dimension], 0)
                color += 1
            color += 1
            dibujarTexto(screen, self.letras[i], [x, p_inicio[1] - tamanio_fuente], fuente)
            dibujarTexto(screen,str(i + 1), [p_inicio[0] - tamanio_fuente, x], fuente)
            
       
    def dibujarTexto(self,screen, texto, posicion, fuente):
        self.Texto = fuente.render(texto, 1, self.azul)
        screen.blit(self.Texto, posicion)        
        
    def ajustarMedidas(self,tamanio_fuente):
        if self.dimen[1] < self.dimen[0]:
            ancho = int((self.dimen[1] - (tamanio_fuente * 2)) / 8)
            inicio = ((self.dimen[0] - self.dimen[1]) / 2) + tamanio_fuente, tamanio_fuente
        else:
            ancho = int((self.dimen[0] - (tamanio_fuente * 2)) / 8)
            inicio = tamanio_fuente, ((self.dimen[1] - self.dimen[0]) / 2) + tamanio_fuente
        return [inicio, ancho]    
        
    def obtenerPosicion(self,mouse, dimension, p_inicio, actual):
        xr, yr = mouse[0], mouse[1]
        for i in range(8):
            for j in range(8):
                x = i * dimension + p_inicio[0]
                y = j * dimension + p_inicio[1]
                if (xr >= x) and (xr <= x + dimension) and (yr >= y) and (yr <= y + dimension):
                    actual = [self.letras[i], j + 1]
        return actual
    
    def main(self):
        pygame.init()
        screen = pygame.display.set_mode(self.dimen)
        pygame.display.set_caption("__Tablero__")
        game_over = False
        clock = pygame.time.Clock()
        tamanio_fuente = 30
        seleccion = ['Z', -1]
        fuente = pygame.font.Font("fuentes/AliceandtheWickedMonster.ttf", tamanio_fuente)
        puntoInicio, dimension = ajustarMedidas(tamanio_fuente)
        while game_over is False:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    game_over = True
            botones = pygame.mouse.get_pressed()
            if botones[0]:
                pos = pygame.mouse.get_pos()
                seleccion = obtenerPosicion(pos, dimension, puntoInicio, seleccion)
            screen.fill(self.fondo)
            dibujarTablero(screen, dimension, puntoInicio, tamanio_fuente, fuente, seleccion)
            pygame.display.flip()
            clock.tick(60)
        pygame.quit()


if __name__ == "__main__":
    ajadrez.main()



