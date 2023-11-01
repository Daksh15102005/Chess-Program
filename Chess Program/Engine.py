class GameState:
    whiteToMove: bool
    def __init__(self):
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]]

        self.movefunctions = {'p': self.getPawnmoves, 'R': self.getRookMoves, 'N': self.getKnightmoves,
                              'B': self.getBishopmoves, 'Q': self.getQueenmoves, 'K': self.getKingmoves}
        self.whiteToMove = True
        self.moveLog = []
        self.whitekinglocation = (7, 4)
        self.blackkinglocation = (0, 4)
        self.incheck = False
        self.pins = []
        self.checks = []
        self.checkmate = False
        self.stalemate = False
        self.enpassantPossible = ()
        self.whiteCastlekingside = True
        self.whiteCastlequeenside = True
        self.blackCastlekingside = True
        self.blackCastlequeenside = True
        self.currentCalingRight = CatleRights(True, True, True, True)
        self.castleRightsLog = [CatleRights(self.whiteCastlekingside, self.blackCastlequeenside,
                                            self.whiteCastlequeenside, self.blackCastlequeenside)]
    def makeMove(self, move):# Legal moves
        self.board[move.startrow][move.startcol] = '--'
        self.board[move.endrow][move.endcol] = move.pieceMoved
        self.moveLog.append(move)
        self.whiteToMove = not self.whiteToMove
        if move.pieceMoved == 'wK':
            self.whitekinglocation = (move.endrow, move.endcol)
        elif move.pieceMoved == 'bK':
            self.blackkinglocation = (move.endrow, move.endcol)
        if move.isPawnPromotion:
            # piecechoice = input('What piece you want? :')
            self.board[move.endrow][move.endcol] = move.pieceMoved[0] + 'Q'
        # Enpassant
        if move.isEnpassantMove:
            self.board[move.startrow][move.endcol] = '--'
        if move.pieceMoved[1] == 'p' and abs(move.startrow - move.endrow) == 2:
            self.enpassantPossible = ((move.startrow + move.endrow) // 2, move.endcol)
        else:
            self.enpassantPossible = ()
        self.updaeCatleRights(move)        # Castle
        self.castleRightsLog.append(CatleRights(self.whiteCastlekingside, self.blackCastlequeenside,
                                                self.whiteCastlequeenside, self.blackCastlequeenside))
        if move.Castle:
            if move.endcol - move.startcol == 2:
                self.board[move.endrow][move.endcol - 1] = self.board[move.endrow][move.endcol + 1]
                self.board[move.endrow][move.endcol + 1] = '--'
            else:
                self.board[move.endrow][move.endcol + 1] = self.board[move.endrow][move.endcol - 2]
                self.board[move.endrow][move.endcol - 2] = '--'
    def undoMove(self):
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            self.board[move.startrow][move.startcol] = move.pieceMoved
            self.board[move.endrow][move.endcol] = move.piececaptured
            self.whiteToMove = not self.whiteToMove
            if move.pieceMoved == 'wK':
                self.whitekinglocation = (move.endrow, move.endcol)
            elif move.pieceMoved == 'bK':
                self.blackkinglocation = (move.endrow, move.endcol)
            if move.isEnpassantMove:
                self.board[move.endrow][move.endcol] = '--'
                self.board[move.startrow][move.endcol] = move.piececaptured
                self.enpassantPossible = (move.endrow, move.endcol)
            if move.pieceMoved[1] == 'p' and abs(move.startrow - move.endrow) == 2:
                self.enpassantPossible = ()
            self.castleRightsLog.pop()            # Castle Rights
            castleRights = self.castleRightsLog[-1]
            self.whiteCastlekingside = castleRights.wks
            self.blackCastlekingside = castleRights.bks
            self.whiteCastleQueenside = castleRights.wqs
            self.blackCastleQueenside = castleRights.bqs
            if move.Castle:
                if move.endcol - move.startcol == 2:  # kingside
                    self.board[move.endrow][move.endcol + 1] = self.board[move.endrow][move.endcol - 1]
                    self.board[move.endrow][move.endcol - 1] = '--'
                else:
                    self.board[move.endrow][move.endcol - 2] = self.board[move.endrow][move.endcol + 1]
                    self.board[move.endrow][move.endcol + 1] = '--'
            self.checkmate = False
            self.stalemate = False

    def updaeCatleRights(self, move):
        if move.pieceMoved == 'wK':
            self.whiteCastlequeenside = False
            self.whiteCastlekingside = False

        elif move.pieceMoved == 'bK':
            self.blackCastlequeenside = False
            self.blackCastlekingside = False

        elif move.pieceMoved == 'wR':
            if move.startrow == 7:
                if move.startcol == 0:
                    self.whiteCastlekingside = False
                elif move.startcol == 7:
                    self.whiteCastlekingside = False

        elif move.pieceMoved == 'bR':
            if move.startrow == 0:
                if move.startcol == 7:
                    self.blackCastlekingside = False
                elif move.startcol == 0:
                    self.blackCastlequeenside = False

        elif move.piececaptured == 'wR':
            if move.startrow == 7:
                if move.startcol == 0:
                    self.whiteCastlekingside = False
                elif move.startcol == 7:
                    self.whiteCastlekingside = False

        elif move.piececaptured == 'bR':
            if move.startrow == 0:
                if move.startcol == 7:
                    self.blackCastlekingside = False
                elif move.startcol == 0:
                    self.blackCastlequeenside = False

    def getvalidMoves(self):    # valid moves by pieces
        moves = []
        self.incheck, self.pins, self.checks = self.checkforpinsandchecks()
        if self.whiteToMove:
            kingrow = self.whitekinglocation[0]
            kingcol = self.whitekinglocation[1]
        else:
            kingrow = self.blackkinglocation[0]
            kingcol = self.blackkinglocation[1]
        if self.incheck:
            print("incheck")
            if len(self.checks) == 1:
                moves = self.getallposiblemoves()
                check = self.checks[0]
                checkrow = check[0]
                checkcol = check[1]
                piecechecking = self.board[checkrow][checkcol]
                validsquares = []
                if piecechecking[1] == 'N':
                    validsquares = [(checkrow, checkcol)]
                else:
                    for i in range(1, 8):
                        validsquare = (kingrow + check[2] * i, kingcol + check[3] * i)
                        validsquares.append(validsquare)
                        if validsquare[0] == checkrow and validsquare[1] == checkcol:
                            break
                for i in range(len(moves) - 1, -1, -1):
                    if moves[i].pieceMoved[1] != 'K':
                        if not (moves[i].endrow, moves[i].endcol) in validsquares:
                            moves.remove(moves[i])
            else:
                self.getKingmoves(kingrow, kingcol, moves)
        else:
            moves = self.getallposiblemoves()
        if len(moves) == 0:
            if self.incheck:
                self.checkmate = True
                print(self.whitekinglocation)
                print(self.blackkinglocation)
            else:
                self.stalemate = True
        else:
            self.checkmate = False
            self.stalemate = False
        return moves
    def getallposiblemoves(self):
        move = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn = self.board[r][c][0]
                if (turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    self.movefunctions[piece](r, c, move)
        return move

    def getPawnmoves(self, r, c, move):
        piecepinned = False
        pindirection = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecepinned = True
                pindirection = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break

        if self.whiteToMove:
            if self.board[r - 1][c] == '--':
                if not piecepinned or pindirection == (-1, 0):
                    move.append(Move((r, c), (r - 1, c), self.board))
                    if r == 6 and self.board[r - 2][c] == '--':
                        move.append(Move((r, c), (r - 2, c), self.board))
            # Captures
            if c - 1 >= 0:
                if self.board[r - 1][c - 1][0] == 'b':
                    if not piecepinned or pindirection == (-1, -1):
                        move.append(Move((r, c), (r - 1, c - 1), self.board))
                if (r - 1, c - 1) == self.enpassantPossible:
                    move.append(Move((r, c), (r - 1, c - 1), self.board, isEnpassantMove=True))

            if c + 1 <= 7:
                if self.board[r - 1][c + 1][0] == 'b':
                    if not piecepinned or pindirection == (-1, 1):
                        move.append(Move((r, c), (r - 1, c + 1), self.board))
                if (r - 1, c + 1) == self.enpassantPossible:
                    move.append(Move((r, c), (r - 1, c + 1), self.board, isEnpassantMove=True))
        else:
            if self.board[r + 1][c] == '--':
                if not piecepinned or pindirection == (1, 0):
                    move.append(Move((r, c), (r + 1, c), self.board))
                    if r == 1 and self.board[r + 2][c] == '--':
                        move.append(Move((r, c), (r + 2, c), self.board))
            # Captures
            if c - 1 >= 0:
                if self.board[r + 1][c - 1][0] == 'w':
                    if not piecepinned or pindirection == (1, -1):
                        move.append(Move((r, c), (r + 1, c - 1), self.board))
                if (r + 1, c - 1) == self.enpassantPossible:
                    move.append(Move((r, c), (r + 1, c - 1), self.board, isEnpassantMove=True))
            if c + 1 <= 7:
                if self.board[r + 1][c + 1][0] == 'w':
                    if not piecepinned or pindirection == (1, 1):
                        move.append(Move((r, c), (r + 1, c + 1), self.board))
                if (r + 1, c + 1) == self.enpassantPossible:
                    move.append(Move((r, c), (r + 1, c + 1), self.board, isEnpassantMove=True))

    def getRookMoves(self, r, c, move):
        piecepinned = False
        pindirection = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecepinned = True
                pindirection = (self.pins[i][2], self.pins[i][3])
                if self.board[r][c][1] != 'Q':
                    self.pins.remove(self.pins[i])
                break
        direction = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        if self.whiteToMove:
            enemy = 'b'
        else:
            enemy = 'w'
        for d in direction:
            for i in range(1, 8):
                lastrow = r + d[0] * i
                lastcol = c + d[1] * i
                if 0 <= lastrow < 8 and 0 <= lastcol < 8:
                    if not piecepinned or pindirection == d or pindirection == (-d[0], -d[1]):
                        lastpiece = self.board[lastrow][lastcol]
                        if lastpiece == '--':
                            move.append(Move((r, c), (lastrow, lastcol), self.board))
                        elif lastpiece[0] == enemy:
                            move.append(Move((r, c), (lastrow, lastcol), self.board))
                            break
                        else:
                            break
                else:
                    break

    def getBishopmoves(self, r, c, move):
        piecepinned = False
        pindirection = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecepinned = True
                pindirection = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break
        direction = ((1, 1), (-1, 1), (1, -1), (-1, -1))
        if self.whiteToMove:
            enemy = 'b'
        else:
            enemy = 'w'
        for d in direction:
            for i in range(1, 8):
                lastrow = r + d[0] * i
                lastcol = c + d[1] * i
                if 0 <= lastrow < 8 and 0 <= lastcol < 8:
                    if not piecepinned or pindirection == d or pindirection == (-d[0], -d[1]):
                        if self.board[lastrow][lastcol] == '--':
                            move.append(Move((r, c), (lastrow, lastcol), self.board))
                        elif self.board[lastrow][lastcol][0] == enemy:
                            move.append(Move((r, c), (lastrow, lastcol), self.board))
                            break
                        else:
                            break
                else:
                    break

    def getQueenmoves(self, r, c, move):
        self.getRookMoves(r, c, move)
        self.getBishopmoves(r, c, move)

    def checkforpinsandchecks(self):
        pins = []
        checks = []
        incheck = False
        if self.whiteToMove:
            enemycolor = 'b'
            allycolor = 'w'
            startrow = self.whitekinglocation[0]
            startcol = self.whitekinglocation[1]
        else:
            enemycolor = 'w'
            allycolor = 'b'
            startrow = self.blackkinglocation[0]
            startcol = self.blackkinglocation[1]
        direction = ((-1, 0), (0, -1), (1, 0), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1))
        for j in range(len(direction)):
            d = direction[j]
            posiblepin = ()
            for i in range(1, 8):
                endrow = startrow + d[0] * i
                endcol = startcol + d[1] * i
                if 0 <= endrow < 8 and 0 <= endcol < 8:
                    endpiece = self.board[endrow][endcol]
                    if endpiece[0] == allycolor and endpiece[1] != 'K':
                        if posiblepin == ():
                            posiblepin = (endrow, endcol, d[0], d[1])
                        else:
                            break
                    elif endpiece[0] == enemycolor:
                        type = endpiece[1]
                        if (0 <= j <= 3 and type == 'R') or \
                                (4 <= j <= 7 and type == 'B') or \
                                (i == 1 and type == 'p' and ((enemycolor == 'w' and 6 <= j <= 7) or
                                                             (enemycolor == 'b' and 4 <= j <= 5))) or \
                                (type == 'Q') or (i == 1 and type == 'K'):

                            if posiblepin == ():
                                incheck = True
                                checks.append((endrow, endcol, d[0], d[1]))
                                break
                            else:
                                pins.append(posiblepin)
                                break
                        else:
                            break
                else:
                    break
        knightmoves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        for m in knightmoves:
            endrow = startrow + m[0]
            endcol = startcol + m[1]
            if 0 <= endrow < 8 and 0 <= endcol < 8:
                endpiece = self.board[endrow][endcol]
                if endpiece[0] == enemycolor and endpiece[1] == 'N':
                    incheck = True
                    checks.append((endrow, endcol, m[0], m[1]))
        return incheck, pins, checks

    def getKnightmoves(self, r, c, move):
        piecepinned = False
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecepinned = True
                self.pins.remove(self.pins[i])
                break
        direction = ((-1, -2), (-2, -1), (-2, 1), (-1, 2),
                     (1, 2), (2, 1), (2, -1), (1, -2))
        if self.whiteToMove:
            friend = 'w'
        else:
            friend = 'b'
        for i in range(8):
            lastrow = r + direction[i][0]
            lastcol = c + direction[i][1]
            if 0 <= lastrow < 8 and 0 <= lastcol < 8:
                if not piecepinned:
                    endpiece = self.board[lastrow][lastcol]
                    if endpiece[0] != friend:
                        move.append(Move((r, c), (lastrow, lastcol), self.board))

    def getKingmoves(self, r, c, move):
        rowmoves = (-1, -1, -1, 0, 0, 1, 1, 1)
        colmoves = (-1, 0, 1, -1, 1, -1, 0, 1)
        allycolor = 'w' if self.whiteToMove else 'b'
        for i in range(8):
            endrow = r + rowmoves[i]
            endcol = c + colmoves[i]
            if 0 <= endrow < 8 and 0 <= endcol < 8:
                endpiece = self.board[endrow][endcol]
                if endpiece[0] != allycolor:
                    if allycolor == 'w':
                        self.whitekinglocation = (endrow, endcol)
                    else:
                        self.blackkinglocation = (endrow, endcol)
                    incheck, pins, checks = self.checkforpinsandchecks()
                    if not incheck:
                        move.append(Move((r, c), (endrow, endcol), self.board))
                    if allycolor == 'w':
                        self.whitekinglocation = (r, c)
                    else:
                        self.blackkinglocation = (r, c)
        self.getcastlemoves(r, c, move, allycolor)

    def getcastlemoves(self, r, c, moves, allycolor):
        inCheck = self.squareUnderAttack(r, c, allycolor)
        if inCheck:
            return
        if (self.whiteToMove and self.whiteCastlekingside) or (not self.whiteToMove and self.blackCastlekingside):
            self.getkingsidecastlemoves(r, c, moves, allycolor)
        if (self.whiteToMove and self.whiteCastlequeenside) or (not self.whiteToMove and self.blackCastlequeenside):
            self.getqueensidecastlemoves(r, c, moves, allycolor)

    def getkingsidecastlemoves(self, r, c, moves, allycolor):
        if self.board[r][c + 1] == '--' and self.board[r][c + 2] == '--' and \
                not self.squareUnderAttack(r, c + 1, allycolor) and not self.squareUnderAttack(r, c + 2, allycolor):
            moves.append(Move((r, c), (r, c + 2), self.board, Castle=True))

    def getqueensidecastlemoves(self, r, c, moves, allycolor):
        if self.board[r][c - 1] == '--' and self.board[r][c - 2] == '--' and self.board[r][c - 3] == '--' and \
                not self.squareUnderAttack(r, c - 1, allycolor) and not self.squareUnderAttack(r, c - 2, allycolor):
            moves.append(Move((r, c), (r, c - 2), self.board, Castle=True))

    def squareUnderAttack(self, r, c, allycolor):
        enemycolor = 'w' if allycolor == 'b' else 'b'
        direction = ((-1, 0), (0, -1), (1, 0), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1))
        for j in range(len(direction)):
            d = direction[j]
            for i in range(1, 8):
                endrow = r + d[0] * i
                endcol = c + d[1] * i
                if 0 <= endrow < 8 and 0 <= endcol < 8:
                    endpiece = self.board[endrow][endcol]
                    if endpiece[0] == allycolor:
                        break
                    elif endpiece[0] == enemycolor:
                        type = endpiece[1]
                        if (0 <= j <= 3 and type == 'R') or \
                                (4 <= j <= 7 and type == 'B') or \
                                (i == 1 and type == 'p' and (
                                        (enemycolor == 'w' and 6 <= j <= 7) or (enemycolor == 'b' and 4 <= j <= 5)))\
                                or (type == 'Q') or (i == 1 and type == 'K'):
                            return True
                        else:
                            break
                else:
                    break
        knightmoves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        for m in knightmoves:
            endrow = r + m[0]
            endcol = c + m[1]
            if 0 <= endrow < 8 and 0 <= endcol < 8:
                endpiece = self.board[endrow][endcol]
                if endpiece[0] == enemycolor and endpiece[1] == 'N':
                    return True
        return False

