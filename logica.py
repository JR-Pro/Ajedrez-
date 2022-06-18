import colorsys
from email.mime import image, images
from shutil import move
from sqlite3 import SQLITE_SELECT, Row
from turtle import Screen, color, width
import pygame as p 
from pygame import MOUSEBUTTONDOWN, draw
from pyparsing import col
import engine, IntArt , time 
ancho=altura=512
dimension= 8 # esta es la dimension del tablero 
tamaño_cuadrado=51 // dimension # estos son las dimensiones de las casillas 
max_Fps=15 # esto servira para las animaciones 
images = {}

#para inicializar las imagenes de las piezas 
def cargando_image():
    piezas= ["bP","bR","bN","bB","bQ","bK","wP","wR","wN","wB","wQ","wK"]
    for piezas in piezas:
        images[piezas]= p.transform.scale(p.image.cargando("images/" + piezas +".png" )(tamaño_cuadrado,tamaño_cuadrado))
def main():
    p.init()
    pantalla=p.display.set_mode((ancho,altura))
    reloj=p.time.Clock()
    pantalla.fill(p.colr("white"))
    gs = engine.gamestate()
    ValidarMovimientos = gs.getvalidarMOvimientos()
    MovimientoEcho = False # esta funcion servira para cuando un movimiento sea echo
    cargando_image()
    run=True 
    sqselect=()
    playerClick=[] # servira para el conteo de las parejas
    GameOver=False
    jugador1=False # si el jugador juega blancas, sera true , si no no
    jugador2=True # igual que con jugador 1 pero orientando a las negras 
    while run:
        GiroHumano =(gs.whiteToMode and jugador1) or (not gs.whiteToMove and jugador2)
        for e in p.event.get():
            if e.type==p.QUIT:
                run=False
            elif e.type==MOUSEBUTTONDOWN: # esta funcion para hacer clik y que las piezas del Ajedrez de muevan 
                if not GameOver and GiroHumano:
                    ubicacion=p.mouse.get_pos #esta es la posision del mouse en el eje x e Y
                    col = ubicacion[0]//tamaño_cuadrado
                    Row = ubicacion[1]//tamaño_cuadrado
                    if sqselect == (col,Row): # el usuario hace clik doble veces y se borra o se limpia 
                        sqselect()
                        playerClick = []
                else:
                    sqselect =(col,Row)
                    playerClick.append(sqselect)
                if len(playerClick)==2: # despues de dos cliks
                    move = engine.Move(playerClick[0],playerClick[1], gs.board)
                    print(move.getChessNotation())
                    for i in range(len(ValidarMovimientos)):
                        if move == ValidarMovimientos[i]: # para verificar la validez de un movimiento
                            gs.makeMOve(ValidarMovimientos[i])
                            MovimientoEcho=True
                            sqselect= ()
                            playerClick= []
                    if not MovimientoEcho:
                        playerClick = [sqselect]
            elif e.type == p.KEYDOWN: #se desace el movimiento echo al pulsar z
                if e.key == p.K_z:
                    gs.desacerMovimiento() 
                    MovimientoEcho = True 
                    GameOver = False
                if e.key == p.K_r: # esto sirve para reiniciar el tablero
                    gs = engine.gamestate()
                    ValidarMovimientos= gs.validarMovimientos()
                    sqselect = ()
                    playerClick = []
                    MovimientoEcho= True
                    GameOver = False
                    #movimiento de la i.a 
                if not GameOver and not GiroHumano:
                    time.sleep(2) 
                    apuntar=IntArt.encontrarMejorMovimiento(gs.validarMovimiento)
                    if apuntar is None:
                        apuntar = IntArt.buscarMovimiento(ValidarMovimientos)
                        gs.hacerMOvimiento(apuntar)
                        MovimientoEcho = True
                    if MovimientoEcho:
                        ValidarMovimientos=gs.obtenerMovimientosValidos()
                        MovimientoEcho= False
                        dibujarJuego = (Screen,gs,MovimientoEcho,sqselect)
                     #cuando termina la partida en un empate de un jaque mate 
                    if gs.checkMate:
                        GameOver = True
                        if gs.whiteToMove:
                            dibujarTexto = (Screen,"victoria de las negras por jaque mate")
                        else:
                            dibujarTexto(Screen, " victorias de las blancas por el jaque mate ")
                    elif gs.estancamiento:
                        GameOver =True
                        dibujarTexto(Screen,"empate por rey ahogado")
                        reloj.tick(max_Fps)
                        p.display.flip()
#Esto es el resalte de las casillas disponibles conforme al movimiento de las piezas
    def resaltarCuadros(Screen,gs,ValidarMovimientos,sqselect):
     if sqselect !=():
        r,c = sqselect
        if gs.board[r][c][0]==("w" gs.whiteToMove else "B"): #pieza seleccionada
            #resalte de las casillas elegidas 
            s = p.superficie((tamaño_cuadrado,tamaño_cuadrado))
            s.seth_alpha(100)
            s.llenar(p.color("orange"))
            Screen.blit(s(c * tamaño_cuadrado, r * tamaño_cuadrado))
           
            #resalte de los movimientos en aquellas casillas
            s.susperficie(p.color("blue ")) 
            for move in ValidarMovimientos:
                if move.comienzo == r and move.comienzoCol == c:
                    Screen.blit(s, (tamaño_cuadrado * move.finalCol,tamaño_cuadrado * move.finalRow))
# esto dibuja todos los elementos del juego , el tablero entero con piezas 
#el tablero y las piezas el ultimo ejecuta el programa 
    def dibujarJuego(screen,gs,validarMovimientos,sqselect):
        drawBoard(screen)
        resaltarCuadros(screen,gs,validarMovimientos,sqselect)
        drawpiezas(screen,gs.Board)
   
   
    def drawBoard(Screen):
        global color
        color=[p.color("white"), p.color("dark green")]
        for r in range (dimension): # para las filas 
            for c in range(dimension): #para las columnas 
                
                # esto es para pintar las casillas 
                color=color[((r+c) % 2)]
                p.draw.rect(Screen,color,p.Rect(c * tamaño_cuadrado, r * tamaño_cuadrado, tamaño_cuadrado,tamaño_cuadrado))
    def  drawpiezas(Screen,Board):
        for r in range(dimension):#para las filas 
            for c in range (dimension):#para las columnas 
                piezas= drawBoard[r][c]
                if piezas !="--": #para las casillas que no estan vacias 
                    Screen.blit(images[piezas], p.rect(c * tamaño_cuadrado, r * tamaño_cuadrado,tamaño_cuadrado,tamaño_cuadrado))
    def drawText(Screen,text):
        font = p.font.SysFont("times new roman",28,True,False)  
        textObj = font.render(text,0,p.color("black")) 
        textUbicacion=p.rect(0,0,width,altura).move(width/2 - textObj.get_width()/2,altura/2 - textObj.get_height()/2)
        Screen.blit(textObj,textUbicacion)
        textObj= font.render(text,0, p.Color("gray"))
        Screen.blit(textObj,textUbicacion.move(2,2))

    if  __name__ == "__main__":
        print("si tienes dudas mra dentro de los archivos")
        print("numbasan")
        main()
             
