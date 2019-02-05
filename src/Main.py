
import random
import pandas as pd

size = 2
board = pd.DataFrame(2, index=range(0, size), columns=['Player A', 'Player B'])
home = pd.DataFrame(0, index=['Player A', 'Player B'], columns=['Scores'])
player, computer = '', ''


def print_board():
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


def turn_cycle(move, count, player):
	other_player = board.columns.values[board.columns.values != player][0]
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
		if game_still_going():
			if player == 'Player A':
				print_board()
				print('Move again!')
				new_move = user_move()
				return make_move(board, player, new_move)
			else:  # player == 'Player B'
				print('Computer moves again')
				return computer_move()
		else:
			return True
	else:  # count > 1 # If it passes home
		home.loc[player, 'Scores'] += 1
		count -= 1
		if count > size:  # If it makes it all the way around
			board[other_player] += 1
			count -= size
			return turn_cycle(size-1, count, player)
		else:
			for i in range(0, count):
				board.loc[size - 1 - i, other_player] += 1
			return True


def make_move(board, player, move, undo=False):
	if can_move(board, player, move):
		count = board.loc[move, player]
		board.loc[move, player] = 0
		return turn_cycle(move, count, player)
		# return True
	return False


def user_move():
	print('# Make your move ! [1-6] : ', end='')
	return int(input()) - 1


def repeatable_moves(board, player):
	repeat_moves = []
	for i in board[player].index:
		if board.loc[i, player] == (i + 1):
			repeat_moves.append(i)
	print('repeatable indicies are : %s' % repeat_moves)
	return repeat_moves


def clearance_moves(board, player):
	other_player = board.columns.values[board.columns.values != player][0]
	clear_moves = []
	for i in board[player].index:
		count = board.loc[i, player]
		if count > 0 and (
				i-count >= 0) and (
				board.loc[i - count, player] == 0) and (
				board.loc[(size - i), other_player] > 0):
			clear_moves.append(i)
	print('clearance indicies are : %s' % clear_moves)
	return clear_moves


# AI goes here
def computer_move():
	available_moves = board[board[computer] > 0].index
	repeat_moves = repeatable_moves(board, computer)
	clear_moves = clearance_moves(board, computer)
	# print(repeat_moves)
	if len(repeat_moves) > 0:
		move = min(repeat_moves)
	elif len(clear_moves) > 0:
		move = random.choice(clear_moves)
	else:
		move = random.choice(available_moves)
	print('%s moves: %s' % (computer, move + 1))

	return move


def game_still_going():
	# print(board)
	return (len(board[board[computer] > 0]) > 0) and (len(board[board[player] > 0]) > 0)


def calculate_score():
	print_board()
	for player in board.columns.values:
		home.loc[player, 'Scores'] += sum(board.loc[:, player])
	result = home['Scores']
	if max(home['Scores']) == min(home['Scores']):
		print('Tie Game: %s to %s' % (max(home['Scores']), min(home['Scores'])))
	else:
		winner = home['Scores'].idxmax()
		print('%s wins! [%s] to [%s]' % (winner, max(home['Scores']), min(home['Scores'])))
	return result


# def play_game(board, home, player, computer):
player, computer = starting_position()
print('Player is %s and computer is %s' % (player, computer))
result = 'tie'
turn = 'Player A'
while game_still_going():
	# print("active")
	print_board()
	if turn == 'Player A':
		move = user_move()
		moved = make_move(board, player, move)
		if not moved:
			print(' >> Invalid number ! Try again !')
			continue
		turn = 'Player B'
	else:
		move = computer_move()
		moved = make_move(board, computer, move)
print("game over")
result = calculate_score()
print(result)


# play_game(board, home, player, computer)
