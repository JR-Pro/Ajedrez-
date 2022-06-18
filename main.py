import colorsys
from email.mime import image
from shutil import move
from sqlite3 import SQLITE_SELECT, Row
from turtle import Screen, color, width
import pygame as p 
from pygame import MOUSEBUTTONDOWN, draw
import game, intArt , time, movimiento 
whidth=height=512
dimension= 8 # esta es la dimension del tablero 
sq_Size=51 // dimension # estos son las dimensiones de las casillas 
max_Fps=15 # esto servira para las animaciones 
images = {}

#para inicializar las imagenes de las piezas 
def loadimage():
    pieces= ["bP","bR","bN","bB","bQ","bK","wP","wR","wN","wB","wQ","wK"]
    for pices in pieces:
        print("")
       
def main():
    p.init()
    Screen=p.display.set_mode((whidth,height))
    Clock=p.time.Clock()
    White = (255, 255, 255)
    black = (0,0,0)
    Screen.fill(White)
    gs = game.gamestate
    ValidMoves = gs.getvalidMoves
    Movemade = False # esta funcion servira para cuando un movimiento sea echo
    
    run=True 
    sqselect=()
    playerClick=[] # servira para el conteo de las parejas
    GameOver=False
    playerOne=False # si el jugador juega blancas, sera true , si no no
    playerTwo=True # igual que con jugador 1 pero orientando a las negras 
    while run:
        humanTurn = (gs.makeMOve and playerOne) or (not gs.makeMOve and playerTwo)
        for e in p.event.get():
            if e.type==p.QUIT:
                run=False
            elif e.type==MOUSEBUTTONDOWN: # esta funcion para hacer clik y que las piezas del Ajedrez de muevan 
                if not GameOver and humanTurn:
                    location=p.mouse.get_pos #esta es la posision del mouse en el eje x e Y
                    col = location[0] // sq_Size
                    Row = location[1] // sq_Size
                if sqselect == (Row,col): # el usuario hace clik doble veces y se borra o se limpia 
                        sqselect()
                        playerClick = []
                else:
                    sqselect = (Row,col)
                    playerClick.append(sqselect)
                if len(playerClick) == 2: # despues de dos cliks
                    move = movimiento.Move(playerClick[0],playerClick[1], gs.board)
                    print(move.getChessNotation())
                    for i in range(len(ValidMoves)):
                        if move == ValidMoves[i]: # para verificar la validez de un movimiento
                            gs.makeMOve(ValidMoves[i])
                            Movemade = True
                            sqselect = ()
                            playerClick= []
                    if not MovimientoEcho:
                        playerClick = [sqselect]
            elif e.type == p.KEYDOWN: #se desace el movimiento echo al pulsar z
                if e.key == p.K_z:
                    gs.undoMove() 
                    Movemade = True 
                    GameOver = False
                if e.key == p.K_r: # esto sirve para reiniciar el tablero
                    gs = game.gamestate()
                    ValidMoves= gs.validarMovimientos()
                    sqselect = ()
                    playerClick = []
                    MovimientoEcho= True
                    GameOver = False
                    #movimiento de la i.a 
                if not GameOver and not humanTurn:
                    time.sleep(2) 
                    AIMove=intArt.findeBestMove(gs.validMoves)
                    if AIMove is None:
                        AIMove = intArt.findrandomMove(ValidMoves)
                        gs.makeMOve(AIMove)
                        Movemade= True
                    if Movemade:
                        ValidMoves=gs.getValidMoves()
                        Movemade= False
                    drawGameStage = (Screen,gs,ValidMoves,sqselect)
                     #cuando termina la partida en un empate de un jaque mate 
                    if gs.checkMate:
                         GameOver = True
                         if gs.whiteToMove:
                            drawText(Screen,"victoria de las negras por jaque mate")
                         else:
                             drawText(Screen, " victorias de las blancas por el jaque mate ")
                    elif gs.staleMate:
                        GameOver =True
                        drawText(Screen,"empate por rey ahogado")
                       
                    Clock.tick(max_Fps)
                    p.display.flip()
#Esto es el resalte de las casillas disponibles conforme al movimiento de las piezas
    def highlightSquares(Screen,gs,ValidMoves,sqSelectd):
     if sqSelectd !=():
        r,c = sqSelectd
        if gs.board[r][c][0]==("w" if  gs.whiteToMove else "b"): #pieza seleccionada
            #resalte de las casillas elegidas 
            s = p.Surface((sq_Size , sq_Size))
            s.seth_alpha(100)
            s.fill(p.color("orange"))
            Screen.blit(s,(c * sq_Size, r * sq_Size))
           
            #resalte de los movimientos en aquellas casillas
            s.fill(p.color("blue ")) 
            for move in ValidMoves:
                if move.starRow == r and move.startCol == c:
                    Screen.blit(s, (sq_Size * move.endcol, sq_Size * move.endRow))
# esto dibuja todos los elementos del juego , el tablero entero con piezas 
#el tablero y las piezas el ultimo ejecuta el programa 
    def drawGamestage(screen,gs,validMoves,sqselectd):
     drawBoard(screen)
    highlightSquares(Screen,gs,ValidMoves,sqselect)
    drawpiezas(Screen, gs.board)
   
   
    def drawBoard(Screen):
        global color
        color=[p.color(White), p.color(black)]
        for r in range (dimension): # para las filas 
            for c in range(dimension): #para las columnas 
                
                # esto es para pintar las casillas 
                color=color[((r+c) % 2)]
                p.draw.rect(Screen,color,p.Rect(c * sq_Size, r * sq_Size, sq_Size,sq_Size))
    def  drawpiezas(Screen,Board):
       for r in range(dimension):#para las filas 
        for c in range (dimension):#para las columnas 
            piezas= Board[r][c]
            if piezas !="--": #para las casillas que no estan vacias 
                Screen.blit(images[piezas], p.rect(c * sq_Size, r * sq_Size,sq_Size,sq_Size))
    def drawText(Screen,text):
        font = p.font.SysFont("times new roman",28,True,False)  
        textObj = font.render(text,0,p.color("black")) 
        textlocation=p.rect(0,0,width,height).move(width/2 - textObj.get_width()/2,height/2 - textObj.get_height()/2)
        Screen.blit(textObj,textlocation)
        textObj= font.render(text,0, p.Color("gray"))
        Screen.blit(textObj,textlocation.move(2,2))
if  __name__== "__main__":
    print("si tienes dudas mra dentro de los archivos")
    print("numbasan")
    main()