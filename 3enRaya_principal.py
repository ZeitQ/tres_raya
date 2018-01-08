# 3 en raya

import random
import Back_Propagation_prueba as bp

def drawBoard(board):
    # Esta funcion implica el "board" que se pasò
    # "board" es una lista de 10 cadenas que representan el tablero (ignorar el índice 0)
    print('   |   |')
    print(' ' + board[1] + ' | ' + board[2] + ' | ' + board[3])
    print('   |   |')
    print('-----------')
    print('   |   |')
    print(' ' + board[4] + ' | ' + board[5] + ' | ' + board[6])
    print('   |   |')
    print('-----------')
    print('   |   |')
    print(' ' + board[7] + ' | ' + board[8] + ' | ' + board[9])
    print('   |   |')

def inputPlayerLetter():
    # Dejemos que el jugador escriba qué letra quiere que sea.
    # Devuelve una lista con la letra del jugador como primer elemento y el
    # La carta de la computadora como la segunda.
    letter = ''
    while not (letter == 'X' or letter == 'O'):
        print('¿Quieres ser X o O?')
        letter = input().upper()

    # el primer elemento en la tupla es la letra del jugador, el segundo es la letra de la computadora.
    if letter == 'X':
        return ['X', 'O']
    else:
        return ['O', 'X']
    print('Player = ',letter)
    #return ['1', '-1']

def whoGoesFirst():
    # Elige al azar al jugador que va primero.
    if random.randint(0,1) == 0:
        return 'computer'
    else:
        return 'player'

def playAgain():
    # Esta función devuelve True si el jugador quiere volver a jugar, de lo contrario, devuelve False.
    print('¿Quieres jugar de nuevo? Si(y) o No(n)')
    return input().lower().startswith('y')

def makeMove(board, letter, move):
    board[move] = letter

def isWinner(bo, le):
    # Dado un tablero y la letra de un jugador, esta función
    # devuelve Verdadero si ese jugador ha ganado. Utilizamos
    # bo en lugar de board y le en lugar de letter
    return ((bo[7] == le and bo[8] == le and bo[9] == le) or # por arriba
    (bo[4] == le and bo[5] == le and bo[6] == le) or # en el medio
    (bo[1] == le and bo[2] == le and bo[3] == le) or # abajo
    (bo[7] == le and bo[4] == le and bo[1] == le) or # a la izquierda
    (bo[8] == le and bo[5] == le and bo[2] == le) or # down the middle
    (bo[9] == le and bo[6] == le and bo[3] == le) or # por la mitad
    (bo[7] == le and bo[5] == le and bo[3] == le) or # diagonal
    (bo[9] == le and bo[5] == le and bo[1] == le)) # diagonal

def getBoardCopyForNN(board, computerLetter):
    # Se hace un duplicado de la lista de la junta y devuelve el duplicado.
    dupeBoard = []
    for i in range(0,1):
        pares=[]
        valores=[]
        for j in board:
            if computerLetter == 'X':
                if j == ' ':
                    val = 0
                elif j == 'X':
                    val = -1
                elif j == 'O':
                    val = 1
            else:
                if j == ' ':
                    val = 0
                elif j == 'X':
                    val = 1
                elif j == 'O':
                    val = -1
            valores.append(val)

        pares.append(valores)
        dupeBoard.append(pares)

    dupeBoard[0][0].remove(0)
    return dupeBoard

def getBoardCopy(board):
    # Se hace un duplicado de la lista de la junta y devuelve el duplicado.
    dupeBoard = []

    for i in board:
        dupeBoard.append(i)

    return dupeBoard

def isSpaceFree(board, move):
    # Devuelve true si el movimiento pasado esta libre en el tablero.
    return board[move] == ' '

def getPlayerMove(board):
    # Let the player type in his move.
    move = ' '
    while move not in '1 2 3 4 5 6 7 8 9'.split() or not isSpaceFree(board, int(move)):
        print('¿Cuàl es tu proximo movimiento? (1-9)')
        move = input()
    return int(move)

def chooseRandomMoveFromList(board, movesList):
    # Devuelve un movimiento válido de la lista aprobada en el tablero pasado.
    # Devuelve None si no hay un movimiento válido.
    possibleMoves = []
    for i in movesList:
        if isSpaceFree(board, i):
            possibleMoves.append(i)

    if len(possibleMoves) != 0:
        return random.choice(possibleMoves)
    else:
        return None

def getComputerMove(board, computerLetter, n):
    # Dado un tablero y la carta de la computadora, determina dónde moverse y devuelve ese movimiento.
    if computerLetter == 'X':
        playerLetter = 'O'
    else:
        playerLetter = 'X'


    copyNN = getBoardCopyForNN(board,computerLetter)
    copy = getBoardCopy(board)
    possible_moves = bp.BPTest(n, copyNN)
    for i in range(0,len(possible_moves[0]),1):
        min_val = min(possible_moves[0])
        index = possible_moves[0].index(min_val) + 1
        if isSpaceFree(copy, index):
            return index
        else:
            possible_moves[0][index-1] = 1000

def isBoardFull(board):
    # Devuelve True si se ha tomado cada espacio en el tablero. De lo contrario, devuelve False.
    for i in range(1, 10):
        if isSpaceFree(board, i):
            return False
    return True


print('Bienvenido a Tres en Raya :D')

first = True

while True:
    if(first):
        tam_in = 9#int(input("Ingrese la cantidad de entradas de cada par: "))
        #print tam_in
        tam_out = 9#int(input("Ingrese la cantidad de salidas de cada par: "))
        #print tam_out
        n, pat = bp.BP(tam_in, tam_out)
        bp.BPTrain(n, pat)
    
    # Reset the board
    theBoard = [' '] * 10
    playerLetter, computerLetter = inputPlayerLetter()
    turn = whoGoesFirst()
    print('El ' + turn + ' irà primero.')
    gameIsPlaying = True

    while gameIsPlaying:
        if turn == 'player':
            # Turno del jugador.
            drawBoard(theBoard)
            move = getPlayerMove(theBoard)
            makeMove(theBoard, playerLetter, move)

            if isWinner(theBoard, playerLetter):
                drawBoard(theBoard)
                print('Felicidades! Has ganado el juego!')
                gameIsPlaying = False
            else:
                if isBoardFull(theBoard):
                    drawBoard(theBoard)
                    print('Haz empatado el juego!')
                    break
                else:
                    turn = 'computer'

        else:
            # Turno de la computadora.
            move = getComputerMove(theBoard, computerLetter, n)
            makeMove(theBoard, computerLetter, move)

            if isWinner(theBoard, computerLetter):
                drawBoard(theBoard)
                print('La computadora te ha vencido! Perdiste.')
                gameIsPlaying = False
            else:
                if isBoardFull(theBoard):
                    drawBoard(theBoard)
                    print('Haz empatado el juego!')
                    break
                else:
                    turn = 'player'

    if not playAgain():
        break
    else:
        first = False