class CatleRights:
    def __init__(self, wks, bks, wqs, bqs):
        self.wks = wks
        self.bks = bks
        self.wqs = wqs
        self.bqs = bqs

class Move:
    ranksToRows = {'1': 7, "2": 6, "3": 5, "4": 4,
                   "5": 3, "6": 2, "7": 1, "8": 0}
    rowToRanks = {v: k for k, v in ranksToRows.items()}
    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3,
                   "e": 4, "f": 5, "g": 6, "h": 7}
    colsToFiles = {v: k for k, v in filesToCols.items()}
    def __init__(self, startsq, endsq, board, isEnpassantMove=False, Castle=False):
        self.startrow = startsq[0]
        self.startcol = startsq[1]
        self.endrow = endsq[0]
        self.endcol = endsq[1]
        self.pieceMoved = board[self.startrow][self.startcol]
        self.piececaptured = board[self.endrow][self.endcol]
        self.isPawnPromotion = (self.pieceMoved == "wp" and self.endrow == 0) or (
                    self.pieceMoved == 'bp' and self.endrow == 7)
        # self.isenpassantPossible = (self.pieceMoved[1] == 'p' and (self.endrow, self.endcol) == enpassantPossible)
        self.isEnpassantMove = isEnpassantMove
        if self.isEnpassantMove:
            self.piececaptured = 'wp' if self.pieceMoved == 'bp' else 'bp'

        self.Castle = Castle

        self.moveID = self.startrow * 1000 + self.startcol * 100 + self.endrow * 10 + self.endcol

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False

    def getChessNotation(self):
        return self.getRankFiles(self.startrow, self.startcol) + self.getRankFiles(self.endrow, self.endcol)

    def getRankFiles(self, r, c):
        return self.colsToFiles[c] + self.rowToRanks[r]
