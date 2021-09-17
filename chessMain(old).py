from Board import Board
from InputParser import InputParser
from AI import AI
import sys
import random
import gspread
from oauth2client.service_account import ServiceAccountCredentials

import RPi.GPIO as GPIO  # Used to control reed switches on board
import time

# Imports things for screen
import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import subprocess

# sys.exit()


GPIO.setwarnings(False)  # Remove unnecessary warning output
GPIO.setmode(GPIO.BCM)

GPIO.setup(14, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(15, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# Row and column pin numbers
rowPins = [5, 11, 9, 10, 22, 27, 17, 4]
colPins = [6, 13, 19, 26, 18, 23, 24, 25]

# Two dimensional array to represent board, used to check last position
boardShow = [[1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1]]
boardShowLegal = [[1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1], [0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0],
                  [1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1]]

# Set up screen
RST = 0

disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST)
disp.begin()
disp.clear()
disp.display()

width = disp.width
height = disp.height
image1 = Image.new('1', (width, height))
draw = ImageDraw.Draw(image1)
draw.rectangle((0, 0, width, height), outline=0, fill=0)

padding = -2
top = padding
bottom = height - padding
x = 0
font = ImageFont.load_default()


# Lights up LEDs using charlieplexing
def led1():
    GPIO.setup(8, GPIO.OUT)
    GPIO.setup(7, GPIO.OUT)
    GPIO.setup(12, GPIO.IN)
    GPIO.setup(16, GPIO.IN)
    GPIO.setup(20, GPIO.IN)

    GPIO.output(8, 0)
    GPIO.output(7, 1)
    GPIO.input(12)
    GPIO.input(16)
    GPIO.input(20)


def led2():
    GPIO.setup(8, GPIO.OUT)
    GPIO.setup(12, GPIO.OUT)
    GPIO.setup(16, GPIO.IN)
    GPIO.setup(7, GPIO.IN)
    GPIO.setup(20, GPIO.IN)

    GPIO.output(8, 0)
    GPIO.output(12, 1)
    GPIO.input(16)
    GPIO.input(7)
    GPIO.input(20)


def led3():
    GPIO.setup(8, GPIO.OUT)
    GPIO.setup(16, GPIO.OUT)
    GPIO.setup(12, GPIO.IN)
    GPIO.setup(7, GPIO.IN)
    GPIO.setup(20, GPIO.IN)

    GPIO.output(8, 0)
    GPIO.output(16, 1)
    GPIO.input(12)
    GPIO.input(7)
    GPIO.input(20)


def led4():
    GPIO.setup(8, GPIO.OUT)
    GPIO.setup(20, GPIO.OUT)
    GPIO.setup(16, GPIO.IN)
    GPIO.setup(7, GPIO.IN)
    GPIO.setup(12, GPIO.IN)

    GPIO.output(8, 0)
    GPIO.output(20, 1)
    GPIO.input(16)
    GPIO.input(7)
    GPIO.input(12)


def led5():
    GPIO.setup(8, GPIO.OUT)
    GPIO.setup(7, GPIO.OUT)
    GPIO.setup(16, GPIO.IN)
    GPIO.setup(12, GPIO.IN)
    GPIO.setup(20, GPIO.IN)

    GPIO.output(8, 1)
    GPIO.output(7, 0)
    GPIO.input(16)
    GPIO.input(12)
    GPIO.input(20)


def led6():
    GPIO.setup(8, GPIO.OUT)
    GPIO.setup(12, GPIO.OUT)
    GPIO.setup(16, GPIO.IN)
    GPIO.setup(7, GPIO.IN)
    GPIO.setup(20, GPIO.IN)

    GPIO.output(8, 1)
    GPIO.output(12, 0)
    GPIO.input(16)
    GPIO.input(7)
    GPIO.input(20)


def led7():
    GPIO.setup(8, GPIO.OUT)
    GPIO.setup(16, GPIO.OUT)
    GPIO.setup(7, GPIO.IN)
    GPIO.setup(12, GPIO.IN)
    GPIO.setup(20, GPIO.IN)

    GPIO.output(8, 1)
    GPIO.output(16, 0)
    GPIO.input(7)
    GPIO.input(12)
    GPIO.input(20)


def led8():
    GPIO.setup(8, GPIO.OUT)
    GPIO.setup(20, GPIO.OUT)
    GPIO.setup(16, GPIO.IN)
    GPIO.setup(12, GPIO.IN)
    GPIO.setup(7, GPIO.IN)

    GPIO.output(8, 1)
    GPIO.output(20, 0)
    GPIO.input(16)
    GPIO.input(12)
    GPIO.input(7)


def led9():
    GPIO.setup(7, GPIO.OUT)
    GPIO.setup(12, GPIO.OUT)
    GPIO.setup(16, GPIO.IN)
    GPIO.setup(20, GPIO.IN)
    GPIO.setup(8, GPIO.IN)

    GPIO.output(7, 0)
    GPIO.output(12, 1)
    GPIO.input(16)
    GPIO.input(8)
    GPIO.input(20)


def led10():
    GPIO.setup(12, GPIO.OUT)
    GPIO.setup(7, GPIO.OUT)
    GPIO.setup(16, GPIO.IN)
    GPIO.setup(20, GPIO.IN)
    GPIO.setup(8, GPIO.IN)

    GPIO.output(7, 1)
    GPIO.output(12, 0)
    GPIO.input(16)
    GPIO.input(20)
    GPIO.input(8)


def led11():
    GPIO.setup(7, GPIO.OUT)
    GPIO.setup(20, GPIO.OUT)
    GPIO.setup(16, GPIO.IN)
    GPIO.setup(12, GPIO.IN)
    GPIO.setup(8, GPIO.IN)

    GPIO.output(7, 0)
    GPIO.output(20, 1)
    GPIO.input(16)
    GPIO.input(12)
    GPIO.input(8)


def led12():
    GPIO.setup(12, GPIO.OUT)
    GPIO.setup(20, GPIO.OUT)
    GPIO.setup(16, GPIO.IN)
    GPIO.setup(7, GPIO.IN)
    GPIO.setup(8, GPIO.IN)

    GPIO.output(20, 1)
    GPIO.output(12, 0)
    GPIO.input(16)
    GPIO.input(8)
    GPIO.input(7)


def led13():
    GPIO.setup(16, GPIO.OUT)
    GPIO.setup(20, GPIO.OUT)
    GPIO.setup(8, GPIO.IN)
    GPIO.setup(12, GPIO.IN)
    GPIO.setup(7, GPIO.IN)

    GPIO.output(16, 0)
    GPIO.output(20, 1)
    GPIO.input(8)
    GPIO.input(12)
    GPIO.input(7)


def led14():
    GPIO.setup(7, GPIO.OUT)
    GPIO.setup(20, GPIO.OUT)
    GPIO.setup(16, GPIO.IN)
    GPIO.setup(12, GPIO.IN)
    GPIO.setup(8, GPIO.IN)

    GPIO.output(7, 1)
    GPIO.output(20, 0)
    GPIO.input(16)
    GPIO.input(12)
    GPIO.input(8)


def led15():
    GPIO.setup(12, GPIO.OUT)
    GPIO.setup(20, GPIO.OUT)
    GPIO.setup(8, GPIO.IN)
    GPIO.setup(16, GPIO.IN)
    GPIO.setup(7, GPIO.IN)

    GPIO.output(12, 1)
    GPIO.output(20, 0)
    GPIO.input(8)
    GPIO.input(16)
    GPIO.input(7)


def led16():
    GPIO.setup(16, GPIO.OUT)
    GPIO.setup(20, GPIO.OUT)
    GPIO.setup(8, GPIO.IN)
    GPIO.setup(12, GPIO.IN)
    GPIO.setup(7, GPIO.IN)

    GPIO.output(16, 1)
    GPIO.output(20, 0)
    GPIO.input(8)
    GPIO.input(12)
    GPIO.input(7)


def ledReset():
    GPIO.setup(16, GPIO.IN)
    GPIO.setup(20, GPIO.IN)
    GPIO.setup(8, GPIO.IN)
    GPIO.setup(12, GPIO.IN)
    GPIO.setup(7, GPIO.IN)

    GPIO.input(16)
    GPIO.input(20)
    GPIO.input(8)
    GPIO.input(12)
    GPIO.input(7)


# Prints the board, used for development
def printBoard():
    for i in range(-1, -9, -1):
        print(boardShow[i])
    print("")


def ledCoord(row, col):
    if row == 1:
        led16()
    elif row == 2:
        led15()
    elif row == 3:
        led14()
    elif row == 4:
        led13()
    elif row == 5:
        led12()
    elif row == 6:
        led11()
    elif row == 7:
        led10()
    elif row == 8:
        led9()
    time.sleep(0.01)

    if col == 1:
        led8()
    elif col == 2:
        led7()
    elif col == 3:
        led6()
    elif col == 4:
        led5()
    elif col == 5:
        led4()
    elif col == 6:
        led3()
    elif col == 7:
        led2()
    elif col == 8:
        led1()

    time.sleep(0.01)


# Used so that the parser understands statement
def numToLetter(coord):
    letters = ["A", "B", "C", "D", "E", "F", "G", "H"]
    return letters[coord]


def letterToNum(coord):
    letters = ["A", "B", "C", "D", "E", "F", "G", "H"]
    return letters.index(coord)


def convertNotation(coord):
    print("Coord: " + coord)
    nums = [0, 0, 8, 7, 6, 5, 4, 3, 2, 1]
    letters = ["H", "G", "F", "E", "D", "C", "B", "A"]

    swapped = letters[letterToNum(coord[0])]
    swapped += str(nums[int(coord[1])])
    swapped += letters[letterToNum(coord[2])]
    swapped += str(nums[int(coord[3])])

    return swapped


def swapNum(coord):
    nums = [7, 6, 5, 4, 3, 2, 1, 0]

    return nums[int(coord)]


# Set column pins as input and pull up
def colSetup():
    for col in colPins:
        GPIO.setup(col, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


# Set row pins as output then set them to False
def rowSetup():
    for row in rowPins:
        GPIO.setup(row, GPIO.OUT)
        GPIO.setup(row, 0)


def makeMove(move, board):
    print("Making move : " + move.notation)
    board.makeMove(move)


def checkBoard():
    for row in rowPins:
        GPIO.output(row, 0)

    legalBoard = False
    while not legalBoard:
        legalBoard = True
        for i in range(8):
            GPIO.output(rowPins[i], 1)
            for j in range(8):
                if boardShow[i][j] != GPIO.input(colPins[j]):
                    legalBoard = False
                    illegalPiece = numToLetter(j)
                    illegalPiece += str(i + 1)
                    # print("Piece is missing on: " + illegalPiece)
                    writeToLCD("Piece is missing on:", illegalPiece, "", "")
                    while True:
                        ledCoord(i + 1, j + 1)
                        if GPIO.input(colPins[j]):
                            ledReset()
                            break

            GPIO.output(rowPins[i], 0)


# Makes sure that all pieces are on the board in the right places
def startSetup():
    for row in rowPins:
        GPIO.output(row, 0)

    rowList = [5, 11, 17, 4]
    legalBoard = False
    while not legalBoard:
        legalBoard = True
        for row in rowList:
            GPIO.output(row, 1)
            for col in colPins:
                if GPIO.input(col) == 0:
                    illegalPiece = numToLetter((colPins.index(col)))
                    illegalPiece += str(rowPins.index(row) + 1)
                    print("Piece is missing on: " + illegalPiece)
                    writeToLCD("Piece is missing on:", illegalPiece, "", "")
                    while True:
                        ledCoord(rowPins.index(row) + 1, colPins.index(col) + 1)
                        if GPIO.input(col):
                            ledReset()
                            break
                    legalBoard = False
            GPIO.output(row, 0)
    writeToLCD("All set up", "", "", "")


# Gets position of move to and from, and returns these values in tuple
# Currently assumes that no mistakes are made and all pieces are already present
def moveInput():
    print("Make move")
    writeToLCD("Make Move", "", "", "")
    moveFrom = False
    moveTo = False
    fromNotation = "False"
    toNotation = "False"
    while not moveFrom and not moveTo:
        for row in rowPins:
            GPIO.output(row, 1)
            for col in colPins:
                if GPIO.input(col) == 0 and boardShow[rowPins.index(row)][colPins.index(col)] == 1:
                    if WHITE and colouredBoard[rowPins.index(row)][colPins.index(col)] == "w":
                        moveFromCol = col
                        moveFromRow = row
                        moveFrom = True
                        printBoard()
                    elif WHITE and colouredBoard[rowPins.index(row)][colPins.index(col)] == "b":
                        moveToCol = col
                        moveToRow = row
                        moveTo = True
                        printBoard()
                    elif not WHITE and colouredBoard[rowPins.index(row)][colPins.index(col)] == "w":
                        moveToCol = col
                        moveToRow = row
                        moveTo = True
                        printBoard()
                    elif not WHITE and colouredBoard[rowPins.index(row)][colPins.index(col)] == "b":
                        moveFromCol = col
                        moveFromRow = row
                        moveFrom = True
                        printBoard()

            GPIO.output(row, 0)

    writeToLCD("Move from:  " + str(moveFrom), "", "Move to:  " + str(moveTo), "")
    print(moveFrom)
    print(moveTo)
    while not moveFrom or not moveTo:
        for row in rowPins:
            GPIO.output(row, 1)
            for col in colPins:
                if GPIO.input(14) or GPIO.input(15) or GPIO.input(21):
                    moveFromCol = 0
                    moveFromRow = 0
                    moveToCol = 0
                    moveToRow = 0
                    moveFrom = True
                    moveTo = True
                if GPIO.input(col) == 0 and boardShow[rowPins.index(row)][colPins.index(col)] == 1:
                    if WHITE and not moveFrom and colouredBoard[rowPins.index(row)][colPins.index(col)] == "w":
                        moveFromCol = col
                        moveFromRow = row
                        moveFrom = True
                        printBoard()
                    elif not WHITE and not moveFrom and colouredBoard[rowPins.index(row)][colPins.index(col)] == "b":
                        moveFromCol = col
                        moveFromRow = row
                        moveFrom = True
                        printBoard()
                    elif not WHITE and not moveTo and colouredBoard[rowPins.index(row)][colPins.index(col)] == "w":
                        moveToCol = col
                        moveToRow = row
                        moveTo = True
                        printBoard()
                    elif WHITE and not moveTo and colouredBoard[rowPins.index(row)][colPins.index(col)] == "b":
                        moveToCol = col
                        moveToRow = row
                        moveTo = True
                        printBoard()
                elif GPIO.input(col) == 1 and boardShow[rowPins.index(row)][colPins.index(col)] == 0:
                    moveToCol = col
                    moveToRow = row
                    moveTo = True
                    printBoard()

            GPIO.output(row, 0)

    writeToLCD("Move from:  " + str(moveFrom), "", "Move to:  " + str(moveTo), "")

    if moveFromCol == moveToRow and moveFromCol == moveToCol:
        return "error", "error", "error", "error"

    print(moveFromCol, moveFromRow, moveToCol, moveToRow)
    return moveFromCol, moveFromRow, moveToCol, moveToRow


# Contains all game logic including ai movement
def startGame(board, playerSide, ai):
    startTime = time.time()
    global colouredBoard, colouredBoardLegal
    global boardShow, boardShowLegal
    parser = InputParser(board, playerSide)
    moves = 0
    while True:
        moves += 1
        # Checks if the game has ended, either checkmate or stalemate
        if board.isCheckmate() or board.isStalemate():
            f = open("/home/pi/Public/command-line-chess-master/src/ChessStats")
            gamesWon = f.readline()
            gamesLost = f.readline()
            totalTime = f.readline()
            totalMoves = f.readline()
            gamesWon = int(gamesWon)
            gamesLost = int(gamesLost)
            totalTime = int(totalTime)
            totalMoves = int(totalMoves)
            f.close()

            f = open("/home/pi/Public/command-line-chess-master/src/ChessStats", "w")

            endTime = time.time()
            timeTaken = (int(endTime - startTime)) // 60
            if board.isCheckmate():

                if board.currentSide == playerSide:
                    print("Checkmate, you lost")
                    writeToLCD("Checkmate, you lost", "Game length: " + str(timeTaken) + " mins",
                               "Moves made: " + str(moves), "")
                    f.write(str(gamesWon) + "\n")
                    f.write(str(gamesLost + 1) + "\n")
                    f.write(str(totalTime + timeTaken) + "\n")
                    f.write(str(totalMoves + moves) + "\n")
                else:
                    print("Checkmate! You won!")
                    writeToLCD("Checkmate! You won!", "Game length: " + str(timeTaken) + " mins",
                               "Moves made: " + str(moves), "")
                    f.write(str(gamesWon + 1) + "\n")
                    f.write(str(gamesLost) + "\n")
                    f.write(str(totalTime + timeTaken) + "\n")
                    f.write(str(totalMoves + moves) + "\n")

            if board.isStalemate():
                print("Stalemate")
                writeToLCD("Stalemate", "Game length: " + str(timeTaken) + " mins", "Moves made: " + str(moves), "")
                f.write(str(gamesWon) + "\n")
                f.write(str(gamesLost) + "\n")
                f.write(str(totalTime + timeTaken) + "\n")
                f.write(str(totalMoves + moves) + "\n")

            f.close()
            return

        # Checks whether it is the users or the computers turn
        if board.currentSide == playerSide:

            # Takes user move
            # writeToLCD("Player's Move", "", "", "")
            # move = None
            moveFromCol, moveFromRow, moveToCol, moveToRow = moveInput()

            try:
                moveFrom1 = numToLetter((colPins.index(moveFromCol)))
                moveFrom2 = str(rowPins.index(moveFromRow) + 1)
                moveTo1 = numToLetter((colPins.index(moveToCol)))
                moveTo2 = str(rowPins.index(moveToRow) + 1)
                command = moveFrom1 + moveFrom2 + moveTo1 + moveTo2

                if not WHITE:
                    command = moveFrom1 + str(int(moveFrom2) + 1) + moveTo1 + str(int(moveTo2) + 1)
                    command = convertNotation(command)

                print(command)

                # Checks if move is valid
                move = parser.parse(command)

                if WHITE:
                    colour = "w"
                else:
                    colour = "b"

                colouredBoard[rowPins.index(moveFromRow)][colPins.index(moveFromCol)] = 0
                boardShow[rowPins.index(moveFromRow)][colPins.index(moveFromCol)] = 0
                colouredBoard[rowPins.index(moveToRow)][colPins.index(moveToCol)] = colour
                boardShow[rowPins.index(moveToRow)][colPins.index(moveToCol)] = 1

                temp = colouredBoard
                colouredBoardLegal = temp
                temp = boardShow
                boardShowLegal = temp

                print("Movement successful: ")  # Then print move made
                writeToLCD("Acceptable movement", "", "", "")
                time.sleep(0.5)
                checkBoard()

            except ValueError as error:
                if moveFromCol == 0 and moveFromRow == 0 and moveToCol == 0 and moveToRow == 0:
                    writeToLCD("Movement cancelled", "", "", "")
                else:
                    writeToLCD("Invalid Move", "", "", "")

                time.sleep(2)
                checkBoard()

                temp = colouredBoardLegal
                colouredBoard = temp
                temp = boardShowLegal
                boardShow = temp
                print("%s" % error)
                print("Invalid move")
                continue

            makeMove(move, board)

        # Decides where the AI moves
        else:
            # writeToLCD("AI thinking...", "", "", "")
            print("AI thinking...")
            writeToLCD("AI Thinking...", "", "", "")
            move = ai.getBestMove()
            print(move)

            # Make it check that piece was moved to the correct place, repeat if it is wrong
            aiMoveFromCol = int(str(move)[11])
            aiMoveFromRow = int(str(move)[14])
            aiMoveToCol = int(str(move)[31])
            aiMoveToRow = int(str(move)[34])
            aiMove = numToLetter(aiMoveFromCol)
            aiMove += str(aiMoveFromRow + 1)
            aiMove += numToLetter(aiMoveToCol)
            aiMove += str(aiMoveToRow + 1)
            writeToLCD("AI move:", aiMove, "", "")
            time.sleep(2)

            print("Move piece from: ", numToLetter(aiMoveFromCol) + str(aiMoveFromRow))
            writeToLCD("Move piece from:", aiMove[0:2], "", "")
            if WHITE:
                while True:
                    GPIO.output(rowPins[aiMoveFromRow], 1)
                    ledCoord(aiMoveFromRow + 1, aiMoveFromCol + 1)
                    if GPIO.input(colPins[aiMoveFromCol]) == 0:
                        print(rowPins[aiMoveFromRow])
                        print(colPins[aiMoveFromCol])
                        GPIO.output(rowPins[aiMoveFromRow], 0)
                        break
            else:
                while True:
                    GPIO.output(rowPins[swapNum(aiMoveFromRow)], 1)
                    ledCoord(swapNum(aiMoveFromRow) + 1, swapNum(aiMoveFromCol) + 1)
                    if GPIO.input(colPins[swapNum(aiMoveFromCol)]) == 0:
                        print(rowPins[aiMoveFromRow])
                        print(colPins[aiMoveFromCol])
                        GPIO.output(rowPins[swapNum(aiMoveFromRow)], 0)
                        break

            if WHITE:
                printBoard()
                print(aiMoveToCol, aiMoveToRow)
                if boardShow[swapNum(aiMoveToCol)][swapNum(aiMoveToRow)] == 1:
                    print("Remove!!!!!!!!!!!!!!!!")
                    print("Remove piece from:", numToLetter(aiMoveToCol) + str(aiMoveToRow))
                    writeToLCD("Reove piece from:", aiMove[2:4], "", "")
                    GPIO.output(rowPins[aiMoveToRow], 1)
                    while True:
                        if GPIO.input(colPins[aiMoveToCol]) == 0:
                            GPIO.output(rowPins[aiMoveToRow], 0)
                            break
                        ledCoord(aiMoveToRow + 1, aiMoveToCol + 1)
            else:
                if boardShow[aiMoveToCol][aiMoveToRow] == 1:
                    print("Remove piece from:", numToLetter(aiMoveToCol) + str(aiMoveToRow))
                    writeToLCD("Reove piece from:", aiMove[2:4], "", "")
                    GPIO.output(rowPins[swapNum(aiMoveToRow)], 1)
                    while True:
                        if GPIO.input(colPins[swapNum(aiMoveToCol)]) == 0:
                            GPIO.output(rowPins[swapNum(aiMoveToRow)], 0)
                            break
                        ledCoord(swapNum(aiMoveToRow) + 1, swapNum(aiMoveToCol) + 1)

            if WHITE:
                print("Move piece to:", numToLetter(aiMoveToCol) + str(aiMoveToRow))
                writeToLCD("Move piece to:", aiMove[2:4], "", "")
                GPIO.output(rowPins[aiMoveToRow], 1)
                while True:
                    ledCoord(aiMoveToRow + 1, aiMoveToCol + 1)
                    if GPIO.input(colPins[aiMoveToCol]) == 1:
                        GPIO.output(rowPins[aiMoveToRow], 0)
                        break
            else:
                print("Move piece to:", numToLetter(aiMoveToCol) + str(aiMoveToRow))
                writeToLCD("Move piece to:", aiMove[2:4], "", "")
                GPIO.output(rowPins[swapNum(aiMoveToRow)], 1)
                while True:
                    ledCoord(swapNum(aiMoveToRow) + 1, swapNum(aiMoveToCol) + 1)
                    if GPIO.input(colPins[swapNum(aiMoveToCol)]) == 1:
                        GPIO.output(rowPins[swapNum(aiMoveToRow)], 0)
                        break

            ledReset()

            if WHITE:
                colouredBoard[aiMoveToRow][aiMoveToCol] = "b"
                colouredBoardLegal[aiMoveToRow][aiMoveToCol] = "b"
            else:
                colouredBoard[swapNum(aiMoveToRow)][swapNum(aiMoveToCol)] = "w"
                colouredBoardLegal[swapNum(aiMoveToRow)][swapNum(aiMoveToCol)] = "w"
                print("Done")
                writeToLCD("Done", "", "", "")

            if WHITE:
                colouredBoard[aiMoveFromRow][aiMoveFromCol] = 0
                colouredBoardLegal[aiMoveFromRow][aiMoveFromCol] = 0
                boardShow[aiMoveFromRow][aiMoveFromCol] = 0
                boardShow[aiMoveToRow][aiMoveToCol] = 1
                temp = boardShow
                boardShowLegal = temp

            elif not WHITE:
                colouredBoard[swapNum(aiMoveFromRow)][swapNum(aiMoveFromCol)] = 0
                colouredBoardLegal[swapNum(aiMoveFromRow)][swapNum(aiMoveFromCol)] = 0
                boardShow[swapNum(aiMoveFromRow)][swapNum(aiMoveFromCol)] = 0
                boardShow[swapNum(aiMoveToRow)][swapNum(aiMoveToCol)] = 1
                temp = boardShow
                boardShowLegal = temp

            move.notation = parser.notationForMove(move)
            makeMove(move, board)
            for i in range(-1, -9, -1):
                print(colouredBoard[i])
                print("")


def opponentLED(coord):
    for row in rowPins:
        GPIO.output(row, 0)
    coord1 = letterToNum(coord[0].upper()) + 1
    coord2 = int(coord[1])
    coord3 = letterToNum(coord[2].upper()) + 1
    coord4 = int(coord[3])

    print(coord1, coord2, coord3, coord4)

    GPIO.output(rowPins[coord1 - 1], 1)
    while True:
        ledCoord(coord2, coord1)
        if GPIO.input(colPins[coord2 - 1]) == 0:
            break
    GPIO.output(rowPins[coord1 - 1], 0)

    GPIO.output(rowPins[coord3 - 1], 1)
    while True:
        ledCoord(coord4, coord3)
        if GPIO.input(colPins[coord4 - 1]) == 1:
            break


def twoPlayerGame(board):
    writeToLCD("Connecting to server...")
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        '/home/pi/Public/command-line-chess-master/src/chessboard-c68165e9de9f.json', scope)
    gc = gspread.authorize(credentials)
    wks = gc.open("chess").sheet1

    startTime = time.time()
    global colouredBoard, colouredBoardLegal
    global boardShow, boardShowLegal
    moves = 0
    lastMove = ""
    commandLower = ""
    while True:
        moves += 1
        # Checks if the game has ended, either checkmate or stalemate
        if board.isCheckmate() or board.isStalemate():
            f = open("/home/pi/Public/command-line-chess-master/src/ChessStats")
            gamesWon = f.readline()
            gamesLost = f.readline()
            totalTime = f.readline()
            totalMoves = f.readline()
            gamesWon = int(gamesWon)
            gamesLost = int(gamesLost)
            totalTime = int(totalTime)
            totalMoves = int(totalMoves)
            f.close()

            f = open("/home/pi/Public/command-line-chess-master/src/ChessStats", "w")

            endTime = time.time()
            timeTaken = (int(endTime - startTime)) // 60
            if board.isCheckmate():

                if board.currentSide == playerSide:
                    print("Checkmate, you lost")
                    writeToLCD("Checkmate, you lost", "Game length: " + str(timeTaken) + " mins",
                               "Moves made: " + str(moves), "")
                    f.write(str(gamesWon) + "\n")
                    f.write(str(gamesLost + 1) + "\n")
                    f.write(str(totalTime + timeTaken) + "\n")
                    f.write(str(totalMoves + moves) + "\n")
                else:
                    print("Checkmate! You won!")
                    writeToLCD("Checkmate! You won!", "GaThis thingme length: " + str(timeTaken) + " mins",
                               "Moves made: " + str(moves), "")
                    f.write(str(gamesWon + 1) + "\n")
                    f.write(str(gamesLost) + "\n")
                    f.write(str(totalTime + timeTaken) + "\n")
                    f.write(str(totalMoves + moves) + "\n")

            if board.isStalemate():
                print("Stalemate")
                writeToLCD("Stalemate", "Game length: " + str(timeTaken) + " mins", "Moves made: " + str(moves), "")
                f.write(str(gamesWon) + "\n")
                f.write(str(gamesLost) + "\n")
                f.write(str(totalTime + timeTaken) + "\n")
                f.write(str(totalMoves + moves) + "\n")

            f.close()
            return

        # Checks whether it is the users or the computers turn
        if board.currentSide == playerSide:
            parser = InputParser(board, playerSide)

            # Takes user move
            # writeToLCD("Player's Move", "", "", "")
            # move = None
            moveFromCol, moveFromRow, moveToCol, moveToRow = moveInput()

            try:
                moveFrom1 = numToLetter((colPins.index(moveFromCol)))
                moveFrom2 = str(rowPins.index(moveFromRow) + 1)
                moveTo1 = numToLetter((colPins.index(moveToCol)))
                moveTo2 = str(rowPins.index(moveToRow) + 1)
                command = moveFrom1 + moveFrom2 + moveTo1 + moveTo2
                lastMove = moveFrom1 + moveFrom2 + moveTo1 + moveTo2

                if not WHITE:
                    command = moveFrom1.upper() + str(int(moveFrom2) + 1) + moveTo1.upper() + str(int(moveTo2) + 1)
                    command = convertNotation(command)
                    lastMove = command

                commandLower = list(command)
                commandLower[0] = commandLower[0].lower()
                commandLower[2] = commandLower[2].lower()
                commandLower = ''.join(commandLower)

                print(command)

                # Checks if move is valid
                move = parser.parse(command)
                wks.update_acell('a2', commandLower)

                if WHITE:
                    colour = "w"
                else:
                    colour = "b"

                colouredBoard[rowPins.index(moveFromRow)][colPins.index(moveFromCol)] = 0
                boardShow[rowPins.index(moveFromRow)][colPins.index(moveFromCol)] = 0
                colouredBoard[rowPins.index(moveToRow)][colPins.index(moveToCol)] = colour
                boardShow[rowPins.index(moveToRow)][colPins.index(moveToCol)] = 1

                temp = colouredBoard
                colouredBoardLegal = temp
                temp = boardShow
                boardShowLegal = temp

                print("Movement successful: ")  # Then print move made
                writeToLCD("Acceptable movement", "", "", "")
                time.sleep(0.5)
                checkBoard()

            except ValueError as error:
                if moveFromCol == 0 and moveFromRow == 0 and moveToCol == 0 and moveToRow == 0:
                    writeToLCD("Movement cancelled", "", "", "")
                else:
                    writeToLCD("Invalid Move", "", "", "")

                time.sleep(2)
                checkBoard()

                temp = colouredBoardLegal
                colouredBoard = temp
                temp = boardShowLegal
                boardShow = temp
                print("%s" % error)
                print("Invalid move")
                continue

            makeMove(move, board)

        # Decides where the AI moves
        else:
            writeToLCD("Opponent turn...")
            while True:
                for i in range(10, 0, -1):
                    time.sleep(1)
                    writeToLCD("Opponent turn...", "", "Checking in: " + str(i))

                move = wks.acell('a2').value
                if move != commandLower:
                    break

            print(move)

            # Make it check that piece was moved to the correct place, repeat if it is wrong
            if playerSide:
                parser = InputParser(board, False)
            else:
                parser = InputParser(board, True)

            aiMoveFromCol = move[0].upper()
            aiMoveFromRow = move[1]
            aiMoveToCol = move[2].upper()
            aiMoveToRow = move[3]
            aiMove = aiMoveFromCol + aiMoveFromRow + aiMoveToCol + aiMoveToRow
            move = parser.parse(aiMove)
            writeToLCD("Opponent move:", aiMove, "", "")
            time.sleep(2)

            print("Move piece from: ", aiMoveFromCol + aiMoveFromRow)
            writeToLCD("Move piece from:", aiMove[0:2], "", "")

            aiMoveFromCol = letterToNum(aiMoveFromCol)
            aiMoveToCol = letterToNum(aiMoveToCol)

            if WHITE:
                while True:
                    GPIO.output(rowPins[int(aiMoveFromRow) - 1], 1)
                    ledCoord(int(aiMoveFromRow), int(aiMoveFromCol) + 1)
                    if GPIO.input(colPins[aiMoveFromCol]) == 0:
                        print(rowPins[int(aiMoveFromRow)])
                        print(colPins[int(aiMoveFromCol)])
                        GPIO.output(rowPins[int(aiMoveFromRow)], 0)
                        break
            else:
                while True:
                    GPIO.output(rowPins[swapNum(int(aiMoveFromRow) - 1)], 1)
                    ledCoord(swapNum(int(aiMoveFromRow) - 2), swapNum(int(aiMoveFromCol)) + 1)
                    if GPIO.input(colPins[swapNum(aiMoveFromCol)]) == 0:
                        print(rowPins[int(aiMoveFromRow)])
                        print(colPins[int(aiMoveFromCol)])
                        GPIO.output(rowPins[swapNum(int(aiMoveFromRow))], 0)
                        break

            if WHITE:
                printBoard()
                if boardShow[swapNum(aiMoveToCol)][swapNum(int(aiMoveToRow) - 1)] == 1:
                    print("Remove piece from:", numToLetter(aiMoveToCol) + str(aiMoveToRow))
                    writeToLCD("Remove piece from:", aiMove[2:4])
                    GPIO.output(rowPins[int(aiMoveToRow) - 1], 1)
                    while True:
                        if GPIO.input(colPins[aiMoveToCol]) == 0:
                            GPIO.output(rowPins[int(aiMoveToRow)], 0)
                            break
                        ledCoord(int(aiMoveToRow), aiMoveToCol + 1)
            else:
                print("This thing", aiMoveToCol, aiMoveToRow)
                if boardShow[aiMoveToCol][int(aiMoveToRow) - 1] == 1:
                    print("Remove piece from:", numToLetter(aiMoveToCol) + str(aiMoveToRow))
                    writeToLCD("Reove piece from:", aiMove[2:4])
                    GPIO.output(rowPins[swapNum(aiMoveToRow) + 1], 1)
                    while True:
                        if GPIO.input(colPins[swapNum(aiMoveToCol)]) == 0:
                            GPIO.output(rowPins[swapNum(aiMoveToRow)], 0)
                            break
                        ledCoord(swapNum(aiMoveToRow) + 2, swapNum(aiMoveToCol) + 1)

            if WHITE:
                print("Move piece to:", numToLetter(aiMoveToCol) + str(aiMoveToRow))
                writeToLCD("Move piece to:", aiMove[2:4], "", "")
                GPIO.output(rowPins[int(aiMoveToRow) - 1], 1)
                while True:
                    ledCoord(int(aiMoveToRow), aiMoveToCol + 1)
                    if GPIO.input(colPins[aiMoveToCol]) == 1:
                        GPIO.output(rowPins[int(aiMoveToRow)], 0)
                        break
            else:
                print("Move piece to:", numToLetter(aiMoveToCol) + str(aiMoveToRow))
                writeToLCD("Move piece to:", aiMove[2:4], "", "")
                print("#### col pin:", colPins[swapNum(aiMoveToCol)])
                print("#### row pin:", rowPins[swapNum(aiMoveToRow) + 1])
                GPIO.output(rowPins[swapNum(aiMoveToRow) + 1], 1)
                while True:
                    ledCoord(swapNum(aiMoveToRow) + 2, swapNum(aiMoveToCol) + 1)
                    if GPIO.input(colPins[swapNum(aiMoveToCol)]) == 1:
                        GPIO.output(rowPins[swapNum(aiMoveToRow)], 0)
                        break

            ledReset()

            if WHITE:
                colouredBoard[int(aiMoveToRow) - 1][aiMoveToCol] = "b"
                colouredBoardLegal[int(aiMoveToRow)][aiMoveToCol] = "b"
            else:
                colouredBoard[swapNum(int(aiMoveToRow) - 1)][swapNum(aiMoveToCol)] = "w"
                colouredBoardLegal[swapNum(aiMoveToRow)][swapNum(aiMoveToCol)] = "w"
                print("Done")
                writeToLCD("Done", "", "", "")

            if WHITE:
                colouredBoard[int(aiMoveFromRow) - 1][aiMoveFromCol] = 0
                colouredBoardLegal[int(aiMoveFromRow) - 1][aiMoveFromCol] = 0
                boardShow[int(aiMoveFromRow) - 1][aiMoveFromCol] = 0
                boardShow[int(aiMoveToRow) - 1][aiMoveToCol] = 1
                temp = boardShow
                boardShowLegal = temp

            elif not WHITE:
                print(swapNum(aiMoveFromRow), swapNum(aiMoveFromCol))
                colouredBoard[swapNum(int(aiMoveFromRow) - 1)][swapNum(aiMoveFromCol)] = 0
                colouredBoardLegal[swapNum(aiMoveFromRow) - 1][swapNum(aiMoveFromCol)] = 0
                boardShow[swapNum(int(aiMoveFromRow) - 1)][swapNum(aiMoveFromCol)] = 0
                boardShow[swapNum(aiMoveToRow) + 1][swapNum(aiMoveToCol)] = 1
                temp = boardShow
                boardShowLegal = temp

            move.notation = parser.notationForMove(move)
            makeMove(move, board)
            for i in range(-1, -9, -1):
                print(colouredBoard[i])
                print("")

            printBoard()


# Clears screen then writes up to four lines
def writeToLCD(text1="", text2="", text3="", text4=""):
    draw.rectangle((0, 0, width, height), outline=0, fill=0)
    disp.clear()
    disp.display()
    draw.text((x, top), text1, font=font, fill=255)
    draw.text((x, top + 8), text2, font=font, fill=255)
    draw.text((x, top + 16), text3, font=font, fill=255)
    draw.text((x, top + 24), text4, font=font, fill=255)
    disp.image(image1)
    disp.display()


# First thing that happens when board loads
###### 14 up, 15 enter, 21 down
def homeMenu():
    wait = 0.5

    menu = [["> New Game", "  Statistics"], ["  New Game", "> Statistics"]]
    menuNum = 0
    writeToLCD(menu[0][0], menu[0][1], "", "")

    while True:
        if GPIO.input(15):
            break

        elif GPIO.input(14) or GPIO.input(21):
            if menuNum == 0:
                menuNum = 1
                writeToLCD(menu[menuNum][0], menu[menuNum][1], "", "")
                time.sleep(wait)
            else:
                menuNum = 0
                writeToLCD(menu[menuNum][0], menu[menuNum][1], "", "")
                time.sleep(wait)

    if menuNum == 0:
        menu = [["> Single Player", "  Multiplayer"], ["  Single Player", "> Multiplayer"]]
        menuNum = 0
        writeToLCD(menu[menuNum][0], menu[menuNum][1], "", "")
        time.sleep(wait)

        while True:
            if GPIO.input(15):
                if menuNum == 0:
                    mode = "s"
                else:
                    mode = "m"
                break

            elif GPIO.input(14) or GPIO.input(21):
                if menuNum == 0:
                    menuNum = 1
                    writeToLCD(menu[menuNum][0], menu[menuNum][1], "", "")
                    time.sleep(wait)
                else:
                    menuNum = 0
                    writeToLCD(menu[menuNum][0], menu[menuNum][1], "", "")
                    time.sleep(wait)

        menu = [["Pick side:", "> White", "  Black"], ["Pick side:", "  White", "> Black"]]
        menuNum = 0
        writeToLCD(menu[menuNum][0], menu[menuNum][1], menu[menuNum][2], "")
        time.sleep(wait)

        while True:
            if GPIO.input(15):
                if menuNum == 0:
                    colour = "w"
                else:
                    colour = "b"
                break

            elif GPIO.input(14) or GPIO.input(21):
                if menuNum == 0:
                    menuNum = 1
                    writeToLCD(menu[menuNum][0], menu[menuNum][1], menu[menuNum][2], "")
                    time.sleep(wait)
                else:
                    menuNum = 0
                    writeToLCD(menu[menuNum][0], menu[menuNum][1], menu[menuNum][2], "")
                    time.sleep(wait)

        level = 2
        writeToLCD("Difficulty", "^", str(level), "v")
        time.sleep(wait)

        while True:
            if GPIO.input(14):
                level += 1
                writeToLCD("Difficulty", "^", str(level), "v")
                time.sleep(wait)
            elif GPIO.input(15):
                break
            elif GPIO.input(21):
                level -= 1
                writeToLCD("Difficulty", "^", str(level), "v")
                time.sleep(wait)

        return mode, colour, level

    elif menuNum == 1:
        f = open("/home/pi/Public/command-line-chess-master/src/ChessStats")
        gamesWon = f.readline()
        gamesLost = f.readline()
        averageTime = f.readline()
        averageMoves = f.readline()
        f.close()

        print(gamesWon, gamesLost, averageTime, averageMoves)
        writeToLCD("Games won: " + gamesWon, "Games lost: " + gamesLost,
                   "Avg time: " + str(int(averageTime) // (int(gamesWon) + int(gamesLost))) + " mins",
                   "Average moves: " + str(int(averageMoves) // (int(gamesWon) + int(gamesLost))))
        time.sleep(wait)
        while True:
            if GPIO.input(15):
                return 0, 0, 0
                break


# Sets up board to be played on
colSetup()
rowSetup()

# Makes sure all pieces are in the right place
startSetup()
time.sleep(0.2)
startSetup()
time.sleep(0.2)

mode, colour, level = homeMenu()
print(colour)

checkBoard()

if colour == "w":
    WHITE = True
    BLACK = False
    colouredBoard = [["w", "w", "w", "w", "w", "w", "w", "w"], ["w", "w", "w", "w", "w", "w", "w", "w"],
                     [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0], ["b", "b", "b", "b", "b", "b", "b", "b"],
                     ["b", "b", "b", "b", "b", "b", "b", "b"]]
    colouredBoardLegal = [["w", "w", "w", "w", "w", "w", "w", "w"], ["w", "w", "w", "w", "w", "w", "w", "w"],
                          [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0, 0], ["b", "b", "b", "b", "b", "b", "b", "b"],
                          ["b", "b", "b", "b", "b", "b", "b", "b"]]
else:
    WHITE = False
    BLACK = True
    colouredBoard = [["b", "b", "b", "b", "b", "b", "b", "b"], ["b", "b", "b", "b", "b", "b", "b", "b"],
                     [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0], ["w", "w", "w", "w", "w", "w", "w", "w"],
                     ["w", "w", "w", "w", "w", "w", "w", "w"]]
    colouredBoardLegal = [["b", "b", "b", "b", "b", "b", "b", "b"], ["b", "b", "b", "b", "b", "b", "b", "b"],
                          [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0, 0], ["w", "w", "w", "w", "w", "w", "w", "w"],
                          ["w", "w", "w", "w", "w", "w", "w", "w"]]

playerSide = WHITE

aiDepth = level
# Starts game logic, continues until game end
board = Board()
opponentAI = AI(board, not playerSide, aiDepth)

# Starts either one or two player game
if mode == "s":
    startGame(board, playerSide, opponentAI)
elif mode == "m":
    twoPlayerGame(board)
