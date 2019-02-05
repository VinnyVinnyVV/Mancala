
import random
import pandas as pd
from tqdm import tqdm

def make_board():
	size = 6
	return pd.DataFrame(4, index=range(0, size), columns=['Player A', 'Player B'])


def print_board(board, home):
	size = len(board)
	for player in ['Player B', 'Player A']:
		if player == 'Player B':
			print('\n%s score is [%s]' % (player, home.loc[player, 'Scores']))
		x = 1
		for i in board.index:
			end = ' | '
			if x == size:
				if player == 'Player B':
					end = ' \n'
					# if i != 1:
					end += '---------------------\n'
				elif player == 'Player A':
					end = ' '

			char = board.loc[i, player]
			if player == 'Player A':
				char = board.loc[size - 1 - i, player]
			# if i in ('X', 'O'):
			# 	char = i
			x += 1
			print(char, end=end)
		if player == 'Player A':
			print('\n%s score is [%s]\n' % (player, home.loc[player, 'Scores']))
		# print(player, ' score: ', home[player])


def starting_position():
	roles = ('Player A', 'Player B')
	if random.randint(0, 1) == 0:
		return roles[::-1]
	return roles


def can_move(brd, player, move):
	if move in brd.index and brd.loc[move, player] > 0:
		return True
	return False


def turn_cycle(board, move, count, player, home):
	size = len(board)
	other_player = board.columns.values[board.columns.values != player][0]
	increased_cells = []
	if move > 0:
		increased_cells = list(range(max(0, move - count), move))
		board.loc[board.index.isin(increased_cells), player] += 1  # Check this
		count = count - move
	if count < 1:  # If it doesn't make it to home
		if (board.loc[min(increased_cells), player] == 1) and (
				board.loc[size - 1 - min(increased_cells), other_player] > 0):
			home.loc[player, 'Scores'] += board.loc[size - 1 - min(increased_cells), other_player] + 1
			board.loc[min(increased_cells), player] = 0
			board.loc[size - 1 - min(increased_cells), other_player] = 0
		return True
	elif count == 1:  # If it lands on home and gets another turn
		home.loc[player, 'Scores'] += 1
		if game_still_going(board):
			return 'Move Again'
			# if player == 'Player A':
			# 	print_board()
			# 	print('Move again!')
			# 	new_move = user_move()
			# 	return make_move(board, player, new_move)
			# else:  # player == 'Player B'
			# 	print_board()
			# 	print('Computer moves again')
			# 	return computer_move()
		else:
			return True
	else:  # count > 1 # If it passes home
		home.loc[player, 'Scores'] += 1
		count -= 1
		if count > size:  # If it makes it all the way around
			board[other_player] += 1
			count -= size
			return turn_cycle(board, size-1, count, player, home)
		else:
			for i in range(0, count):
				board.loc[size - 1 - i, other_player] += 1
			return True


def make_move(board, player, move, home):
	if can_move(board, player, move):
		count = board.loc[move, player]
		board.loc[move, player] = 0
		return turn_cycle(board, move, count, player, home)
		# return True
	return 'Invalid'


def user_move():
	print('# Make your move ! [1-6] : ', end='')
	return int(input()) - 1


def repeatable_moves(board, player):
	repeat_moves = []
	for i in board[player].index:
		if board.loc[i, player] == (i + 1):
			repeat_moves.append(i)
	# print('repeatable indicies are : %s' % repeat_moves)
	return repeat_moves


def clearance_moves(board, player):
	size = len(board)
	other_player = board.columns.values[board.columns.values != player][0]
	clear_moves = []
	for i in board[player].index:
		count = board.loc[i, player]
		if count > 0 and (
				i-count >= 0) and (
				board.loc[i - count, player] == 0) and (
				board.loc[(size - i), other_player] > 0):
			clear_moves.append(i)
	# print('clearance indicies are : %s' % clear_moves)
	return clear_moves


