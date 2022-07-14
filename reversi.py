# Reversi
# projeto para a cadeira de Inteligência Artificial
# Recebemos o codigo reversi.py (jogo Othello) com o objetivo de implementar uma IA.
#Dupla: Alerandro Lourenço e Claudio Lopes- UFMA
#foi implementado getPosicao, uma função Heuristica getHeurisitica e minimax, dessa forma, IA sempre tem como objetivo captura os cantos...
# Onde fica a maior pontuação devivo a função heuristica.
from json.encoder import INFINITY
import random
import sys

def drawBoard(board):
	# Essa funcao desenha o tabuleiro
	HLINE = '  +---+---+---+---+---+---+---+---+'
	VLINE = '  |   |   |   |   |   |   |   |   |'

	print('    1   2   3   4   5   6   7   8')
	print(HLINE)

	for y in range(8):
		print(VLINE)
		print(y+1, end=' ')
		for x in range(8):
			print('| %s' % (board[x][y]), end=' ')
		print('|')
		print(VLINE)
		print(HLINE)

def resetBoard(board):
	#Essa funcao esvazia o tabuleiro
	for x in range(8):
		for y in range(8):
			board[x][y] = ' '
	# Pecas iniciais:
	board[3][3] = 'X'
	board[3][4] = 'O'
	board[4][3] = 'O'
	board[4][4] = 'X'

def getNewBoard():
	# Criar um tabuleiro novo
	board = []
	for i in range(8):
		board.append([' '] * 8)
	return board

def isValidMove(board, tile, xstart, ystart):
	# Retorna False se o movimento em xstart, ystart é invalido
	# Se o movimento é valido, retorna uma lista de casas que devem ser viradas após o movimento
	if board[xstart][ystart] != ' ' or not isOnBoard(xstart, ystart):
		return False
	board[xstart][ystart] = tile 
	if tile == 'X':
		otherTile = 'O'
	else:
		otherTile = 'X'
	tilesToFlip = []
	for xdirection, ydirection in [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]:
		x, y = xstart, ystart
		x += xdirection # first step in the direction
		y += ydirection # first step in the direction
		if isOnBoard(x, y) and board[x][y] == otherTile:
			x += xdirection
			y += ydirection
			if not isOnBoard(x, y):
				continue
			while board[x][y] == otherTile:
				x += xdirection
				y += ydirection
				if not isOnBoard(x, y):
					break
			if not isOnBoard(x, y):
				continue
			if board[x][y] == tile:
				while True:
					x -= xdirection
					y -= ydirection
					if x == xstart and y == ystart:
						break
					tilesToFlip.append([x, y])
	board[xstart][ystart] = ' '
	if len(tilesToFlip) == 0:
		return False
	return tilesToFlip
 
def isOnBoard(x, y):
	# Retorna True se a casa está no tabuleiro.
	return x >= 0 and x <= 7 and y >= 0 and y <=7

def getBoardWithValidMoves(board, tile):
	# Retorna um tabuleiro com os movimentos validos
	dupeBoard = getBoardCopy(board)
	for x, y in getValidMoves(dupeBoard, tile):
		dupeBoard[x][y] = '.'
	return dupeBoard

def getValidMoves(board, tile):
	# Retorna uma lista de movimentos validos
	validMoves = []
	for x in range(8):
		for y in range(8):
			if isValidMove(board, tile, x, y) != False:
				validMoves.append([x, y])
	return validMoves

def getScoreOfBoard(board):
	# Determina o score baseado na contagem de 'X' e 'O'.
	xscore = 0
	oscore = 0
	for x in range(8):
		for y in range(8):
			if board[x][y] == 'X':
				xscore += 1
			if board[x][y] == 'O':
				oscore += 1
	return {'X':xscore, 'O':oscore}

def enterPlayerTile():
	# Permite que o player escolha ser X ou O
	tile = ''
	while not (tile == 'X' or tile == 'O'):
		print('Escolha suas peças: X ou O?')
		tile = input().upper()
	if tile == 'X':
		return ['X', 'O']
	else:
	  return ['O', 'X']

