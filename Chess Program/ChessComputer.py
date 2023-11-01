
import random

piecescore = {'K': 89, 'Q': 9, 'R': 5, 'B': 3, 'N': 3, 'p': 1}
CHECKMATE = 1000
STALEMATE = 0
DEPTH = 5

def findrandomove(validmoves):
    return validmoves[random.randint(0, len(validmoves)-1)]

def findbestmove(gs, validmoves):
    turnMultiplier = 1 if gs.whiteToMove else -1
    opponentMinMaxScore = CHECKMATE
    bestPlayerMove = None
    random.shuffle(validmoves)
    for playerMove in validmoves:
        gs.makeMove(playerMove)
        opponentsMoves = gs.getvalidMoves()
        if gs.stalemate:
            opponentMaxScore = STALEMATE
        elif gs.checkmate:
            opponentMaxScore = -CHECKMATE
        else:
            opponentMaxScore = -CHECKMATE
            for opponentsMove in opponentsMoves:
                gs.makeMove(opponentsMove)
                gs.getvalidMoves()
                if gs.checkmate:
                    score = CHECKMATE
                elif gs.stalemate:
                    score = STALEMATE
                else:
                    score = -turnMultiplier * Scorematerial(gs.board)
                if score > opponentMaxScore:
                     opponentMaxScore = score
                gs.undoMove()
        if opponentMaxScore < opponentMinMaxScore:
            opponentMinMaxScore = opponentMaxScore
            bestPlayerMove = playerMove
        gs.undoMove()
    return bestPlayerMove



def findBestMoveMinMax(gs, validMoves):
    global nextMove
    nextMove = None
    findMoveMinMax(gs, validMoves, DEPTH, gs.whiteToMove)
    return nextMove



def findMoveMinMax(gs, validmoves, depth, whiteToMove):
    global nextMove
    if depth == 0:
        return Scorematerial(gs.board)

    if whiteToMove:
        maxScore = -CHECKMATE
        random.shuffle(validmoves)
        for move in validmoves:
            gs.makeMove(move)
            nextMoves = gs.getvalidMoves()
            score = findMoveMinMax(gs, nextMoves, depth - 1, False)
            if score > maxScore:
                maxScore = score
                if depth == DEPTH:
                    nextMove = move
            gs.undoMove()
            return maxScore
    else:
        minScore = CHECKMATE
        for move in validmoves:
            gs.makeMove(move)
            nextMoves = gs.getvalidMoves()
            score = findMoveMinMax(gs, nextMoves, depth - 1, True)
            if score < minScore:
                minScore = score
                if depth == DEPTH:
                    nextMove = move
            gs.undoMove()
        return minScore

def scoreBoard(gs):
    if gs.checkmate:
        if gs.whiteToMove:      # +ve score for white
            return -CHECKMATE
        else:                   #-ve score for Black
            return CHECKMATE
    elif gs.stalemate:
        return STALEMATE
    score = 0
    for rows in gs.board:
        for square in rows:
            if square[0] == 'w':
                score += piecescore[square[1]]
            elif square[0] == 'b':
                score -= piecescore[square[1]]
    return score



def Scorematerial(board):
    score = 0
    for rows in board:
        for square in rows:
            if square[0] == 'w':
                score += piecescore[square[1]]
            elif square[0] == 'b':
                score -= piecescore[square[1]]
    return score
