# AI goes here
def computer_move(board, computer, home, comptype='random'):
	available_moves = board[board[computer] > 0].index
	repeat_moves = repeatable_moves(board, computer)
	clear_moves = clearance_moves(board, computer)
	# print(repeat_moves)
	if comptype == 'random':
		move = random.choice(available_moves)
	elif comptype == 'repeat_clearance':
		if len(repeat_moves) > 0:
			move = min(repeat_moves)
		elif len(clear_moves) > 0:
			move = random.choice(clear_moves)
		else:
			move = random.choice(available_moves)
	elif comptype == 'clearance_priority':
		if len(clear_moves) > 0:
			move = random.choice(clear_moves)
		elif len(repeat_moves) > 0:
			move = min(repeat_moves)
		else:
			move = random.choice(available_moves)
	else:
		move = random.choice(available_moves)

	return move


def game_still_going(board):
	# print(board)
	# return (len(board[board[computer] > 0]) > 0) and (len(board[board[player] > 0]) > 0)
	# print(board.iloc[:, 0])
	return (len(board[board.iloc[:, 0] > 0]) > 0) and (len(board[board.iloc[:, 1] > 0]) > 0)


def calculate_score(board, home, prnt=False):
	for player in board.columns.values:
		home.loc[player, 'Scores'] += sum(board.loc[:, player])
	# result = home['Scores'].values
	if prnt:
		print_board(board, home)
		if max(home['Scores']) == min(home['Scores']):
			print('Tie Game: %s to %s' % (max(home['Scores']), min(home['Scores'])))
		else:
			winner = home['Scores'].idxmax()
			print('%s wins! [%s] to [%s]' % (winner, max(home['Scores']), min(home['Scores'])))
	return home['Scores']


def play_game():
	player, computer = starting_position()
	home = pd.DataFrame(0, index=[player, computer], columns=['Scores'])
	print('Player is %s and computer is %s' % (player, computer))
	turn = 'Player A'
	board = make_board()

	while game_still_going(board):
		# print("active")
		print_board(board, home)
		if turn == player:
			move = user_move()
			moved = make_move(board, player, move, home)
			if moved == "Invalid":
				print(' >> Invalid number ! Try again !')
				continue
			if moved == "Move Again":
				print('Move Again!')
				continue
			turn = computer
		else:
			move = computer_move(board, computer, home)
			print('%s moves: %s' % (computer, move + 1))
			moved = make_move(board, computer, move, home)
			if moved == "Move Again":
				print('Move Again!')
				continue
			turn = player
	print("game over")
	player, computer = calculate_score(board, home, prnt=True).values
	print(player, computer)


def play_simulation(comptype1='random', comptype2='random'):
	computer1, computer2 = starting_position()
	home = pd.DataFrame(0, index=[computer1, computer2], columns=['Scores'])

	# print('Comp1 is %s and Comp2 is %s' % (computer1, computer2))
	turn = 'Player A'
	board = make_board()
	# print_board(board)
	while game_still_going(board):
		# print("active")
		# print_board(board, home)
		if turn == computer1:
			move = computer_move(board, computer1, home, comptype1)
			moved = make_move(board, computer1, move, home)
			if moved == "Move Again":
				# print('Move Again!')
				continue
			turn = computer2
		else:
			move = computer_move(board, computer2, home, comptype2)
			moved = make_move(board, computer2, move, home)
			if moved == "Move Again":
				# print('Move Again!')
				continue
			turn = computer1
	# print("game over")
	comp1score, comp2score = calculate_score(board, home)
	# print(comp1score, comp2score)
	return comp1score, comp2score, computer1


def run_simulation(comp1='random', comp2='repeat_clearance'):
	# 'random', 'repeat_clearance', 'clearance_priority'
	col_3 = 'comp1 position'
	n = 10
	home = pd.DataFrame(0, index=[], columns=[comp1, comp2, col_3])
	for i in tqdm(range(0, n)):
		home.loc[i, [comp1, comp2, col_3]] = play_simulation(comp1, comp2)

	home['Margin'] = (home[comp1] - home[comp2])
	print(home.head())
	mean_score_diff = home['Margin'].mean()
	print('mean score diff is %s' % mean_score_diff)
	win = len(home[home['Margin'] > 0])
	tie = len(home[home['Margin'] == 0])
	loss = len(home[home['Margin'] < 0])
	win_percent = len(home[home['Margin'] > 0]) / len(home)
	print('win percent is %s  %s-%s-%s' % (win_percent, win, tie, loss))


# run_simulation('random', 'repeat_clearance')
play_game()
