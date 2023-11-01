
import pygame as p

import Engine, ChessComputer

p.init()

p.display.set_caption("Chess")
icon = p.image.load("chess.png")
p.display.set_icon(icon)

width = height = 800
Dimension = 8
sqSize = height // Dimension
MaxFPS = 15
Images = {}


def loadimages():
    pieces = ["wR", "wN", "wB", "wQ", "wK", "bR", "bN", "bB", "bQ", "bK", "bp", "wp"]
    for piece in pieces:
        Images[piece] = p.transform.scale(p.image.load(piece + ".png"), (sqSize, sqSize))


def main():
    p.init()
    screen = p.display.set_mode((width, height))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = Engine.GameState()
    movemade = False


    validmoves = gs.getvalidMoves()
    loadimages()
    running = True
    sqselected = ()
    plyclicks = []
    gameover = False
    player1 = True   # player one is white
    player2 = False  # True = Human
    while running:
        human = (gs.whiteToMove and player1) or(not gs.whiteToMove and player2)
        for event in p.event.get():
            if event.type == p.QUIT:
                running = False
            elif event.type == p.MOUSEBUTTONDOWN:
                if not gameover and human:

                    location = p.mouse.get_pos()
                    cl = location[0]//sqSize
                    rw = location[1]//sqSize
                    if sqselected == (rw, cl):
                        sqselected = ()
                        plyclicks = []
                    else:
                        sqselected = (rw, cl)
                        plyclicks.append(sqselected)
                    if len(plyclicks) == 2:
                        move = Engine.Move(plyclicks[0], plyclicks[1], gs.board)
                        print(move.getChessNotation())
                        for i in range(len(validmoves)):
                            if move == validmoves[i]:
                                gs.makeMove(validmoves[i])
                                movemade = True
                            sqselected = ()
                            plyclicks = []

            elif event.type == p.KEYDOWN:
                if event.key == p.K_z:
                    gs.undoMove()
                    movemade = True
                if event.key == p.K_r:
                    gs = Engine.GameState()
                    movemade = False
                    validmoves = gs.getvalidMoves()
                    sqselected = ()
                    plyclicks = []

        # computer
        if not gameover and not human:
            computermove = ChessComputer.findbestmove(gs, validmoves)
            if computermove is None:
                computermove = ChessComputer.findrandomove(validmoves)

            gs.makeMove(computermove)
            movemade = True



        if movemade:
            validmoves = gs.getvalidMoves()
            movemade = False

        drawgamestate(screen, gs, validmoves, sqselected)

        if gs.checkmate:
            gameover = True
            if gs.whiteToMove:
                drawtext(screen, 'Black won by Checkmate')
            else:
                drawtext(screen, 'White won by Checkmate')
        elif gs.stalemate:
            gameover = True
            drawtext(screen, 'Stalemate')

        clock.tick(MaxFPS)
        p.display.flip()


def highlightsquares(screen, gs, validmoves, sqselected):
    if sqselected != ():
        r, c = sqselected
        if gs.board[r][c][0] == ('w' if gs.whiteToMove else 'b'):
            s = p.Surface((sqSize, sqSize))
            s.set_alpha(150)
            s.fill(p.Color('IndianRed1'))
            screen.blit(s, (c*sqSize, r*sqSize))
            s.set_alpha(100)
            s.fill(p.Color('yellow'))
            for moves in validmoves:
                if moves.startrow == r and moves.startcol == c:
                    screen.blit(s, (moves.endcol * sqSize, moves.endrow * sqSize))



def drawgamestate(screen, gs, validmoves, sqselected):
    drawboard(screen)
    highlightsquares(screen, gs, validmoves, sqselected)
    drawpieces(screen, gs.board)

def drawboard(screen):
    colors = [p.Color("PaleGreen4"), p.Color("gainsboro")]
    for r in range(Dimension):
        for c in range(Dimension):
            color = colors[((r + c) % 2)]
            p.draw.rect(screen, color, p.Rect(c * sqSize, r * sqSize, sqSize, sqSize))


def drawpieces(screen, board):
    for r in range(Dimension):
        for c in range(Dimension):
            piece = board[r][c]
            if piece != "--":
                screen.blit(Images[piece], p.Rect(c * sqSize, r * sqSize, sqSize, sqSize))



def drawtext(screen, text):
    font = p.font.SysFont('Helvitca', 66, True, False)
    textObject = font.render(text, False, p.Color('grey30'))
    textlocation = p.Rect(0, 0, width, height).move(width / 2 - textObject.get_width() / 2,
                                                    height / 2 - textObject.get_height() / 2)
    screen.blit(textObject, textlocation)





if __name__ == "__main__":
    main()















