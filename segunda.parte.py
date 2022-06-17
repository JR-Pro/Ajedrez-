class gamestate():
    def __init__(self):
        self.board = [
            ["bR","bN","bB","bQ","bK","bB","bN","bR"]
            ["bP","bP","bP","bP","bP","bP","bP","bP"]
            ["--","--","--","--","--","--","--","--"]
            ["--","--","--","--","--","--","--","--"]
            ["--","--","--","--","--","--","--","--"]
            ["--","--","--","--","--","--","--","--"]
            ["wP","wP","wP","wP","wP","wP","wP","wP"]
            ["wR","wN","wB","wQ","wK","wB","wN","wR"]
        ]
        self.moveFunctions = {"P": self.getPawnMoves, "R": self.getRookMoves, "N": self.getKinightMoves, "B": self.getBishopMoves, "Q": self.getQueenMoves, "K": self.getkingMoves}
        self.whiteToMove = True
        self.moveLog = []
        self.whiteKingLocation = (7,4)
        self.blackKingLocation = (0,4)
        self.inCheck = False
        self.pins = []
        self.checks = []
        self.checkMate = False
        self.staleMate = False
        self.enPassantPossible = ()

        self.wCastleKingside = True
        self.wCastleQueenside = True
        self.bCastleKingside = True
        self.bCastleQueenside = True
        selfl.castleRightslog = [CastleRights(self.wCastleKingside, self.bCastleKingside, self.wCastleQueenside, self.bCastleQueenside)]

    def makeMOve(self,move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move)
        self.whiteToMove = not self.whiteToMove

        if move.pieceMoved == "wK":
            self.whiteKingLocation = (move.endRow, move.endCol)
        elif move.pieceMoved == "bK":
            self.blackKingLocation = (move.endRow, move.endCol)

        if move.pieceMoved[1] == "P" and abs(move.startRow, move.startCol) == 2:
            self.enPassantPossible = ((move.endRow + move.startRow) // 2, move.endCol)
        else:
            self.enPassantPossible = ()

        if move.enPassant:
            self.board[move.startRow][move.endCol] = "--"

        if move.pawnPromotion == True:
            promotedPiece = input("\nPromosion del peon a:\nReina (Q), Alfil (B), Caballo (N) o Torre (R). \ingresa la letra que esta en parentesis pero en minuscula \nElijo: ")
            if  promotedPiece == "q" or promotedPiece == "b" or promotedPiece == "n" or promotedPiece == "r":
                self.board[move.endRow][move.endCol] = move.pieceMoved[0] + promotedPiece.upper()
            else:
                error = True
                while (error == True):
                    print("\nCodigo erroneo")
                    promotedPiece = input("\nPromosion del peon a:\nReina (Q), Alfil (B), Caballo (N) o Torre (R). \ingresa la letra que esta en parentesis pero en minuscula \nElijo: ")
                    if  promotedPiece == "q" or promotedPiece == "b" or promotedPiece == "n" or promotedPiece == "r":
                        self.board[move.endRow][move.endCol] = move.pieceMoved[0] + promotedPiece.upper()
                        error = False

        self.updateCastleRight(move)
        self.castleRightslog.append(CastleRights(self.wCastleKingside, self.wCastleQueenside, self.bCastleKingside, self.bCastleQueenside))

        if move.castle:
            if move.endCol - move.startCol == 2:
                self.board[move.endRow][move.endCol - 1] = self.board[move.endRow][move.endCol + 1]   
                self.board[move.endRow][move.endCol + 1] = "--"
            else:
                self.board[move.endRow][move.endCol + 1] = self.board[move.endRow][move.endCol - 2]   
                self.board[move.endRow][move.endCol - 2] = "--"

    def undoMove(self):
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCapture
            self.whiteToMove = not self.whiteToMove
            if move.pieceMoved == "wK":
                self.whiteKingLocation = (move.endRow, move.endCol)
            elif move.pieceMoved == "bK":
                self.blackKingLocation = (move.endRow, move.endCol)
            if move.enPassant:
                self.board[move.endRow][move.endCol] = "--"
                self.board[move.startRow][move.startCol] = move.pieceCapture
                self.enPassantPossible = (move.endRow, move.endCol)

            if move.pieceMoved[1] == "P" and abs(move.startRow - move.endRow) == 2:
                self.enPassantPossible = ()

            self.castleRightslog.pop()
            CastleRights = self.castleRightslog[-1]
            self.wCastleKingside = CastleRights.wks
            self.wCastleQueenside = CastleRights.wqs 
            self.bCastleKingside = CastleRights.bks 
            self.bCastleQueenside = CastleRights.bqs 

            if move.castle:
                if move.endCol - move.startCol == 2:
                    self.board[move.endRow][move.endCol + 1] = self.board[move.endRow][move.endCol + 1]   
                    self.board[move.endRow][move.endCol - 1] = "--"
                else:
                    self.board[move.endRow][move.endCol - 2] = self.board[move.endRow][move.endCol - 2]   
                    self.board[move.endRow][move.endCol + 1] = "--"
                 
            self.checkMate = False 
            self.staleMate = False 

    def getvalidMoves(self):
        moves = []
        self.inCheck, self.pins, self.checks = self.checkForPinAndChecks()
        if self.whiteToMove:
            KingRow = self.whiteKingLocation[0]
            KingCol = self.whiteKingLocation[1]
        else:
            KingRow = self.blackKingLocation[0]
            KingCol = self.blackKingLocation[1]
            
        if self.inCheck:
            if len(self.check) == 1:
                moves = self.getAllPosiblesMoves()

                check = self.checks[0]
                checkRow = check[0]
                checkCol = check[1]
                piecechecking = self.board[checkRow][checkCol]
                validSquares = []

                if piecechecking[1] == "N":
                    validSquares = [(checkRow, checkCol)]
                else:
                    for i in range(1,8)
                        validSquare = (KingRow + check[2] * i, KingCol + check[3] * i)
                        validSquares.append(validSquare)
                        if validSquare[0] == checkRow and validSquare[1] == checkCol:
                            break
                for i in range(len(moves)-1, -1, -1):
                    if moves[i].pieceMoved[1] != "K":
                        if not (moves[i].endRow, moves[i].endCol) in validSquares:
                            moves.remove(moves[i])
            else:
                self.getkingMoves(KingRow, KingCol, moves)
        else:
            moves = self.getAllPosiblesMoves()
        if len(moves) == 0:
            if self.inCheck:
                self.checkMate = True
            else:
                self.staleMate = True
        else:
            self.checkMate = False 
            self.staleMate = False 
        return moves
    
    def checkForPinsAndChecks(self):
        pins = []
        checks = []
        inCheck = False 
        if self.whiteToMove:
            enemycolor = "b"
            allycolor = "w"
            startRow = self.whiteKingLocation[0]
            startCol = self.whiteKingLocation[1]
        else:
            enemycolor = "b"
            allycolor = "w"
            startRow = self.blackKingLocation[0]
            startCol = self.blackKingLocation[1]

        directions = ((-1, 0), (0, -1), (1,0), (0,1), (-1, -1), (-1, 1), (1, -1), (1, 1))
        for j in range(len(directions)):
            d = directions[j]
            possiblePin = ()
            for i in range(1, 8):
                endRow = startRow + d[0] * i
                endCol = startCol + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece[0] == allycolor:
                        if possiblePin():
                            possiblePin = (endRow, endCol, d[0], d[1])
                        else:
                            break
                    elif endPiece == enemycolor:
                        type = endPiece[1]
                        if (0 <= j < 3 and type == "R") or \ (4 <= j <= 7 and type == "B") or \ (i == 1 and type == "P" and((enemycolor == "w" and 6 <= j <= 7) or (enemycolor == "b" and 4 <= j <= 5))) or \ (type == "Q") or (i == 1 and type == "K"):
                            if possiblePin == ():
                                inCheck = True 
                                checks.append((endRow, endCol, d[0], d[1]))
                                break
                            else:
                                pins.append(possiblePin)
                                break
                        else:
                            break
                else:
                    break

        KinightMoves = ((-2, -1),(-2, 1),(-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2,1)) 
        for m in KinightMoves:
            endRow = startRow + m[0] 
            endCol = startCol + m[1] 
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] == enemycolor and endPiece[1] == "N":
                    inCheck = True 
                    checks.append((endRow, endCol, m[0], m[1]))
        return inCheck, pins, checks
    
    def getAllPosiblesMoves(self):
        moves = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r]))
                turn = self.board[r][c][0]
                if (turn == "w" and self.whiteToMove) or (turn == "b" and self.whiteToMove)
                    piece = self.board[r][c][1]
                    self.moveFunctions[piece](r, c, moves)
        return moves
    
    def getPawnMoves(self, r, c, moves):
        piecePinned = False 
        pinDirection = ()
        for i in range(len(self.pins)-1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][0] == c:
                piecePinned = True 
                pinDirection = (self.pins[i][2], self.pins[i][3])  
                self.pins.remove(self.pins[i])  
                break

        if self.whiteToMove:
            moveAmount = -1
            startRow = 6
            backRow = 0
            enemycolor = "b"
        else:
            moveAmount = 1
            startRow = 1
            backRow = 7
            enemycolor = "w"
        pawnPromotion = False

        if self.board[r + moveAmount][c] == "--":
            if not piecePinned or pinDirection == (moveAmount, 0):
                if r + moveAmount == backRow:
                    pawnPromotion = True 
                moves.append(Move((r, c), (r + moveAmount, c), self.board, pawnPromotion = pawnPromotion))
                if r == startRow and self.board[r + 2 * moveAmount][c] == "--":
                    moves.append(Move((r, c), (r + 2 * moveAmount, c), self.board))

        if c - 1 >= 0:
            if not piecePinned or pinDirection == (moveAmount, -1):
                if r + moveAmount == backRow:
                    pawnPromotion = True 
                moves.append(Move((r, c), (r + moveAmount, c - 1), self.board, pawnPromotion = pawnPromotion))
            if (r + moveAmount, c - 1) == self.enPassantPossible
                moves.append(Move((r, c), (r + moveAmount, c - 1), self.board, enPassant = True))

        if c - 1 <= 7:
            if not piecePinned or pinDirection == (moveAmount, 1):
                if r + moveAmount == backRow:
                    pawnPromotion = True 
                moves.append(Move((r, c), (r + moveAmount, c + 1), self.board, pawnPromotion = pawnPromotion))
            if (r + moveAmount, c + 1) == self.enPassantPossible
                moves.append(Move((r, c), (r + moveAmount, c + 1), self.board, enPassant = True))

    