def whoGoesFirst():
	# Escolhe aleatóriamente quem começa.
	if random.randint(0, 1) == 0:
		return 'computer'
	else:
		return 'player'

def playAgain():
	# Retorna True se o player quer jogar novamente
	print('Quer jogar novamente? (yes ou no)')
	return input().lower().startswith('y')

def makeMove(board, tile, xstart, ystart):
	# Coloca a peça no tabuleiro em xstart, ystart, e as peças do oponente
	# Retorna False se for um movimento invalido
	tilesToFlip = isValidMove(board, tile, xstart, ystart)
	if tilesToFlip == False:
		return False
	board[xstart][ystart] = tile
	for x, y in tilesToFlip:
		board[x][y] = tile
	return True

def getBoardCopy(board):
	# Faz uma cópia do tabuleiro e retorna a cópia
	dupeBoard = getNewBoard()
	for x in range(8):
		for y in range(8):
			dupeBoard[x][y] = board[x][y]
	return dupeBoard

def isOnCorner(x, y):
	# Retorna True se a posição x, y é um dos cantos do tabuleiro
	return (x == 0 and y == 0) or (x == 7 and y == 0) or (x == 0 and y == 7) or (x == 7 and y == 7)

def getPlayerMove(board, playerTile):
	# Permite que o player insira sua jogada
	DIGITS1TO8 = '1 2 3 4 5 6 7 8'.split()
	while True:
		print('Insira seu movimento, ou insira quit para sair do jogo, ou hints para ativar/desativar dicas.')
		move = input().lower()
		if move == 'quit':
			return 'quit'
		
		if move == 'hints':
			return 'hints'
		
		if len(move) == 2 and move[0] in DIGITS1TO8 and move[1] in DIGITS1TO8:
			x = int(move[0]) - 1
			y = int(move[1]) - 1
			if isValidMove(board, playerTile, x, y) == False:
				print('Essa não é uma jogada válida')
				continue
			else:
				break
		else: 
			print('Essa não é uma jogada válida, digite o valor de x (1-8), depois o valor de y (1-8).')
			print('Por exemplo, 81 será o canto superior direito.')
			
	return [x, y]

def getPosicao(board, playerTitle): # pecorrere a matriz e guardar elementos na lista
	lista_posicoes = []
	for y in range(8):
		for x in range(8):
			peca = board[y][x]
			if peca == playerTitle:
				lista_posicoes.append([x,y])
	return lista_posicoes


def getHeuristica(board, PlayerTitle):
	score = 0
	lookup = [
        [16.16,  -3.03,	 0.99, 0.43,  	0.43,   0.99,  -3.03,  16.16	],
        [-4.12,  -1.81, -0.08, 0.27,  -0.27,  	-0.08,  -1.81, -4.12	],
        [1.33,  -0.04,   0.51,  0.07,   0.07,   0.51,  -0.04, 1.33		],
        [0.63,   -0.18, -0.04, -0.01, -0.01, 	-0.04, -0.18, 0.63		],
        [0.63,   -0.18, -0.04, -0.01, -0.01, 	-0.04, -0.18, 0.63 		],
        [1.33,  -0.04,   0.51,  0.07,  0.07,   	0.51,  -0.04,1.33		],
        [-4.12,  -1.81, -0.08, 0.27,  -0.27,  	-0.08,  -1.81, -4.12	],
		[16.16,  -3.03, 0.99, 0.43,  0.43,   	0.99,  -3.03,  16.16	]
	]
	
	for peca in getPosicao(board, PlayerTitle): #adicionando a pontuação das peças que estao no board
		x = peca[0]
		y = peca[1]
		score += lookup[y][x]					 
	return score        
        
        
        
