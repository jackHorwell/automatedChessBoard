class Piece:
    def __init__(self, colour, pieceType, pieceSymbol):
        self.colour = colour
        self.pieceType = pieceType
        self.pieceSymbol = pieceSymbol

wp = Piece("white", "pawn", "♙")
wr = Piece("white", "rook", "♖")
wkn = Piece("white", "knight", "♘")
wb = Piece("white", "bishop", "♗")
wq = Piece("white", "queen", "♕")
wk = Piece("white", "king", "♔")

bp = Piece("black", "pawn", "♟")
br = Piece("black", "rook", "♜")
bkn = Piece("black", "knight", "♞")
bb = Piece("black", "bishop", "♝")
bq = Piece("black", "queen", "♛")
bk = Piece("black", "king", "♚")

class BoardState:
    board = [[0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0]]

    def __init__(self, wp=wp, wr=wr, wkn=wkn, wb=wb, wq=wq, wk=wk, bp=bp, br=br, bkn=bkn, bb=bb, bq=bq, bk=bk):
        self.wp = wp
        self.wr = wr
        self.wkn = wkn
        self.wb = wb
        self.wq = wq
        self.wk = wk

        self.bp = bp
        self.br = br
        self.bkn = bkn
        self.bb = bb
        self.bq = bq
        self.bk = bk

        self.board[0][0], self.board[0][7] = wr, wr
        self.board[0][1], self.board[0][6] = wkn, wkn
        self.board[0][2], self.board[0][5] = wb, wb
        self.board[0][3] = wq
        self.board[0][4] = wk
        for square in self.board[1]:
            square = wp

        self.board[7][0], self.board[7][7] = br, br
        self.board[7][1], self.board[7][6] = bkn, bkn
        self.board[7][2], self.board[7][5] = bb, bb
        self.board[7][3] = bq
        self.board[7][4] = bk
        for square in self.board[6]:
            square = bp

    def printBoard():
        for row in range(7, -1, -1):
            for square in row:
                if square != 0:
                    
            print(self.board[row])

    # Variable to store previous move
    #previousMove = 

    #function to move pieces based on input
    def movePiece(self, pieceFrom, pieceTo):
        self.board[pieceTo[0]][pieceTo[1]] = self.board[pieceFrom[0]][pieceFrom[1]]
        self.board[pieceFrom[0]][pieceFrom[1]] = 0
