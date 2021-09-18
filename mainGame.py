# Imports modules to control raspberry pi GPIO
import RPi.GPIO as GPIO
import time

# Sets up Stockfish engine
from stockfish import Stockfish
stockfish = Stockfish("/home/pi/Downloads/a-stockf")
stockfish = Stockfish(parameters={"Threads": 2, "Minimum Thinking Time": 30})

# 97 is the ASCII code for a, using this we can reduce this down to a numeric form
asciiA = 97

# Class to store piece attributes like colour and type
class Piece:
    def __init__(self, colour, pieceType, icon):
        self.colour = colour
        self.pieceType = pieceType
        self.icon = icon

# Class to group together piece initialisation
class Pieces:
    def __init__(self):
        # Initalises the piece objects and passes their attributes
        self.wp = Piece("white", "pawn", "♙")
        self.wr = Piece("white", "rook", "♖")
        self.wkn = Piece("white", "knight", "♞")
        self.wb = Piece("white", "bishop", "♗")
        self.wq = Piece("white", "queen", "♕")
        self.wk = Piece("white", "king", "♔")

        self.bp = Piece("black", "pawn", "♟")
        self.br = Piece("black", "rook", "♜")
        self.bkn = Piece("black", "knight", "♞")
        self.bb = Piece("black", "bishop", "♝")
        self.bq = Piece("black", "queen", "♛")
        self.bk = Piece("black", "king", "♚")

# Class to store the current state and last known legal state of the board
class BoardRecord:
    def __init__(self, p): 
        # Stack to store previous move
        self.previousMoves = []
        
        # Creates a 2D array to store piece locations
        self.board = [[p.wr,p.wkn,p.wb,p.wq,p.wk,p.wb,p.wkn,p.wr],
                 [p.wp,p.wp,p.wp,p.wp,p.wp,p.wp,p.wp,p.wp],
                 [0,0,0,0,0,0,0,0],
                 [0,0,0,0,0,0,0,0],
                 [0,0,0,0,0,0,0,0],
                 [0,0,0,0,0,0,0,0],
                 [p.bp,p.bp,p.bp,p.bp,p.bp,p.bp,p.bp,p.bp],
                 [p.br,p.bkn,p.bb,p.bq,p.bk,p.bb,p.bkn,p.br]]

    # Getter for board variable
    def getBoard(self):
        # Prints each row and converts objects into their assigned icons
        for row in range(7, -1, -1):
            rowToPrint = []
            for square in self.board[row]:
                if square != 0:   
                    rowToPrint.append(square.icon)
                else:
                    rowToPrint.append("0 ")
            print("".join(rowToPrint))

        return self.board


    # Setter for board variable
    # Takes two coordinates and moves a piece to it's new position
    def setBoard(self, pieceFrom, pieceTo, move):
        self.board[pieceTo[1]][pieceTo[0]] = self.board[pieceFrom[1]][pieceFrom[0]]
        
        self.board[pieceFrom[1]][pieceFrom[0]] = 0

        # Adds move made to the previousMoves array
        self.previousMoves.append(move)

        # Updates the moves made for the engine
        stockfish.set_position(self.previousMoves)


# Stores the pin numbers used for the rows and columns
# Index + 1 is the row number
rowPins = [23, 18, 11, 9, 10, 22, 27, 17]
columnPins = [21, 20, 16, 12, 7, 8, 25, 24]

# Sets the pins to be inputs or outputs
def pinSetup():
    GPIO.setmode(GPIO.BCM)
    
    for pin in rowPins:
        GPIO.setup(pin, GPIO.OUT)

    for pin in columnPins:
        GPIO.setup(pin, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

# Function to turn off all the row pins to make sure none are accidently left on
def resetRowPins():
    for pin in rowPins:
        GPIO.output(pin, 0)

# Function to return the position of pieces in a 2D array
def scanCurrentBoard():
    board = []
    
    # Provides power to rows one by one and checks columns for input
    # Stores the output to board array
    for row in range(8):
        board.append([])
        GPIO.output(rowPins[row], 1)
        for column in range(8):
            board[row].append(GPIO.input(columnPins[column]))

        GPIO.output(rowPins[row], 0)

    return board
    
    '''
    Used for development purposes, delete in final
    '''
    for i in range(7, -1, -1):
        print(" ".join(map(str,board[i])))

    print("\n\n")

# Takes the current state of the board and repeatedly checks
# for a change. Once found will return the position of the change
"""
Could optimise with wait for edge?
"""
def reportChange():
    oldBoard = scanCurrentBoard()
    
    while True:
        newBoard = scanCurrentBoard()
        
        if newBoard != oldBoard:
            for row in range(8):
                if newBoard[row] != oldBoard[row]:
                    for column in range(8):
                        if newBoard[row][column] != oldBoard[row][column]:
                            resetRowPins()
                            return [column, row]

# Function to make sure that the pieces are where they're meant to be


# Function to tell player where to move pieces
def moveComputerPieces(moveFrom, moveTo, move):
    # Tells user which piece to pick up, checks for piece removal
    GPIO.output(rowPins[moveFrom[1]], 1)
    print(f"Move piece from {move[0:2]}")
    GPIO.wait_for_edge(columnPins[moveFrom[0]], GPIO.FALLING)
    GPIO.output(rowPins[moveFrom[1]], 0)

    # Checks if a piece is being taken, if so tells user to remove it
    board = currentBoard.getBoard()
    if board[moveTo[1]][moveTo[0]] != 0:
        GPIO.output(rowPins[moveTo[1]], 1)
        print(f"Remove piece from {move[2:]}")
        GPIO.wait_for_edge(columnPins[moveTo[0]], GPIO.FALLING)
        GPIO.output(rowPins[moveTo[1]], 0)

    # Tells user where to move piece
    GPIO.output(rowPins[moveTo[1]], 1)
    print(f"Move piece to {move[2:]}")
    GPIO.wait_for_edge(columnPins[moveTo[0]], GPIO.RISING)
    GPIO.output(rowPins[moveTo[1]], 0)

    resetRowPins()

# Function to convert move to chess notation (for Stockfish)
# Example: "a2"
def convertToChessNotation(move):
    return chr(ord('a') + move[0]) + str(move[1] + 1)

# Function to convert chess notation to move
# Example: [1, 1]
def convertToMove(chessNotation):
    return [ord(chessNotation[0]) - asciiA, int(chessNotation[1]) - 1]

# Function to obtain the move a player makes
def getPlayerMove():
    fromMove = reportChange()
    print(f"From: {fromMove}")
    toMove = reportChange()
    print(f"To {toMove}")

    move = convertToChessNotation(fromMove) + convertToChessNotation(toMove)

    if stockfish.is_move_correct(move):
        print("legal shmegle")
        currentBoard.setBoard(fromMove, toMove, move)
        currentBoard.getBoard()
    else:
        print("Not a legal move")
        getPlayerMove()
        return

# Function to get the AI to generate a move
def generateMove():
    move = stockfish.get_best_move()
    # Splits move into where it's moving from and where it's moving to
    # Converts letters into their corresponding alphabet
    # Both arrays have: column then row
    fromMove = convertToMove(move[0:2])
    toMove = convertToMove(move[2:4])

    currentBoard.getBoard()
    moveComputerPieces(fromMove, toMove, move)
    currentBoard.setBoard(fromMove, toMove, move)

p = Pieces()
currentBoard = BoardRecord(p)
pinSetup()

getPlayerMove()
generateMove()
