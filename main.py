# Imports modules to control raspberry pi GPIO
import RPi.GPIO as GPIO
import time

import charlieplexing

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
    def initialisePieces(self):
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
    resetRowPins()
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

# Function that waits for a square to turn from on to off
def detectFallingAtPosition(coordinates):
    GPIO.output(rowPins[coordinates[1]], 1)
    GPIO.add_event_detect(columnPins[coordinates[0]], GPIO.FALLING)
    numberRows = [8, 7, 6, 5, 4, 3, 2, 1]
    numberCols = [9, 10, 11, 12, 13, 14, 15, 16]
    while True:
        # Lights up position
        charlieplexing.turnOn(numberRows[coordinates[1]])
        charlieplexing.turnOn(numberCols[coordinates[0]])

        # Breaks loop once piece is picked up
        if GPIO.event_detected(columnPins[coordinates[0]]):
            GPIO.remove_event_detect(columnPins[coordinates[0]])
            charlieplexing.turnOn(0)
            break
        
    #GPIO.wait_for_edge(columnPins[coordinates[0]], GPIO.FALLING)
    GPIO.output(rowPins[coordinates[1]], 0)

# Function that waits for a square to turn from off to on
def detectRisingAtPosition(coordinates):
    GPIO.output(rowPins[coordinates[1]], 1)
    GPIO.add_event_detect(columnPins[coordinates[0]], GPIO.RISING)
    numberRows = [8, 7, 6, 5, 4, 3, 2, 1]
    numberCols = [9, 10, 11, 12, 13, 14, 15, 16]
    while True:
        # Lights up position
        charlieplexing.turnOn(numberRows[coordinates[1]])
        charlieplexing.turnOn(numberCols[coordinates[0]])

        # Breaks loop once piece is placed down
        if GPIO.event_detected(columnPins[coordinates[0]]):
            GPIO.remove_event_detect(columnPins[coordinates[0]])
            charlieplexing.turnOn(0)
            break
        
    #GPIO.wait_for_edge(columnPins[coordinates[0]], GPIO.FALLING)
    GPIO.output(rowPins[coordinates[1]], 0)

# Will return True if there is currently a piece at the given coordinates
def isOccupied(coordinates):
    board = currentBoard.getBoard()
    if board[coordinates[1]][coordinates[0]] != 0:
        return True
    else:
        return False


# Function to make sure that the pieces are where they're meant to be
# Recursively calls itself until all pieces are in the correct position
def checkBoardIsLegal():
    board = currentBoard.getBoard()

    for row in range(8):
        resetRowPins()
        GPIO.output(rowPins[row], 1)
        for column in range(8):
            # First checks for pieces where no pieces should be
            if board[row][column] == 0 and GPIO.input(columnPins[column]) == 1:
                print(f"Remove piece from: {convertToChessNotation([column, row])}")
                detectFallingAtPosition([column, row])

                resetRowPins()
                checkBoardIsLegal()
                return

            # Then checks for empty spaces where pieces should be
            elif board[row][column] != 0 and GPIO.input(columnPins[column]) == 0:
                print(f"Place {board[row][column].colour.capitalize()} {board[row][column].pieceType.capitalize()} on {convertToChessNotation([column, row])}")
                detectRisingAtPosition([column, row])

                resetRowPins()
                checkBoardIsLegal()
                return

    resetRowPins()


# Function to tell player where to move pieces
def moveComputerPieces(moveFrom, moveTo, move):
    # Tells user which piece to pick up, checks for piece removal
    print(f"Move piece from {move[0:2]}")
    detectFallingAtPosition(moveFrom)

    # Checks if moveTo position is already occupied, if so tells user to remove it
    if isOccupied(moveTo):
        print(f"Remove piece from {move[2:]}")
        detectFallingAtPosition(moveTo)

    # Tells user where to move piece
    print(f"Move piece to {move[2:]}")
    detectRisingAtPosition(moveTo)

    print("Thank you!")
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
    moveFrom = reportChange()
    print(f"From: {moveFrom}")
    moveTo = reportChange()
    print(f"To {moveTo}")

    if isOccupied(moveTo):
        print("Place down piece")
        detectRisingAtPosition(moveTo)

    move = convertToChessNotation(moveFrom) + convertToChessNotation(moveTo)

    if stockfish.is_move_correct(move):
        print("legal shmegle")
        currentBoard.setBoard(moveFrom, moveTo, move)
        currentBoard.getBoard()
    else:
        print("Not a legal move")
        checkBoardIsLegal()
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
p.initialisePieces()
currentBoard = BoardRecord(p)
pinSetup()

m = input("")
resetRowPins()
checkBoardIsLegal()

while True:
    getPlayerMove()
    checkBoardIsLegal()
    evaluation = stockfish.get_evaluation()
    if evaluation["type"] == 'mate' and evaluation["value"] == 0:
        charlieplexing.slideFast()
    
    generateMove()
    checkBoardIsLegal()
    if evaluation["type"] == 'mate' and evaluation["value"] == 0:
        charlieplexing.slideFast()
