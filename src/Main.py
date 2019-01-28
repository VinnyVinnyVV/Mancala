
# Simple TicTacToe game in Python - EAO

import random
import pandas as pd
import sys

size = 6
board = pd.DataFrame(4, index=range(0, size), columns=['Player A', 'Player B'])
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
	# if random.randint(0, 1) == 0:
	# 	return chars[::-1]
	return roles


def can_move(brd, player, move):
	if move in brd.index and brd.loc[move, player] > 0:
		return True
	return False


# def can_win(board, player, move):
# 	places = []
# 	x = 0
# 	for i in board:
# 		if i == player:
# 			places.append(x)
# 		x += 1
# 	win = True
# 	for tup in winners:
# 		win = True
# 		for ix in tup:
# 			if board[ix] != player:
# 				win = False
# 				break
# 		if win == True:
# 			break
# 	return win


def make_move(board, player, move, undo=False):
	other_player = board.columns.values[board.columns.values != player][0]
	if can_move(board, player, move):
		count = board.loc[move, player]
		board.loc[move, player] = 0
		if move > 0:
			increased_cells = list(range(max(0, move - count), move))
			board.loc[board.index.isin(increased_cells), player] += 1  # Check this
			count = count - move
		if count < 1:
			# print('min of increased cells = ', min(increased_cells))
			if (board.loc[min(increased_cells), player] == 1) and (board.loc[size - 1-min(increased_cells), other_player] > 0):
				home.loc[player, 'Scores'] += board.loc[size - 1-min(increased_cells), other_player] + 1
				board.loc[min(increased_cells), player] = 0
				board.loc[size - 1 - min(increased_cells), other_player]= 0
			return True
		elif count == 1:
			home.loc[player, 'Scores'] += 1
			if game_still_going():
				if player == 'Player A':
					print_board()
					print('Move again!')
					new_move = user_move()
					make_move(board, player, new_move)
				else:  # player == 'Player B'
					print('Computer moves again')
					computer_move()
			else:
				return True
		else:  # count > 1
			home.loc[player, 'Scores'] += 1
			count -= 1
			if count > size:
				board[other_player] += 1
				count -= size
				# cycle again with count, move = size - 1
			else:
				for i in range(0, count):
					board.loc[size - 1-i, other_player] += 1
		#
		# if undo:
		# 	board[move - 1] = move - 1
		return True
	return False


def user_move():
	print('# Make your move ! [1-6] : ', end='')
	return int(input()) - 1


# AI goes here
def computer_move():
	print_board()
	available_moves = board[board[computer] > 0].index
	# if len(available_moves)
	move = random.choice(available_moves)
	print('Player B moves: ', (move + 1))
	# move = -1
	# # If I can win, others don't matter.
	# for i in range(1, 10):
	# 	if make_move(board, computer, i, True)[1]:
	# 		move = i
	# 		break
	# if move == -1:
	# 	# If player can win, block him.
	# 	for i in range(1, 10):
	# 		if make_move(board, player, i, True)[1]:
	# 			move = i
	# 			break
	# if move == -1:
	# 	# Otherwise, try to take one of desired places.
	# 	for tup in moves:
	# 		for mv in tup:
	# 			if move == -1 and can_move(board, computer, mv):
	# 				move = mv
	# 				break
	return make_move(board, computer, move)


def game_still_going():
	# print(board)
	return (len(board[board[computer] > 0]) > 0) and (len(board[board[player] > 0]) > 0)


player, computer = starting_position()
print('Player is %s and computer is %s' % (player, computer))
result = 'tie'
while game_still_going():
	# print("active")
	print_board()
	move = user_move()
	moved = make_move(board, player, move)
	if not moved:
		print(' >> Invalid number ! Try again !')
		continue
	if game_still_going():
		computer_move()
	#
	# if won:
	# 	result = '*** Congratulations ! You won ! ***'
	# 	break
	# elif computer_move()[1]:
	# 	result = '=== You lose ! =='
	# 	break;

# check for ties
# result = home.idmax()

print_board()
print("game over")
for player in board.columns.values:
	home.loc[player, 'Scores'] += sum(board.loc[:, player])
if max(home['Scores']) == min(home['Scores']):
	print('Tie Game: %s to %s' % (max(home['Scores']), min(home['Scores'])))
else:
	result = home['Scores'].idxmax()
	print('%s wins! [%s] to [%s]' % (result, max(home['Scores']), min(home['Scores'])))