def miniMax(players, board, depth, isMaximizing, alpha = float("-inf"), beta = float("inf")):
	if depth == 0:   
		return getHeuristica(board, players[0]) - getHeuristica(board, players[1])
	
	if isMaximizing:
    	#Bot Ganhou
		if getValidMoves(mainBoard, playerTile) == []: # verifica se ainda tem jogadas
			return 10000

		maxEval = float("-inf")
		crrPlayer = players[0]

		for pos in getValidMoves(board, crrPlayer):
			copyBoard = getBoardCopy(board)
			makeMove(copyBoard, crrPlayer, pos[0], pos[1])

			eval = miniMax(players, copyBoard, depth - 1, False, alpha, beta)
			maxEval = max(maxEval, eval)

			alpha = max(eval, alpha)
			if (beta <= alpha): #proning alpha beta
				break
		
		return maxEval
	else:
		#Adversario Ganhou
		if getValidMoves(mainBoard, playerTile) == []:
			return -10000

		minEval = float("inf")
		crrPlayer = players[1]

		for pos in getValidMoves(board, crrPlayer):
			copyBoard = getBoardCopy(board)
			makeMove(copyBoard, crrPlayer, pos[0], pos[1])

			eval = miniMax(players, copyBoard, depth - 1, True, alpha, beta)
			minEval = min(minEval, eval)

			beta = min(eval, beta)
			if (beta <= alpha):  #proning alpha beta
				break
			
		return minEval


def getComputerMove(board, computerTile, playerTile):
	# Permite ao computador executar seu movimento
	possibleMoves = getValidMoves(board, computerTile)
	# randomiza a ordem dos possíveis movimentos
	random.shuffle(possibleMoves)
	# se for possivel, joga no canto
	for x, y in possibleMoves:
		if isOnCorner(x, y):
			return [x, y]
	# Escolhe a jogada que resulta em mais pontos
	bestScore = -1
	for x, y in possibleMoves:
		dupeBoard = getBoardCopy(board)
		makeMove(dupeBoard, computerTile, x, y)
		score = miniMax([computerTile, playerTile], dupeBoard, 4, False)
		if score > bestScore:
			bestMove = [x, y]
			bestScore = score
	return bestMove

def showPoints(playerTile, computerTile):
	# Mostra o score atual
	scores = getScoreOfBoard(mainBoard)
	print('Player1: %s ponto(s). \nComputador: %s ponto(s).' % (scores[playerTile], scores[computerTile]))

print('Welcome to Reversi!')
while True:
	# Reseta o jogo e o tabuleiro
	mainBoard = getNewBoard()
	resetBoard(mainBoard)
	playerTile, computerTile = enterPlayerTile()
	showHints = False
	turn = whoGoesFirst()
	print('O ' + turn + ' começa o jogo.')
	while True:
		if turn == 'player':
			# Player's turn.
			if showHints:
				validMovesBoard = getBoardWithValidMoves(mainBoard, playerTile)
				drawBoard(validMovesBoard)
			else:
				drawBoard(mainBoard)
			showPoints(playerTile, computerTile)
			move = getPlayerMove(mainBoard, playerTile)
			if move == 'quit':
				print('Obrigado por jogar!')
				sys.exit() # terminate the program
			elif move == 'hints':
				showHints = not showHints
				continue
			else:
				makeMove(mainBoard, playerTile, move[0], move[1])
			if getValidMoves(mainBoard, computerTile) == []:
				break
			else:
				turn = 'computer'
		else:
			# Computer's turn.
			drawBoard(mainBoard)
			showPoints(playerTile, computerTile)
			input('Pressione Enter para ver a jogada do computador.')
			x, y = getComputerMove(mainBoard, computerTile, playerTile)
			makeMove(mainBoard, computerTile, x, y)
			if getValidMoves(mainBoard, playerTile) == []:
				break
			else:
				turn = 'player'
	# Mostra o resultado final.
	drawBoard(mainBoard)
	scores = getScoreOfBoard(mainBoard)
	print('X: %s ponto(s) \nO: %s ponto(s).' % (scores['X'], scores['O']))
	if scores[playerTile] > scores[computerTile]:
		print('Você venceu o computador por %s ponto(s)! \nParabéns!' % (scores[playerTile] - scores[computerTile]))
	elif scores[playerTile] < scores[computerTile]:
		print('Você perdeu!\nO computador venceu você por %s ponto(s).' % (scores[computerTile] - scores[playerTile]))
	else:
		print('Empate!')
	if not playAgain():
		break