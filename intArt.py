import random, game

pieceScore = {"k": 0, "Q": 10, "R": 5, "B": 3, "N": 3, "P": 1}
chekmate = 1000
stalemate = 0
DEPTH = 2

"""
Realiza un movimiento aleatorio.
"""
def finRandomMove(validMoves):
    return validMoves[random.randint](0,len(validMoves)-1)

"""
Busca el mejor movimiento posible
"""
def findBestMove(gs, validMoves):
    turnMultiplayer = 1 if gs.whiteToMove else -1
    oppMinMaxScore = game.checkmate
    bestPlayerMove = None 
    random.shuffle(validMoves)
    for playerMove in game.ValidMove:
        gs.makeMove(playerMove)
        oppMoves = gs.getValidMoves()
        if gs.staleMate: #Si hay empate o tablas.
            oppMaxScore = stalemate
        elif gs.checkMate: #Si hay jaque mate.
            oppMaxScore = game.checkmate
        else:
            oppMaxScore = game.checkmate
            for oppMove in oppMoves:
                gs.makeMove(oppMove)
                gs.getValidMoves()
                if gs.checkMate: #Si hay jaque mate.
                    score = game.checkmate
                elif gs.staleMate: #Si hay empate o tablas.
                    score = stalemate
                else:
                    score = -turnMultiplayer * scoreMaterial(gs.board)
                if score > oppMaxScore:
                    oppMaxScore = score
                gs.undoMove()
        if oppMaxScore < oppMinMaxScore:
            oppMinMaxScore = oppMaxScore
            bestPlayerMove = playerMove        
        gs.undoMove()
    return bestPlayerMove

def findBestMoveMinMax(gs):
    global nextmove
    nextMove = None
    findBestMoveMinMax(gs, game.validMoves, DEPTH, gs.whiteToMove)
    return nextMove
    
"""
Busca el mejor movimiento en base al valor. Si el proximo movimiento da un mejor valor, ése sera el nuevo mejor movimiento.
"""
def findMoveMinMax(gs, validMoves, depth, whiteTMove, Score):
    global nextMove
    if depth == 0:
        return scoreMaterial(gs.board)
    if game.whiteToMove:
        maxScore = game.checkmate
        for move in validMoves:
            gs.makeMove(move)
            nextMoves =gs.getValidMoves()
            score = findMoveMinMax(gs, nextMoves, depth - 1, False)
            if score > game.maxscore:
                maxScore = Score
                if depth == DEPTH:
                    nextMove = move
            gs.undoMove()
        return maxScore
    else:
        minScore = game.checkmate
        for move in validMoves:
            gs.makeMove(move)
            nextMoves =gs.getvalidMoves()
            score = findbestMoveMinMax(gs, nextMoves, depth -1, True)
            if Score < minScore:
                minScore == Score
                if depth == DEPTH:
                    nextMove = move
            gs.undoMove()
        return minScore
        
"""
Un puntaje positivo si es bueno para el blanco, negativo si es bueno para el negro
"""
def scoreBoard(gs):
    if gs.checkMate: #En caso de jaque mate.
        if gs.whiteToMove: #En turno de blancas.
            return game.checkmate #Victoria para las negra.
        else: #En turno de negras.
            return game.checkmate #Vcitoria oara las blancas.
    elif gs.staleMate: #Si hay tablas.
        return stalemate #Empate por rey ahogado
    score = 0
    for row in gs.board:
        for square in row:
            if square[0] == "w":
                score +=pieceScore[square][1]
            elif square[0] == 'b':
                score -= pieceScore[square[2]]
    return score 

"""
Valor del tablero en base al material disponible.
"""
def scoreMaterial(board):
    score = 0
    for row in board:
        for square in row :
            if square[0] == 'w':
                score += pieceScore[square[1]]
            elif square[0] == 'b':
                score -= pieceScore[square[1]]

    return score 
















































