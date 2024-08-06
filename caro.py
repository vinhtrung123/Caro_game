import sys

import random
import copy
import math
import numpy as np

from constants import *

#constants
ROWS = 17
COLS = 17

SQSIZE = MAIN_WIDTH//COLS
WIDTH = SQSIZE*COLS
HEIGHT = WIDTH
HEIGHT_BG = HEIGHT
LINE_WIDTH = SQSIZE//80
if ROWS > 8:
	LINE_WIDTH = 1
CIRCLE_WIDTH = SQSIZE//15
CROSS_WIDTH = SQSIZE//15

RADIUS = SQSIZE//3

OFFSET = SQSIZE//5

def upadateConstant(row, col):
	global ROWS
	ROWS = row
	global COLS
	COLS = col
	#print((ROWS, COLS))
	global SQSIZE
	global WIDTH
	SQSIZE= MAIN_WIDTH//COLS
	WIDTH = SQSIZE*COLS
	global HEIGHT
	HEIGHT = WIDTH
	global HEIGHT_BG
	HEIGHT_BG = HEIGHT
	global LINE_WIDTH
	LINE_WIDTH = SQSIZE//80
	if ROWS > 8:
		LINE_WIDTH = 1
	global CIRCLE_WIDTH
	CIRCLE_WIDTH = SQSIZE//15
	global CROSS_WIDTH
	CROSS_WIDTH = SQSIZE//15

	global RADIUS
	RADIUS = SQSIZE//3

	global OFFSET
	OFFSET = SQSIZE//5


#PYGAME SETUP
pygame.init()
screen = pygame.display.set_mode((WIDTH_BG, HEIGHT_BG))
pygame.display.set_caption('Caro')
# icon_image = pygame.image.load("tic-tac-toe.png")
icon_image = pygame.image.load("imgs/caro.png")
pygame.display.set_icon(icon_image)

screen.fill(EASY_BG_COLOR)
screen.fill(EASY_GAME_BG_COLOR, (0, 0, WIDTH, HEIGHT))

font = pygame.font.Font(None, 48)
text_surface = font.render("Match is end. Press R to play a new game!", True, (255, 180, 205))
text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))

map_buttons = []
gamemode_buttons = []
# MAP
map_3x3_button_rect = pygame.Rect(X_MAP_BUTTON + (MAP_BUTTON_WIDTH + MAP_BUTTON_MARGIN), Y_MAP_BUTTON, MAP_BUTTON_WIDTH, MAP_BUTTON_HEIGHT)

map_17x17_button_rect = pygame.Rect(X_MAP_BUTTON + (MAP_BUTTON_WIDTH + MAP_BUTTON_MARGIN)*3, Y_MAP_BUTTON, MAP_BUTTON_WIDTH, MAP_BUTTON_HEIGHT)
#GAME MODE
pvp_button_rect = pygame.Rect(X_GAMEMODE_RIGHT_CENTER, Y_GAMEMODE_BUTTON, GAMEMODE_BUTTON_WIDTH, GAMEMODE_BUTTON_HEIGHT)
pvai_button_rect = pygame.Rect(X_GAMEMODE_RIGHT_CENTER, Y_GAMEMODE_BUTTON + GAMEMODE_BUTTON_HEIGHT + 20, GAMEMODE_BUTTON_WIDTH, GAMEMODE_BUTTON_HEIGHT)
#LEVEL
easy_button_rect = pygame.Rect(X_LEVEL_RIGHT_CENTER, Y_LEVEL_BUTTON, LEVEL_BUTTON_WIDTH, LEVEL_BUTTON_HEIGHT)
medium_button_rect = pygame.Rect(X_LEVEL_RIGHT_CENTER, Y_LEVEL_BUTTON + (LEVEL_BUTTON_HEIGHT + 20), LEVEL_BUTTON_WIDTH, LEVEL_BUTTON_HEIGHT)
hard_button_rect = pygame.Rect(X_LEVEL_RIGHT_CENTER, Y_LEVEL_BUTTON + (LEVEL_BUTTON_HEIGHT + 20)*2, LEVEL_BUTTON_WIDTH, LEVEL_BUTTON_HEIGHT)
#RESET & QUIT
reset_button_rect = pygame.Rect(X_RESET_RIGHT_CENTER, Y_RESET_BUTTON, RESET_BUTTON_WIDTH, RESET_BUTTON_HEIGHT)
quit_button_rect = pygame.Rect(X_RESET_RIGHT_CENTER, Y_RESET_BUTTON + RESET_BUTTON_HEIGHT + 10, RESET_BUTTON_WIDTH, RESET_BUTTON_HEIGHT)


class Board:
	def __init__(self, row=17, col=17):
		self.ROWS = row
		self.COLS = col
		self.squares = np.zeros((self.ROWS, self.COLS))
		self.empty_sqrs = self.squares #[squares]
		self.mark_sqrs = 0
		self.highest_top = len(self.squares) // 2
		self.lowest_bottom = len(self.squares) // 2
		self.farthest_right = len(self.squares) // 2
		self.farthest_left = len(self.squares) // 2
		self.scope_stack = []
		self.scope_stack.append((self.highest_top, self.lowest_bottom, self.farthest_left, self.farthest_right))
		
	def check_game_over(self, last_move, show=False):
		last_move_row, last_move_col = last_move #
		winning_conditions = {
			(3, 3): 3,
			(4, 4): 3,
			(5, 5): 4,
			(6, 6): 4,
		}

		win_condition = winning_conditions.get((self.ROWS, self.COLS), 5)  # Default to 5 in case of a larger board



		# Kiểm tra chiến thắng theo hàng ngang
		col_offset = last_move_col - win_condition
		if(col_offset < -1): 
			col_offset = -1

		for i in range(win_condition):
			consecutive = 0
			col_offset += 1
			if col_offset >= self.COLS or col_offset == last_move_col + 1: 
				break
			for offset in range(win_condition):
				if col_offset + offset >= self.COLS:
					break	
				if self.squares[last_move_row][col_offset + offset] == self.squares[last_move_row][last_move_col]:
					consecutive+= 1
					if consecutive == win_condition:
						if show:
							iPos = (col_offset * SQSIZE + SQSIZE // 4, last_move_row * SQSIZE + SQSIZE // 2)
							fPos = ((col_offset + win_condition - 1) * SQSIZE + 3*(SQSIZE // 4), last_move_row * SQSIZE + SQSIZE // 2)
							pygame.draw.line(screen, WIN_LINE_COLOR, iPos, fPos, CROSS_WIDTH)
						return True

		# Kiểm tra chiến thắng theo hàng dọc
		row_offset = last_move_row - win_condition
		if(row_offset < -1): 
			row_offset = -1
		for i in range(win_condition):
			consecutive = 0
			row_offset+= 1
			if row_offset >= self.ROWS or row_offset == last_move_row + 1: 
				break
			for offset in range(win_condition):
				if row_offset + offset >= self.ROWS:
					break	
				if self.squares[row_offset + offset][last_move_col] == self.squares[last_move_row][last_move_col]:
					consecutive+= 1
					if consecutive == win_condition:
						if show:
							iPos = (last_move_col * SQSIZE + SQSIZE // 2, row_offset * SQSIZE + SQSIZE // 4)
							fPos = (last_move_col * SQSIZE + SQSIZE // 2, (row_offset + win_condition - 1) * SQSIZE + 3 * (SQSIZE // 4))
							pygame.draw.line(screen, WIN_LINE_COLOR, iPos, fPos, CROSS_WIDTH)
						return True

		# Kiểm tra chiến thắng theo đường chéo chính (từ trái trên đến phải dưới)
		row_offset = last_move_row - win_condition
		col_offset = last_move_col - win_condition
		if(row_offset < -1): 
			col_offset += -(row_offset) - 1
			row_offset = -1
		if(col_offset < -1): 
			row_offset += -(col_offset) - 1
			col_offset = -1
		for i in range(win_condition):
			consecutive = 0
			row_offset+= 1
			col_offset+= 1
			if row_offset >= self.ROWS or row_offset == last_move_row + 1: 
				break
			if col_offset >= self.COLS or col_offset == last_move_col + 1: 
				break
			for offset in range(win_condition):
				if row_offset + offset >= self.ROWS or col_offset + offset >= self.COLS:
					break	
				if self.squares[row_offset + offset][col_offset + offset] == self.squares[last_move_row][last_move_col]:
					consecutive+= 1
					if consecutive == win_condition:
						if show:
							iPos = (col_offset * SQSIZE + SQSIZE // 4, row_offset * SQSIZE + SQSIZE // 4)
							fPos = ((col_offset + win_condition - 1) * SQSIZE + 3*(SQSIZE // 4), (row_offset + win_condition - 1) * SQSIZE + 3*(SQSIZE // 4))
							pygame.draw.line(screen, WIN_LINE_COLOR, iPos, fPos, CROSS_WIDTH)
						return True
				else:
					break
				
		# Kiểm tra chiến thắng theo đường chéo phụ (từ trái dưới đến phải trên)
		
		row_offset = last_move_row + win_condition
		col_offset = last_move_col - win_condition
		if(row_offset > self.ROWS):
			col_offset += row_offset - self.ROWS 
			row_offset = self.ROWS
		if(col_offset < -1):
			row_offset = row_offset - (-col_offset - 1)
			col_offset = -1


		for i in range(win_condition):
			consecutive = 0
			row_offset-= 1
			col_offset+= 1
			
			if row_offset <= -1: 
				break
			if col_offset >= self.ROWS: 
				break
			if row_offset == last_move_row - 1 and col_offset == last_move_col + 1:
				break

			for offset in range(win_condition):
				if row_offset - offset < 0 or col_offset + offset >= self.COLS:
					break
				
				if self.squares[row_offset - offset][col_offset + offset] == self.squares[last_move_row][last_move_col]:
					consecutive+= 1
					if consecutive == win_condition:
						if show:
							iPos = (col_offset * SQSIZE + SQSIZE // 4, row_offset * SQSIZE +  3*(SQSIZE // 4))
							fPos = ((col_offset + offset) * SQSIZE + 3*(SQSIZE // 4), (row_offset - offset) * SQSIZE + SQSIZE // 4)
							pygame.draw.line(screen, WIN_LINE_COLOR, iPos, fPos, CROSS_WIDTH)
						return True
				else:
					break
		return False

	def mark_sqr(self, row, col, player):
		self.squares[row][col] = player
		self.mark_sqrs += 1
		self.update_scope((row, col))
	def unmark_sqr(self, row, col):
		self.squares[row][col] = 0
		self.mark_sqrs -= 1
		self.undo_scope()

	def empty_sqr(self, row, col):
		return self.squares[row][col] == 0

	def get_empty_sqrs(self):
		empty_sqrs = []
		for row in range(self.ROWS):
			for col in range(self.COLS):
				if self.empty_sqr(row, col):
					empty_sqrs.append((row, col))
		return empty_sqrs

	def isfull(self):
		return self.mark_sqrs == self.ROWS*self.COLS

	def isempty(self):
		return self.mark_sqrs == 0

	def update_scope(self, last_move):
		row, col = last_move
		if len(self.scope_stack) == 1:
			if (row >= 0 and row < self.ROWS) and (col >= 0 and col < self.COLS):
				self.highest_top = row
				self.lowest_bottom = row
				self.farthest_left = col
				self.farthest_right = col
				self.scope_stack.append((self.highest_top, self.lowest_bottom, self.farthest_left, self.farthest_right))
		else:
			if (row >= 0 and row < self.ROWS) and (col >= 0 and col < self.COLS):
				if row < self.highest_top:
					self.highest_top = row
				if row > self.lowest_bottom:
					self.lowest_bottom = row
				if col < self.farthest_left:
					self.farthest_left = col
				if col > self.farthest_right:
					self.farthest_right = col
				self.scope_stack.append((self.highest_top, self.lowest_bottom, self.farthest_left, self.farthest_right))
		
	def undo_scope(self):
		if len(self.scope_stack) > 1:
			self.scope_stack.pop()
			top_stack = self.scope_stack[-1]
			self.highest_top = top_stack[0]
			self.lowest_bottom = top_stack[1]
			self.farthest_left = top_stack[2]
			self.farthest_right = top_stack[3]

class AI:
	def __init__(self, row, col, level=2, player=2, depth=3):
		self.level = level
		self.player = player
		self.depth = depth
		self.ROWS = row
		self.COLS = col

	def getLevel(self):
		if self.level <= 3: #easy
			return "Easy"
		elif self.level == 4: #medium
			return "Medium"
		
		return "Hard"

	def rnd(self, board):
		empty_sqrs = board.get_empty_sqrs()
		idx = random.randrange(0, len(empty_sqrs))

		return empty_sqrs[idx]
	def is_game_over(self, board, virtual_pos):
		return board.isfull() or board.check_game_over(virtual_pos, show=False)
	def get_possible_moves(self, board):
		return board.get_empty_sqrs()

	def evaluation_lastmove(self, board, last_move, player):
		opponent = 3 - player  # Người chơi đối phương
		score = 0
		last_move_row, last_move_col = last_move #
		winning_conditions = {
			(3, 3): 3,
			(4, 4): 3,
			(5, 5): 4,
			(6, 6): 4,
		}


		win_condition = winning_conditions.get((self.ROWS, self.COLS), 5)  # Default to 5 in case of a larger board

		# Kiểm tra chiến thắng theo hàng ngang
		col_offset = last_move_col - win_condition
		if(col_offset < -1): 
			col_offset = -1

		attack_consecutive = 0
		defense_consecutive = 0
		for i in range(win_condition):
			if(attack_consecutive > 1):
				attack_consecutive -= 1
				continue
			if(defense_consecutive > 1):
				defense_consecutive -= 1
				continue
			attack_consecutive = 0
			defense_consecutive = 0
			empty = 0
			back_blocking = None
			front_blocking = None
			col_offset += 1
			if col_offset >= self.COLS or col_offset == last_move_col + 1: 
				break
			for offset in range(win_condition):
				if col_offset + offset >= self.COLS:
					if back_blocking is None:
						back_blocking = (last_move_row, -1) # bị chặn sau bởi tường
					break
				
				if board.squares[last_move_row][col_offset + offset] == player:
					if col_offset == last_move_col:
						if offset == 0 and col_offset + offset + 1 < self.COLS:
							if board.squares[last_move_row][col_offset + offset + 1] == opponent: # nếu là điểm chặn trước
								continue

					if defense_consecutive > 0: # đã có chặn đối thủ thành công => break => xét tiếp điểm liên tục của bản thân
						back_blocking = (last_move_row, col_offset + offset) # bị chặn sau
						break
					attack_consecutive += 1	
					if attack_consecutive == win_condition:
						return 100000
					if attack_consecutive == 1:
						if col_offset + offset == 0:
							front_blocking = (last_move_row, -1) # -1 => điểm chặn trước bị chặn bởi tường
						elif col_offset + offset > 0:
							if board.squares[last_move_row][col_offset + offset - 1] == opponent:
								front_blocking = (last_move_row, col_offset + offset - 1) # 1 => bị chặn 
							elif board.squares[last_move_row][col_offset + offset - 1] == 0:
								front_blocking = None # => không bị chặn trước
					
				elif board.squares[last_move_row][col_offset + offset] == 0:
					empty += 1
					if attack_consecutive == 0 or defense_consecutive == 0:
						 break
				else: #opponent
					if attack_consecutive > 0: # bị đối thủ chặn rồi => break => xét tiếp điểm liên tục của đối thủ
						back_blocking = (last_move_row, col_offset + offset) # bị chặn sau
						break
					defense_consecutive += 1
					if defense_consecutive == 1:
						if col_offset + offset == 0:
							front_blocking = (last_move_row, -1) # -1 => điểm chặn trước bị chặn bởi tường
						elif col_offset + offset > 0:
							if board.squares[last_move_row][col_offset + offset - 1] == player:
								front_blocking = (last_move_row, col_offset + offset - 1) # => bị chặn bởi quân quân ta
							elif board.squares[last_move_row][col_offset + offset - 1] == 0:
								front_blocking = None # => không bị chặn trước
			is_front_blocking = False
			if front_blocking is not None:
				is_front_blocking = front_blocking[1] == last_move_col
			is_back_blocking = False
			if back_blocking is not None:
				is_back_blocking = back_blocking[1] == last_move_col
			score += self.evaluate_window(attack_consecutive, defense_consecutive, front_blocking, back_blocking, is_front_blocking, is_back_blocking)
		
		# Kiểm tra chiến thắng theo hàng dọc
		row_offset = last_move_row - win_condition
		if(row_offset < -1): 
			row_offset = -1
		attack_consecutive = 0
		defense_consecutive = 0
		for i in range(win_condition):
			if(attack_consecutive > 1):
				attack_consecutive -= 1
				continue
			if(defense_consecutive > 1):
				defense_consecutive -= 1
				continue
			attack_consecutive = 0
			defense_consecutive = 0
			empty = 0
			back_blocking = None
			front_blocking = None
			row_offset+= 1
			if row_offset >= self.ROWS or row_offset == last_move_row + 1: 
				break
			for offset in range(win_condition):
				if row_offset + offset >= self.ROWS:
					if back_blocking is None:
						back_blocking = (-1 , last_move_col) # bị chặn sau bởi tường
					break	
				if board.squares[row_offset + offset][last_move_col] == player:
					if row_offset == last_move_row:
						if offset == 0 and row_offset + offset + 1 < self.ROWS:
							if board.squares[row_offset + offset + 1][last_move_col] == opponent: # nếu là điểm chặn trước
								continue

					if defense_consecutive > 0: # đã có chặn đối thủ thành công => break => xét tiếp điểm liên tục của bản thân
						back_blocking = (row_offset + offset, last_move_col) # bị chặn sau
						break
					attack_consecutive += 1	
					if attack_consecutive == win_condition:
						return 100000
					if attack_consecutive == 1:
						if row_offset + offset == 0:
							front_blocking = (-1, last_move_col) # -1 => điểm chặn trước bị chặn bởi tường
						elif row_offset + offset > 0:
							if board.squares[row_offset + offset - 1][last_move_col] == opponent:
								front_blocking = (row_offset + offset - 1, last_move_col) # 1 => bị chặn 
							elif board.squares[row_offset + offset - 1][last_move_col] == 0:
								front_blocking = None # => không bị chặn trước
					
				elif board.squares[row_offset + offset][last_move_col] == 0:
					empty += 1
					if attack_consecutive == 0 or defense_consecutive == 0:
						 break
				else: #opponent
					
					if attack_consecutive > 0: # bị đối thủ chặn rồi => break => xét tiếp điểm liên tục của đối thủ
						back_blocking = (row_offset + offset, last_move_col) # bị chặn sau
						break
					defense_consecutive += 1
					if defense_consecutive == 1:
						if row_offset + offset == 0:
							front_blocking = (-1, last_move_col) # -1 => điểm chặn trước bị chặn bởi tường
						elif row_offset + offset > 0:
							if board.squares[row_offset + offset - 1][last_move_col] == player:
								front_blocking = (row_offset + offset - 1, last_move_col) # => bị chặn bởi quân quân ta
							elif board.squares[row_offset + offset - 1][last_move_col] == 0:
								front_blocking = None # => không bị chặn trước
			is_front_blocking = False
			if front_blocking is not None:
				is_front_blocking = front_blocking[0] == last_move_row
			is_back_blocking = False
			if back_blocking is not None:
				is_back_blocking = back_blocking[0] == last_move_row
			score += self.evaluate_window(attack_consecutive, defense_consecutive, front_blocking, back_blocking, is_front_blocking, is_back_blocking)

		# Kiểm tra chiến thắng theo đường chéo chính (từ trái trên đến phải dưới)
		row_offset = last_move_row - win_condition
		col_offset = last_move_col - win_condition
		if(row_offset < -1): 
			col_offset += -(row_offset) - 1
			row_offset = -1
		if(col_offset < -1): 
			row_offset += -(col_offset) - 1
			col_offset = -1

		attack_consecutive = 0
		defense_consecutive = 0
		for i in range(win_condition):
			if(attack_consecutive > 1):
				attack_consecutive -= 1
				continue
			if(defense_consecutive > 1):
				defense_consecutive -= 1
				continue
			attack_consecutive = 0
			defense_consecutive = 0
			empty = 0
			back_blocking = None
			front_blocking = None

			row_offset+= 1
			col_offset+= 1
			if row_offset >= self.ROWS or row_offset == last_move_row + 1: 
				break
			if col_offset >= self.COLS or col_offset == last_move_col + 1: 
				break
			for offset in range(win_condition):

				if row_offset + offset >= self.ROWS or col_offset + offset >= self.COLS:
					if back_blocking is None:
						back_blocking = (-1 , -1) # bị chặn sau bởi tường
					break	
				if board.squares[row_offset + offset][col_offset + offset] == player:
					if row_offset == last_move_row and col_offset == last_move_col:
						if offset == 0 and row_offset + offset + 1 < self.ROWS and col_offset + offset + 1 < self.COLS:
							if board.squares[row_offset + offset + 1][col_offset + offset + 1] == opponent: # nếu là điểm chặn trước
								continue

					if defense_consecutive > 0: # đã có chặn đối thủ thành công => break => xét tiếp điểm liên tục của bản thân
						back_blocking = (row_offset + offset, col_offset + offset) # bị chặn sau
						break
					attack_consecutive += 1	
					if attack_consecutive == win_condition:
						return 100000
					if attack_consecutive == 1:
						if row_offset + offset == 0 or col_offset + offset == 0:
							front_blocking = (-1, -1) # -1 => điểm chặn trước bị chặn bởi tường
						elif row_offset + offset > 0 and col_offset + offset > 0:
							if board.squares[row_offset + offset - 1][col_offset + offset - 1] == opponent:
								front_blocking = (row_offset + offset - 1, col_offset + offset - 1) # 1 => bị chặn 
							elif board.squares[row_offset + offset - 1][col_offset + offset - 1] == 0:
								front_blocking = None # => không bị chặn trước
					
				elif board.squares[row_offset + offset][col_offset + offset] == 0:
					empty += 1
					if attack_consecutive == 0 or defense_consecutive == 0:
						 break
				else: #opponent
					
					if attack_consecutive > 0: # bị đối thủ chặn rồi => break => xét tiếp điểm liên tục của đối thủ
						back_blocking = (row_offset + offset, col_offset + offset) # bị chặn sau
						break
					defense_consecutive += 1
					if defense_consecutive == 1:
						if row_offset + offset == 0 or col_offset + offset == 0:
							front_blocking = (-1, -1) # -1 => điểm chặn trước bị chặn bởi tường
						elif row_offset + offset > 0 and col_offset + offset > 0:
							if board.squares[row_offset + offset - 1][col_offset + offset - 1] == player:
								front_blocking = (row_offset + offset - 1, col_offset + offset - 1) # => bị chặn bởi quân quân ta
							elif board.squares[row_offset + offset - 1][col_offset + offset - 1] == 0:
								front_blocking = None # => không bị chặn trước
			is_front_blocking = False
			if front_blocking is not None:
				is_front_blocking = front_blocking == last_move
			is_back_blocking = False
			if back_blocking is not None:
				is_back_blocking = back_blocking == last_move
			score += self.evaluate_window(attack_consecutive, defense_consecutive, front_blocking, back_blocking, is_front_blocking, is_back_blocking)

		# Kiểm tra chiến thắng theo đường chéo phụ (từ trái dưới đến phải trên)
		
		row_offset = last_move_row + win_condition
		col_offset = last_move_col - win_condition
		if(row_offset > self.ROWS):
			col_offset += row_offset - self.ROWS 
			row_offset = self.ROWS
		if(col_offset < -1):
			row_offset = row_offset - (-col_offset - 1)
			col_offset = -1

		attack_consecutive = 0
		defense_consecutive = 0
		for i in range(win_condition):
			if(attack_consecutive > 1):
				attack_consecutive -= 1
				continue
			if(defense_consecutive > 1):
				defense_consecutive -= 1
				continue
			attack_consecutive = 0
			defense_consecutive = 0
			empty = 0
			back_blocking = None
			front_blocking = None
			row_offset-= 1
			col_offset+= 1
			
			if row_offset <= -1: 
				break
			if col_offset >= self.ROWS: 
				break
			if row_offset == last_move_row - 1 and col_offset == last_move_col + 1:
				break

			for offset in range(win_condition):
				if row_offset - offset < 0 or col_offset + offset >= self.COLS:
					if back_blocking is None:
						back_blocking = (-1 , -1) # bị chặn sau bởi tường
					break
				if board.squares[row_offset - offset][col_offset + offset] == player:
					if row_offset == last_move_row and col_offset == last_move_col:
						if offset == 0 and row_offset - offset - 1 < self.ROWS and col_offset + offset + 1 < self.COLS:
							if board.squares[row_offset - offset - 1][col_offset + offset + 1] == opponent: # nếu là điểm chặn trước
								continue

					if defense_consecutive > 0: # đã có chặn đối thủ thành công => break => xét tiếp điểm liên tục của bản thân
						back_blocking = (row_offset - offset, col_offset + offset) # bị chặn sau
						break
					attack_consecutive += 1	
					if attack_consecutive == win_condition:
						return 100000
					if attack_consecutive == 1:
						if row_offset - offset == 0 or col_offset + offset == 0:
							front_blocking = (-1, -1) # -1 => điểm chặn trước bị chặn bởi tường
						elif row_offset - offset < self.ROWS - 1 and col_offset + offset > 0:
							if board.squares[row_offset - offset + 1][col_offset + offset - 1] == opponent:
								front_blocking = (row_offset - offset + 1, col_offset + offset - 1) # 1 => bị chặn 
							elif board.squares[row_offset - offset + 1][col_offset + offset - 1] == 0:
								front_blocking = None # => không bị chặn trước
					
				elif board.squares[row_offset - offset][col_offset + offset] == 0:
					empty += 1
					if attack_consecutive == 0 or defense_consecutive == 0:
						 break
				else: #opponent
					
					if attack_consecutive > 0: # bị đối thủ chặn rồi => break => xét tiếp điểm liên tục của đối thủ
						back_blocking = (row_offset - offset, col_offset + offset) # bị chặn sau
						break
					defense_consecutive += 1
					if defense_consecutive == 1:
						if row_offset - offset == 0 or col_offset + offset == 0:
							front_blocking = (-1, -1) # -1 => điểm chặn trước bị chặn bởi tường
						elif row_offset - offset > 0 and col_offset + offset - 1 < self.COLS and row_offset - offset + 1 < self.ROWS:
							if board.squares[row_offset - offset + 1][col_offset + offset - 1] == player:
								front_blocking = (row_offset - offset + 1, col_offset + offset - 1) # => bị chặn bởi quân quân ta
							elif board.squares[row_offset - offset + 1][col_offset + offset - 1] == 0:
								front_blocking = None # => không bị chặn trước

			is_front_blocking = False
			if front_blocking is not None:
				is_front_blocking = front_blocking == last_move
			is_back_blocking = False
			if back_blocking is not None:
				is_back_blocking = back_blocking == last_move
			score += self.evaluate_window(attack_consecutive, defense_consecutive, front_blocking, back_blocking, is_front_blocking, is_back_blocking)

		# print("lm: " + str(last_move) + "- score: " + str(score))
		return score

	def evaluation_board(self, board, player):
		player_score = self.evaluate_player_score(board, player)
		opponent_score = self.evaluate_player_score(board, 3 - player)

		return player_score - opponent_score #positive => player wins #negative => opponent wins

	def evaluate_player_score(self, board, player):
		score = 0
		score += self.evaluate_horizontal(board, player)
		score += self.evaluate_vertical(board, player)
		score += self.evaluate_diagonal(board, player)
		score += self.evaluate_2nd_diagonal(board, player)

		return score #Tổng điểm của 4 hướng duyệt

	def evaluate_horizontal(self, board, player):
		opponent = 3 - player
		score = 0

		top = board.highest_top
		bottom = board.lowest_bottom
		left = board.farthest_left
		right = board.farthest_right
		for i in range(2):
			if top > 0:
				top -= 1
			if bottom < self.ROWS - 1:
				bottom += 1
			if left > 0:
				left -= 1
			if right < self.COLS - 1:
				right += 1
		for row in range(top, bottom + 1):
			attack_consecutive = 0
			empty = 0
			back_blocking = None
			front_blocking = None
			for col in range(left, right + 1):
				if board.squares[row][col] == player:
					attack_consecutive += 1
					if attack_consecutive == 5:
						score +=  self.evaluate_window(attack_consecutive, 0, front_blocking, back_blocking, False, False)

						#reset
						attack_consecutive = 0
						empty = 0
						back_blocking = None
						front_blocking = None

						continue
					if col + 1 == self.COLS:
						back_blocking = (row, -1) # -1 => điểm chặn sau bị chặn bởi tường
						score +=  self.evaluate_window(attack_consecutive, 0, front_blocking, back_blocking, False, False)
						continue
					if attack_consecutive == 1:#
						#Tìm điểm chặn trước
						if col - 1 < 0:
							front_blocking = (row, -1) # -1 => điểm chặn trước bị chặn bởi tường
						else:
							if board.squares[row][col - 1] == opponent:
								front_blocking = (row, col - 1) # != -1 => điểm chặn trước bị chặn bởi opponent

				elif board.squares[row][col] == 0:
					if attack_consecutive == 0:
						continue
					empty += 1
					if empty == 2:
						if attack_consecutive > 1:
							score +=  self.evaluate_window(attack_consecutive, 0, front_blocking, back_blocking, False, False)

						#reset
						attack_consecutive = 0
						empty = 0
						back_blocking = None
						front_blocking = None
						if board.squares[row][col - 1] == 0: # trước đó là 0 => next
							continue
						else:
							col -= 2 # trở lại điểm trước đó
						continue

					if col + 1 == self.COLS:
						score +=  self.evaluate_window(attack_consecutive, 0, front_blocking, back_blocking, False, False)

						#reset
						attack_consecutive = 0
						empty = 0
						back_blocking = None
						front_blocking = None
						continue
				else: 
					if attack_consecutive == 0:
						continue
					back_blocking = (row, col) #=> điểm chặn sau bị chặn bởi opponent

					# thực hiện + điểm
					score +=  self.evaluate_window(attack_consecutive, 0, front_blocking, back_blocking, False, False)

					#reset
					attack_consecutive = 0
					empty = 0
					back_blocking = None
					front_blocking = None
					continue
		return score
		
	def evaluate_vertical(self, board, player):
		opponent = 3 - player
		score = 0

		top = board.highest_top
		bottom = board.lowest_bottom
		left = board.farthest_left
		right = board.farthest_right
		for i in range(2):
			if top > 0:
				top -= 1
			if bottom < self.ROWS - 1:
				bottom += 1
			if left > 0:
				left -= 1
			if right < self.COLS - 1:
				right += 1
		for col in range(left, right + 1):
			attack_consecutive = 0
			empty = 0
			back_blocking = None
			front_blocking = None
			for row in range(top, bottom + 1):
				if board.squares[row][col] == player:
					attack_consecutive += 1
					if attack_consecutive == 5:
						score +=  self.evaluate_window(attack_consecutive, 0, front_blocking, back_blocking, False, False)

						#reset
						attack_consecutive = 0
						empty = 0
						back_blocking = None
						front_blocking = None

						continue
					if row + 1 == self.ROWS:
						back_blocking = (-1, col) # -1 => điểm chặn sau bị chặn bởi tường
						score +=  self.evaluate_window(attack_consecutive, 0, front_blocking, back_blocking, False, False)
						continue
					if attack_consecutive == 1:#
						#Tìm điểm chặn trước
						if row - 1 < 0:
							front_blocking = (-1, col) # -1 => điểm chặn trước bị chặn bởi tường
						else:
							if board.squares[row - 1][col] == opponent:
								front_blocking = (row - 1, col) # != -1 => điểm chặn trước bị chặn bởi opponent

				elif board.squares[row][col] == 0:
					if attack_consecutive == 0:
						continue
					empty += 1
					if empty == 2:
						if attack_consecutive > 1:
							score +=  self.evaluate_window(attack_consecutive, 0, front_blocking, back_blocking, False, False)

						#reset
						attack_consecutive = 0
						empty = 0
						back_blocking = None
						front_blocking = None
						if board.squares[row - 1][col] == 0: # trước đó là 0 => next
							continue
						else:
							row -= 2 # trở lại điểm trước đó
						continue
					if row + 1 == self.ROWS:
						score +=  self.evaluate_window(attack_consecutive, 0, front_blocking, back_blocking, False, False)

						#reset
						attack_consecutive = 0
						empty = 0
						back_blocking = None
						front_blocking = None
						continue
				else: 
					if attack_consecutive == 0:
						continue
					back_blocking = (row, col) #=> điểm chặn sau bị chặn bởi opponent

					# thực hiện + điểm
					score +=  self.evaluate_window(attack_consecutive, 0, front_blocking, back_blocking, False, False)

					#reset
					attack_consecutive = 0
					empty = 0
					back_blocking = None
					front_blocking = None
					continue
		return score

	def evaluate_diagonal(self, board, player):
		opponent = 3 - player
		score = 0

		top = board.highest_top
		bottom = board.lowest_bottom
		left = board.farthest_left
		right = board.farthest_right
		for i in range(2):
			if top > 0:
				top -= 1
			if bottom < self.ROWS - 1:
				bottom += 1
			if left > 0:
				left -= 1
			if right < self.COLS - 1:
				right += 1
		for i in range(bottom, top - 1, -1):
			attack_consecutive = 0
			empty = 0
			back_blocking = None
			front_blocking = None
			col = left
			row = i
			while row < bottom + 1 and col < right + 1: 
				if board.squares[row][col] == player:
					attack_consecutive += 1
					if attack_consecutive == 5:
						score +=  self.evaluate_window(attack_consecutive, 0, front_blocking, back_blocking, False, False)

						#reset
						attack_consecutive = 0
						empty = 0
						back_blocking = None
						front_blocking = None

						row += 1
						col += 1
						continue
					if row + 1 == self.ROWS:
						back_blocking = (-1, -1) # -1 => điểm chặn sau bị chặn bởi tường
						score +=  self.evaluate_window(attack_consecutive, 0, front_blocking, back_blocking, False, False)
						break
					if col + 1 == self.COLS:
						back_blocking = (-1, -1) # -1 => điểm chặn sau bị chặn bởi tường
						score +=  self.evaluate_window(attack_consecutive, 0, front_blocking, back_blocking, False, False)
						break
					if attack_consecutive == 1:#
						#Tìm điểm chặn trước
						if col - 1 < 0 or row - 1 < 0:
							front_blocking = (-1, -1) # -1 => điểm chặn trước bị chặn bởi tường
						else:
							if board.squares[row - 1][col - 1] == opponent:
								front_blocking = (row - 1, col - 1) # != -1 => điểm chặn trước bị chặn bởi opponent
					row += 1
					col += 1
				elif board.squares[row][col] == 0:
					if attack_consecutive == 0:
						row += 1
						col += 1
						continue
					empty += 1
					if empty == 2:
						if attack_consecutive > 1:
							score +=  self.evaluate_window(attack_consecutive, 0, front_blocking, back_blocking, False, False)

						#reset
						attack_consecutive = 0
						empty = 0
						back_blocking = None
						front_blocking = None
						if board.squares[row - 1][col - 1] == 0: # trước đó là 0 => next
							row += 1
							col += 1
							continue
						else:
							col -= 1 # trở lại điểm trước đó
							row -= 1 # trở lại điểm trước đó
						continue
					if col + 1 == self.COLS or row + 1 == self.ROWS:
						score +=  self.evaluate_window(attack_consecutive, 0, front_blocking, back_blocking, False, False)

						#reset
						attack_consecutive = 0
						empty = 0
						back_blocking = None
						front_blocking = None
						break
					row += 1
					col += 1
				else:
					if attack_consecutive == 0:
						row += 1
						col += 1
						continue
					back_blocking = (row, col) #=> điểm chặn sau bị chặn bởi opponent

					# thực hiện + điểm
					score +=  self.evaluate_window(attack_consecutive, 0, front_blocking, back_blocking, False, False)

					#reset
					attack_consecutive = 0
					empty = 0
					back_blocking = None
					front_blocking = None
					row += 1
					col += 1
					continue

		for i in range(left, right + 1):
			attack_consecutive = 0
			empty = 0
			back_blocking = None
			front_blocking = None
			col = i
			row = top
			while row < bottom + 1 and col < right + 1: 
				if board.squares[row][col] == player:
					attack_consecutive += 1
					if attack_consecutive == 5:
						score +=  self.evaluate_window(attack_consecutive, 0, front_blocking, back_blocking, False, False)

						#reset
						attack_consecutive = 0
						empty = 0
						back_blocking = None
						front_blocking = None

						row += 1
						col += 1
						continue
					if row + 1 == self.ROWS:
						back_blocking = (-1, -1) # -1 => điểm chặn sau bị chặn bởi tường
						score +=  self.evaluate_window(attack_consecutive, 0, front_blocking, back_blocking, False, False)
						break
					if col + 1 == self.COLS:
						back_blocking = (-1, -1) # -1 => điểm chặn sau bị chặn bởi tường
						score +=  self.evaluate_window(attack_consecutive, 0, front_blocking, back_blocking, False, False)
						break
					if attack_consecutive == 1:#
						#Tìm điểm chặn trước
						if col - 1 < 0 or row - 1 < 0:
							front_blocking = (-1, -1) # -1 => điểm chặn trước bị chặn bởi tường
						else:
							if board.squares[row - 1][col - 1] == opponent:
								front_blocking = (row - 1, col - 1) # != -1 => điểm chặn trước bị chặn bởi opponent
					row += 1
					col += 1
				elif board.squares[row][col] == 0:
					if attack_consecutive == 0:
						row += 1
						col += 1
						continue
					empty += 1
					if empty == 2:
						if attack_consecutive > 1:
							score +=  self.evaluate_window(attack_consecutive, 0, front_blocking, back_blocking, False, False)

						#reset
						attack_consecutive = 0
						empty = 0
						back_blocking = None
						front_blocking = None
						if board.squares[row - 1][col - 1] == 0: # trước đó là 0 => next
							row += 1
							col += 1
							continue
						else:
							col -= 1 # trở lại điểm trước đó
							row -= 1 # trở lại điểm trước đó
						continue
					if col + 1 == self.COLS or row + 1 == self.COLS:
						score +=  self.evaluate_window(attack_consecutive, 0, front_blocking, back_blocking, False, False)

						#reset
						attack_consecutive = 0
						empty = 0
						back_blocking = None
						front_blocking = None
						break
					row += 1
					col += 1
				else: 
					if attack_consecutive == 0:
						row += 1
						col += 1
						continue
					back_blocking = (row, col) #=> điểm chặn sau bị chặn bởi opponent

					# thực hiện + điểm
					score +=  self.evaluate_window(attack_consecutive, 0, front_blocking, back_blocking, False, False)

					#reset
					attack_consecutive = 0
					empty = 0
					back_blocking = None
					front_blocking = None
					row += 1
					col += 1
					continue

		return score

	def evaluate_2nd_diagonal(self, board, player):
		opponent = 3 - player
		score = 0

		top = board.highest_top
		bottom = board.lowest_bottom
		left = board.farthest_left
		right = board.farthest_right
		for i in range(2):
			if top > 0:
				top -= 1
			if bottom < self.ROWS - 1:
				bottom += 1
			if left > 0:
				left -= 1
			if right < self.COLS - 1:
				right += 1
		for i in range(top, bottom + 1):
			attack_consecutive = 0
			empty = 0
			back_blocking = None
			front_blocking = None
			col = left
			row = i
			while row >= 0 and col < right + 1: 
				if board.squares[row][col] == player:
					attack_consecutive += 1
					if attack_consecutive == 5:
						score +=  self.evaluate_window(attack_consecutive, 0, front_blocking, back_blocking, False, False)

						#reset
						attack_consecutive = 0
						empty = 0
						back_blocking = None
						front_blocking = None
						
						row -= 1
						col += 1
						continue
					if row == 0:
						back_blocking = (-1, -1) # -1 => điểm chặn sau bị chặn bởi tường
						score +=  self.evaluate_window(attack_consecutive, 0, front_blocking, back_blocking, False, False)
						break
					if col + 1 == self.COLS:
						back_blocking = (-1, -1) # -1 => điểm chặn sau bị chặn bởi tường
						score +=  self.evaluate_window(attack_consecutive, 0, front_blocking, back_blocking, False, False)
						break
					if attack_consecutive == 1:#
						#Tìm điểm chặn trước
						if col - 1 < 0 or row + 1 >= self.ROWS:
							front_blocking = (-1, -1) # -1 => điểm chặn trước bị chặn bởi tường
						else:
							if board.squares[row + 1][col - 1] == opponent:
								front_blocking = (row + 1, col - 1) # != -1 => điểm chặn trước bị chặn bởi opponent
					row -= 1
					col += 1
				elif board.squares[row][col] == 0:
					if attack_consecutive == 0:
						row -= 1
						col += 1
						continue
					empty += 1
					if empty == 2:
						if attack_consecutive > 1:
							score +=  self.evaluate_window(attack_consecutive, 0, front_blocking, back_blocking, False, False)

						#reset
						attack_consecutive = 0
						empty = 0
						back_blocking = None
						front_blocking = None
						if board.squares[row + 1][col - 1] == 0: # trước đó là 0 => next
							row -= 1
							col += 1
							continue
						else:
							col -= 1 # trở lại điểm trước đó
							row += 1 # trở lại điểm trước đó
						continue
					if col + 1 == self.COLS or row == 0:
						score +=  self.evaluate_window(attack_consecutive, 0, front_blocking, back_blocking, False, False)

						#reset
						attack_consecutive = 0
						empty = 0
						back_blocking = None
						front_blocking = None
						break
					row -= 1
					col += 1
				else: 
					if attack_consecutive == 0:
						row -= 1
						col += 1
						continue
					back_blocking = (row, col) #=> điểm chặn sau bị chặn bởi opponent

					# thực hiện + điểm
					score +=  self.evaluate_window(attack_consecutive, 0, front_blocking, back_blocking, False, False)

					#reset
					attack_consecutive = 0
					empty = 0
					back_blocking = None
					front_blocking = None
					row -= 1
					col += 1
					continue

		for i in range(left, right + 1):
			attack_consecutive = 0
			empty = 0
			back_blocking = None
			front_blocking = None
			col = i
			row = bottom
			while row >= 0 and col < right + 1: 
				if board.squares[row][col] == player:
					attack_consecutive += 1
					if attack_consecutive == 5:
						score +=  self.evaluate_window(attack_consecutive, 0, front_blocking, back_blocking, False, False)
						
						#reset
						attack_consecutive = 0
						empty = 0
						back_blocking = None
						front_blocking = None

						row -= 1
						col += 1
						continue
					if row == 0:
						back_blocking = (-1, -1) # -1 => điểm chặn sau bị chặn bởi tường
						score +=  self.evaluate_window(attack_consecutive, 0, front_blocking, back_blocking, False, False)
						break
					if col + 1 == self.COLS:
						back_blocking = (-1, -1) # -1 => điểm chặn sau bị chặn bởi tường
						score +=  self.evaluate_window(attack_consecutive, 0, front_blocking, back_blocking, False, False)
						break
					if attack_consecutive == 1:#
						#Tìm điểm chặn trước
						if col - 1 < 0 or row + 1 >= self.ROWS:
							front_blocking = (-1, -1) # -1 => điểm chặn trước bị chặn bởi tường
						else:
							if board.squares[row + 1][col - 1] == opponent:
								front_blocking = (row + 1, col - 1) # != -1 => điểm chặn trước bị chặn bởi opponent
					row -= 1
					col += 1
				elif board.squares[row][col] == 0:
					if attack_consecutive == 0:
						row -= 1
						col += 1
						continue
					empty += 1
					if empty == 2:
						if attack_consecutive > 1:
							score +=  self.evaluate_window(attack_consecutive, 0, front_blocking, back_blocking, False, False)

						#reset
						attack_consecutive = 0
						empty = 0
						back_blocking = None
						front_blocking = None
						if board.squares[row + 1][col - 1] == 0: # trước đó là 0 => next
							row -= 1
							col += 1
							continue
						else:
							col -= 1 # trở lại điểm trước đó
							row += 1 # trở lại điểm trước đó
						continue
					if col + 1 == self.COLS or row == 0:
						score +=  self.evaluate_window(attack_consecutive, 0, front_blocking, back_blocking, False, False)

						#reset
						attack_consecutive = 0
						empty = 0
						back_blocking = None
						front_blocking = None
						break
					row -= 1
					col += 1
				else: 
					if attack_consecutive == 0:
						row -= 1
						col += 1
						continue
					back_blocking = (row, col) #=> điểm chặn sau bị chặn bởi opponent

					# thực hiện + điểm
					score +=  self.evaluate_window(attack_consecutive, 0, front_blocking, back_blocking, False, False)

					#reset
					attack_consecutive = 0
					empty = 0
					back_blocking = None
					front_blocking = None
					row -= 1
					col += 1
					continue

		return score

	def evaluate_window(self, attack_consecutive, defense_consecutive, front_blocking, back_blocking, lastmove_is_front_blocking, lastmove_is_back_blocking):
		
		# Các hằng số điểm số cho các trường hợp khác nhau
		ATTACK_SCORES = {2: 50, 3: 300, 4: 1000, 5: 10000}  # Điểm tấn công không bị chặn
		ATTACK_SCORES_1BLOCKED = {2: 5, 3: 50, 4: 500, 5: 10000}  # Điểm tấn công đã bị chặn 1 đầu
		DEFENSE_SCORES = {1: 1, 2: 20, 3: 200, 4: 10000}  # Điểm phòng thủ nếu đối phương không bị chặn
		DEFENSE_SCORES_1BLOCKED = {2: 8, 3: 80, 4: 10000}  # Điểm phòng thủ nếu đối phương bị chặn 1 đầu
		
		total_score = 0

		if defense_consecutive == 0 and attack_consecutive > 0: # đang tấn công 
			if back_blocking is not None:
				if front_blocking is None:
					# cho điểm đánh giá chỉ bị chặn sau
					total_score += ATTACK_SCORES_1BLOCKED.get(attack_consecutive, 0)
			else:
				if front_blocking is None: #
					# Điểm cho attack không bị chặn
					total_score += ATTACK_SCORES.get(attack_consecutive, 0)
				elif front_blocking is not None:
					# cho điểm đánh giá chỉ bị chặn trước
					total_score += ATTACK_SCORES_1BLOCKED.get(attack_consecutive, 0)		

		if attack_consecutive == 0 and defense_consecutive > 0: #đang phòng thủ
			if back_blocking is not None:
				if front_blocking is not None: # bị chặn bởi hai đầu
					if lastmove_is_front_blocking or lastmove_is_back_blocking: # nếu 1 trong 2 đầu bị chặn là điểm điểm đang đánh
						# => + điểm def
						total_score += DEFENSE_SCORES_1BLOCKED.get(defense_consecutive, 0)
				else:
					if lastmove_is_back_blocking: # chưa bị chặn
						# + điểm def
						total_score += DEFENSE_SCORES.get(defense_consecutive, 0)
			if front_blocking is not None:
				if lastmove_is_front_blocking: # chưa bị chặn
					# + điểm def
					total_score += DEFENSE_SCORES.get(defense_consecutive, 0)
		return total_score

	# Thuật toán Minimax với Alpha-Beta Pruning
	def minimax(self, board, depth, maximizing_player, alpha, beta, player, last_virtual_pos, rank):

		if depth == 0 or self.is_game_over(board, last_virtual_pos):
			return self.evaluation_board(board, player)
		
		possible_moves = self.get_possible_moves(board)
		if maximizing_player:
			# Sắp xếp các nước đi theo điểm đánh giá từ lớn đến nhỏ
			moves_with_evaluations = []
			for move in possible_moves:
				row, col = move
				board.squares[row][col] = player
				eval = self.evaluation_lastmove(board, move, player)
				moves_with_evaluations.append((move, eval))
				board.squares[row][col] = 0

			# Sắp xếp danh sách nước đi dựa trên giá trị evaluation_lastmove
			if player == self.player:
				moves_with_evaluations.sort(key=lambda x: x[1], reverse=True)
			else:
				moves_with_evaluations.sort(key=lambda x: x[1])

			max_eval = -math.inf
			count = 0
			for move, e in moves_with_evaluations:
				row, col = move
				board.squares[row][col] = player
				virtual_pos = move
				count += 1
				if count == rank + 1:
					board.squares[row][col] = 0
					return max_eval
				if e == 0: 
					board.squares[row][col] = 0
					return max_eval

				eval = self.minimax(board, depth - 1, False, alpha, beta, player, virtual_pos, rank)
				board.squares[row][col] = 0

				max_eval = max(max_eval, eval)
				alpha = max(alpha, eval)

				if beta <= alpha:
					break
			return max_eval
		else:
			# Sắp xếp các nước đi theo điểm đánh giá từ lớn đến nhỏ
			moves_with_evaluations = []
			for move in possible_moves:
				row, col = move
				board.squares[row][col] = 3 - player
				eval = self.evaluation_lastmove(board, move, 3 - player)
				moves_with_evaluations.append((move, eval))
				board.squares[row][col] = 0

			# Sắp xếp danh sách nước đi dựa trên giá trị evaluation_lastmove
			if player == self.player:
				moves_with_evaluations.sort(key=lambda x: x[1], reverse=True)
			else:
				moves_with_evaluations.sort(key=lambda x: x[1])

			min_eval = math.inf
			count = 0
			for move, e in moves_with_evaluations:
				row, col = move
				board.squares[row][col] = 3 - player
				virtual_pos = move
				count += 1
				if count == rank + 1:
					board.squares[row][col] = 0
					return min_eval
				if e == 0: 
					board.squares[row][col] = 0
					return min_eval

				eval = self.minimax(board, depth - 1, True, alpha, beta, player, virtual_pos, rank)
				board.squares[row][col] = 0

				min_eval = min(min_eval, eval)
				beta = min(beta, eval)

				if beta <= alpha:
					break
			return min_eval

	# Hàm chọn nước đi tối ưu cho AI
	def find_best_move(self, board, depth, player, rank):
		best_move = None
		best_eval = -math.inf if player == self.player else math.inf
		alpha = -math.inf if player == self.player else math.inf
		beta = math.inf if player == self.player else -math.inf
		possible_moves = self.get_possible_moves(board)

		# Sắp xếp các nước đi theo điểm đánh giá từ lớn đến nhỏ
		moves_with_evaluations = []
		for move in possible_moves:
			row, col = move
			board.squares[row][col] = player
			eval = self.evaluation_lastmove(board, move, player)
			moves_with_evaluations.append((move, eval))
			board.squares[row][col] = 0

		# Sắp xếp danh sách nước đi dựa trên giá trị evaluation_lastmove
		if player == self.player:
			moves_with_evaluations.sort(key=lambda x: x[1], reverse=True)
		else:
			moves_with_evaluations.sort(key=lambda x: x[1])

		count = 0
		for move, e in moves_with_evaluations:
			row, col = move
			board.squares[row][col] = player
			count += 1
			if count == rank + 1:
				board.squares[row][col] = 0
				return best_move
			if e == 0: 
				board.squares[row][col] = 0
				return best_move

			eval = self.minimax(board, depth, False, alpha, beta, player, move, rank)

			board.squares[row][col] = 0
			if player == self.player: #=>Nếu là ai
				if eval > best_eval:
					best_eval = eval
					alpha = eval
					best_move = move
			else:
				if eval < best_eval:
					best_eval = eval
					best_move = move
					beta = eval

		return best_move
		
class Game:
	def __init__(self, row=17, col=17, game_mode='ai',ai_level=2):
		self.board = Board(row, col)
		self.ai = AI(row, col, ai_level)
		self.player = 1 #1 - X #2 - O
		self.gamemode = game_mode #pvp or pvai
		self.running = True
		self.ROWS = row
		self.COLS = col
		self.show_lines(self.ROWS, self.COLS)
		self.lastmove = None

	def make_move(self, row, col):
		self.board.mark_sqr(row, col, self.player)
		self.draw_fig(row, col)
		self.next_turn()
		self.lastmove = (row, col)
		if self.isover():
			self.running = False

	def show_lines(self, row, col):
		screen = pygame.display.set_mode((WIDTH_BG, HEIGHT_BG))
		if self.ai.level <= 3: #easy
			screen.fill(EASY_BG_COLOR)
			screen.fill(EASY_GAME_BG_COLOR, (0, 0, WIDTH, HEIGHT))
		elif self.ai.level == 4: #medium
			screen.fill(MEDIUM_BG_COLOR)
			screen.fill(MEDIUM_GAME_BG_COLOR, (0, 0, WIDTH, HEIGHT))
		elif self.ai.level > 4: #hard
			screen.fill(HARD_BG_COLOR)
			screen.fill(HARD_GAME_BG_COLOR, (0, 0, WIDTH, HEIGHT))

		#vertical
		for i in range(1, col + 1):
			x = i * (WIDTH//col)
			pygame.draw.line(screen, LINE_COLOR, (x, 0), (x, HEIGHT), LINE_WIDTH)
		#horizontal
		for i in range(1, row):
			y = i * (HEIGHT//row)
			pygame.draw.line(screen, LINE_COLOR, (0, y), (WIDTH, y), LINE_WIDTH)

	def draw_fig(self, row, col):
		if self.player == 1:
			#draw X
			#desc line
			start_desc = (col * SQSIZE + OFFSET, row * SQSIZE + OFFSET)
			end_desc = (col * SQSIZE + SQSIZE - OFFSET, row * SQSIZE + SQSIZE - OFFSET)
			pygame.draw.line(screen, CROSS_COLOR, start_desc, end_desc, CROSS_WIDTH)
			
			#asc line
			start_asc = (col * SQSIZE + OFFSET, row * SQSIZE + SQSIZE - OFFSET)
			end_asc = (col * SQSIZE + SQSIZE - OFFSET, row * SQSIZE + OFFSET)
			pygame.draw.line(screen, CROSS_COLOR, start_asc, end_asc, CROSS_WIDTH)

		elif self.player == 2:
			#draw O
			center = (col * SQSIZE + SQSIZE // 2, row * SQSIZE + SQSIZE // 2)
			pygame.draw.circle(screen, CIRCLE_COLOR, center, RADIUS, CIRCLE_WIDTH)


	def next_turn(self):
		self.player = 3 - self.player


	def change_gamemode(self):
		if self.gamemode == 'pvp':
			self.gamemode = 'ai'
		else:
			self.gamemode = 'pvp'


	def isover(self):
		return self.board.check_game_over(self.lastmove, show=True) != 0 or self.board.isfull()

	def reset(self, row, col, game_mode='ai',ai_level=2):
		self.__init__(row, col, game_mode, ai_level)

	# Hàm vẽ nút
	def draw_button(self, x, y, width, height, text, button_color, text_color, font_size):
		button_rect = pygame.Rect(x, y, width, height)
		pygame.draw.rect(screen, button_color, button_rect)
		font = pygame.font.Font(None, font_size)
		text_surface = font.render(text, True, text_color)
		text_rect = text_surface.get_rect(center=button_rect.center)
		screen.blit(text_surface, text_rect)
	# Hàm vẽ đoạn text
	def draw_text(self, x, y, text, text_color, font_size):
		font = pygame.font.Font(None, font_size)
		text_surface = font.render(text, True, text_color)
		text_rect = text_surface.get_rect(midtop=(x, y))
		screen.blit(text_surface, text_rect)

def main():

	#object
	game = Game()
	board = game.board
	ai = game.ai
	#print(board.squares)
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()

			if game.running == False:
				# Vẽ dòng chữ "Match is end. Press R to play a new game!" lên màn hình
				game.draw_button(0, HEIGHT//2, WIDTH, 40, "Match is end. Press R to play a new game!", BLACK, WHITE, 36)
					
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_r:
						if game.gamemode == 'ai':
							game.reset(game.ROWS, game.COLS, game.gamemode, ai.level)
						else:
							game.reset(game.ROWS, game.COLS, game.gamemode)
						board = game.board
						ai = game.ai
				if event.type == pygame.MOUSEBUTTONDOWN:
					if map_3x3_button_rect.collidepoint(event.pos) and game.ROWS != 3:
						# Xử lý sự kiện khi click vào nút 3x3
						game.ROWS = 3
						game.COLS = 3
						upadateConstant(game.ROWS, game.COLS)
						if game.gamemode == 'ai':
							game.reset(game.ROWS, game.COLS, game.gamemode, ai.level)
						else:
							game.reset(game.ROWS, game.COLS, game.gamemode)
						board = game.board
						ai = game.ai
						
						
					if map_17x17_button_rect.collidepoint(event.pos) and game.ROWS != 17:
						# Xử lý sự kiện khi click vào nút 17x17
						game.ROWS = 17
						game.COLS = 17
						upadateConstant(game.ROWS, game.COLS)
						if game.gamemode == 'ai':
							game.reset(game.ROWS, game.COLS, game.gamemode, ai.level)
						else:
							game.reset(game.ROWS, game.COLS, game.gamemode)
						board = game.board
						ai = game.ai
						

					if pvp_button_rect.collidepoint(event.pos) and game.gamemode == 'ai':
						game.change_gamemode()

					if pvai_button_rect.collidepoint(event.pos) and game.gamemode == 'pvp':
						game.change_gamemode()

					if easy_button_rect.collidepoint(event.pos) and game.gamemode == 'ai':
						game.ai.level = 2 #easy
						game.reset(game.ROWS, game.COLS, game.gamemode, game.ai.level)
						board = game.board
						ai = game.ai
					if medium_button_rect.collidepoint(event.pos) and game.gamemode == 'ai':
						game.ai.level = 4 #medium
						game.reset(game.ROWS, game.COLS, game.gamemode, game.ai.level)
						board = game.board
						ai = game.ai
					if hard_button_rect.collidepoint(event.pos) and game.gamemode == 'ai':
						game.ai.level = 8 #hard
						game.reset(game.ROWS, game.COLS, game.gamemode, game.ai.level)
						board = game.board
						ai = game.ai
					if reset_button_rect.collidepoint(event.pos):
						if game.gamemode == 'ai':
							game.reset(game.ROWS, game.COLS, game.gamemode, ai.level)
						else:
							game.reset(game.ROWS, game.COLS, game.gamemode)
						board = game.board
						ai = game.ai
					if quit_button_rect.collidepoint(event.pos):
						pygame.quit()
						sys.exit()

				pygame.display.update()		 
			else:
				if game.gamemode == 'ai' and game.player == ai.player:

					#ai methods

					#print("AI playing: ...")

					bestmove = ai.find_best_move(board, ai.depth, ai.player, ai.level)
					if bestmove is not None:

						game.make_move(bestmove[0], bestmove[1])

					if game.isover():
						game.running = False

					pygame.time.delay(1000)
					pygame.display.update() #update lại màn hình với delay là 1 giây để tạo hiệu ứng suy nghĩ 
					#print("AI played: your turn")	   
				if event.type == pygame.MOUSEBUTTONDOWN:
					pos = event.pos
					row = pos[1] // SQSIZE
					col = pos[0] // SQSIZE
					if pos[0] < WIDTH:
						if board.empty_sqr(row, col) and game.running:
							game.make_move(row, col)

				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_g:
						game.change_gamemode()

				#ai - random - lv0
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_0:			 
						ai.level = 0

				#ai - minimax - lv1
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_1:	
						ai.level = 1


				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_r:
						if game.gamemode == 'ai':
							game.reset(game.ROWS, game.COLS, game.gamemode, ai.level)
						else:
							game.reset(game.ROWS, game.COLS, game.gamemode)
						board = game.board
						ai = game.ai

				pygame.display.update()
				if event.type == pygame.MOUSEBUTTONDOWN:
					if map_3x3_button_rect.collidepoint(event.pos) and game.ROWS != 3:
						# Xử lý sự kiện khi click vào nút 3x3
						game.ROWS = 3
						game.COLS = 3
						upadateConstant(game.ROWS, game.COLS)
						if game.gamemode == 'ai':
							game.reset(game.ROWS, game.COLS, game.gamemode, ai.level)
						else:
							game.reset(game.ROWS, game.COLS, game.gamemode)
						board = game.board
						ai = game.ai
						
						
					if map_17x17_button_rect.collidepoint(event.pos) and game.ROWS != 17:
						# Xử lý sự kiện khi click vào nút 17x17
						game.ROWS = 17
						game.COLS = 17
						upadateConstant(game.ROWS, game.COLS)
						if game.gamemode == 'ai':
							game.reset(game.ROWS, game.COLS, game.gamemode, ai.level)
						else:
							game.reset(game.ROWS, game.COLS, game.gamemode)
						board = game.board
						ai = game.ai
						

					if pvp_button_rect.collidepoint(event.pos) and game.gamemode == 'ai':
						game.change_gamemode()

					if pvai_button_rect.collidepoint(event.pos) and game.gamemode == 'pvp':
						game.change_gamemode()

					if easy_button_rect.collidepoint(event.pos) and game.gamemode == 'ai':
						game.ai.level = 2 #easy
						game.reset(game.ROWS, game.COLS, game.gamemode, game.ai.level)
						board = game.board
						ai = game.ai
					if medium_button_rect.collidepoint(event.pos) and game.gamemode == 'ai':
						game.ai.level = 4 #medium
						game.reset(game.ROWS, game.COLS, game.gamemode, game.ai.level)
						board = game.board
						ai = game.ai
					if hard_button_rect.collidepoint(event.pos) and game.gamemode == 'ai':
						game.ai.level = 6 #hard
						game.reset(game.ROWS, game.COLS, game.gamemode, game.ai.level)
						board = game.board
						ai = game.ai
					if reset_button_rect.collidepoint(event.pos):
						if game.gamemode == 'ai':
							game.reset(game.ROWS, game.COLS, game.gamemode, ai.level)
						else:
							game.reset(game.ROWS, game.COLS, game.gamemode)
						board = game.board
						ai = game.ai
					if quit_button_rect.collidepoint(event.pos):
						pygame.quit()
						sys.exit()


		# Vẽ đoạn text ở giữa và phía trên cùng của phần bên phải
		game.draw_text(WIDTH + (WIDTH_BG - WIDTH) // 2, 12, "MAP SETTING", WHITE, 36)
		if game.ROWS == 3:
			# Vẽ nút "3x3"
			game.draw_button(X_MAP_BUTTON + (MAP_BUTTON_WIDTH + MAP_BUTTON_MARGIN)*1, Y_MAP_BUTTON, MAP_BUTTON_WIDTH, MAP_BUTTON_HEIGHT, "3 win", MAP_SELECTED_COLOR, WHITE, 26)
		else:
			# Vẽ nút "3x3"
			game.draw_button(X_MAP_BUTTON + (MAP_BUTTON_WIDTH + MAP_BUTTON_MARGIN)*1, Y_MAP_BUTTON, MAP_BUTTON_WIDTH, MAP_BUTTON_HEIGHT, "3 win", GRAY, WHITE, 26)
		if game.ROWS == 17:
			# Vẽ nút "17x17"
			game.draw_button(X_MAP_BUTTON + (MAP_BUTTON_WIDTH + MAP_BUTTON_MARGIN)*3, Y_MAP_BUTTON, MAP_BUTTON_WIDTH, MAP_BUTTON_HEIGHT, "5 win", MAP_SELECTED_COLOR, WHITE, 26)
		else:
			# Vẽ nút "17x17"
			game.draw_button(X_MAP_BUTTON + (MAP_BUTTON_WIDTH + MAP_BUTTON_MARGIN)*3, Y_MAP_BUTTON, MAP_BUTTON_WIDTH, MAP_BUTTON_HEIGHT, "5 win", GRAY, WHITE, 26)
		

		# Vẽ đoạn text ở giữa và phía trên cùng của phần bên phải

		game.draw_text(WIDTH + (WIDTH_BG - WIDTH) // 2, Y_MAP_BUTTON + MAP_BUTTON_HEIGHT + 20, "GAME MODE", WHITE, 36)
		
		if game.gamemode == 'ai':
			# Vẽ nút "PvP"
			game.draw_button(X_GAMEMODE_RIGHT_CENTER, Y_GAMEMODE_BUTTON, GAMEMODE_BUTTON_WIDTH, GAMEMODE_BUTTON_HEIGHT, "PvP", GRAY, WHITE, 36)
			# Vẽ nút "PvAI"
			game.draw_button(X_GAMEMODE_RIGHT_CENTER, Y_GAMEMODE_BUTTON + GAMEMODE_BUTTON_HEIGHT + 20, GAMEMODE_BUTTON_WIDTH, GAMEMODE_BUTTON_HEIGHT, "PvAI", GAMEMODE_SELECTED_COLOR, WHITE, 36)
			if game.ai.getLevel() == "Easy":
				# Vẽ nút "Easy"
				game.draw_button(X_LEVEL_RIGHT_CENTER, Y_LEVEL_BUTTON, LEVEL_BUTTON_WIDTH, LEVEL_BUTTON_HEIGHT, "EASY", LEVEL_SELECTED_COLOR, WHITE, 36)
			else:
				# Vẽ nút "Easy"
				game.draw_button(X_LEVEL_RIGHT_CENTER, Y_LEVEL_BUTTON, LEVEL_BUTTON_WIDTH, LEVEL_BUTTON_HEIGHT, "Easy", GRAY, WHITE, 36)

			if game.ai.getLevel() == "Medium":
				# Vẽ nút "Medium"
				game.draw_button(X_LEVEL_RIGHT_CENTER, Y_LEVEL_BUTTON + (LEVEL_BUTTON_HEIGHT + 20), LEVEL_BUTTON_WIDTH, LEVEL_BUTTON_HEIGHT, "MEDIUM", LEVEL_SELECTED_COLOR, WHITE, 36)
			else:
				# Vẽ nút "Medium"
				game.draw_button(X_LEVEL_RIGHT_CENTER, Y_LEVEL_BUTTON + (LEVEL_BUTTON_HEIGHT + 20), LEVEL_BUTTON_WIDTH, LEVEL_BUTTON_HEIGHT, "Medium", GRAY, WHITE, 36)
			
			if game.ai.getLevel() == "Hard":
				# Vẽ nút "Hard"
				game.draw_button(X_LEVEL_RIGHT_CENTER, Y_LEVEL_BUTTON + (LEVEL_BUTTON_HEIGHT + 20)*2, LEVEL_BUTTON_WIDTH, LEVEL_BUTTON_HEIGHT, "HARD", LEVEL_SELECTED_COLOR, WHITE, 36)
			else:
				# Vẽ nút "Hard"
				game.draw_button(X_LEVEL_RIGHT_CENTER, Y_LEVEL_BUTTON + (LEVEL_BUTTON_HEIGHT + 20)*2, LEVEL_BUTTON_WIDTH, LEVEL_BUTTON_HEIGHT, "Hard", GRAY, WHITE, 36)
			
		else:
			# Vẽ nút "PvP"
			game.draw_button(X_GAMEMODE_RIGHT_CENTER, Y_GAMEMODE_BUTTON, GAMEMODE_BUTTON_WIDTH, GAMEMODE_BUTTON_HEIGHT, "PvP", GAMEMODE_SELECTED_COLOR, WHITE, 36)
			# Vẽ nút "PvAI"
			game.draw_button(X_GAMEMODE_RIGHT_CENTER, Y_GAMEMODE_BUTTON + GAMEMODE_BUTTON_HEIGHT + 20, GAMEMODE_BUTTON_WIDTH, GAMEMODE_BUTTON_HEIGHT, "PvAI", GRAY, WHITE, 36)
			# Vẽ nút "Easy"
			game.draw_button(X_LEVEL_RIGHT_CENTER, Y_LEVEL_BUTTON, LEVEL_BUTTON_WIDTH, LEVEL_BUTTON_HEIGHT, "Easy", LEVEL_DISABLED_COLOR, WHITE, 36)
			# Vẽ nút "Medium"
			game.draw_button(X_LEVEL_RIGHT_CENTER, Y_LEVEL_BUTTON + (LEVEL_BUTTON_HEIGHT + 20), LEVEL_BUTTON_WIDTH, LEVEL_BUTTON_HEIGHT, "Medium", LEVEL_DISABLED_COLOR, WHITE, 36)
			# Vẽ nút "Hard"
			game.draw_button(X_LEVEL_RIGHT_CENTER, Y_LEVEL_BUTTON + (LEVEL_BUTTON_HEIGHT + 20)*2, LEVEL_BUTTON_WIDTH, LEVEL_BUTTON_HEIGHT, "Hard", LEVEL_DISABLED_COLOR, WHITE, 36)


		#HEIGHT = 460
		# Vẽ nút "RESET"
		game.draw_button(X_RESET_RIGHT_CENTER, Y_RESET_BUTTON, RESET_BUTTON_WIDTH, RESET_BUTTON_HEIGHT, "RESET", GRAY, WHITE, 36)
		# Vẽ nút "QUIT"
		game.draw_button(X_RESET_RIGHT_CENTER, Y_RESET_BUTTON  + RESET_BUTTON_HEIGHT + 10, RESET_BUTTON_WIDTH, RESET_BUTTON_HEIGHT, "QUIT", GRAY, WHITE, 36)
		

		#Hover for map
		#3x3
		if map_3x3_button_rect.collidepoint(pygame.mouse.get_pos()):
			game.draw_button(X_MAP_BUTTON + (MAP_BUTTON_WIDTH + MAP_BUTTON_MARGIN)*1, Y_MAP_BUTTON, MAP_BUTTON_WIDTH, MAP_BUTTON_HEIGHT, "3x3", MAP_HOVER_COLOR, WHITE, 26)
			# Thiết lập kiểu con trỏ chuột thành kiểu "hand"
			pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)

		
		#17x17
		elif map_17x17_button_rect.collidepoint(pygame.mouse.get_pos()):
			game.draw_button(X_MAP_BUTTON + (MAP_BUTTON_WIDTH + MAP_BUTTON_MARGIN)*3, Y_MAP_BUTTON, MAP_BUTTON_WIDTH, MAP_BUTTON_HEIGHT, "17x17", MAP_HOVER_COLOR, WHITE, 26)
			# Thiết lập kiểu con trỏ chuột thành kiểu "hand"
			pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)


		#Hover for game mode
		#pvp
		elif pvp_button_rect.collidepoint(pygame.mouse.get_pos()):
			game.draw_button(X_GAMEMODE_RIGHT_CENTER, Y_GAMEMODE_BUTTON, GAMEMODE_BUTTON_WIDTH, GAMEMODE_BUTTON_HEIGHT, "PvP", GAMEMODE_HOVER_COLOR, WHITE, 36)
			# Thiết lập kiểu con trỏ chuột thành kiểu "hand"
			pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)

		#pvai
		elif pvai_button_rect.collidepoint(pygame.mouse.get_pos()):
			game.draw_button(X_GAMEMODE_RIGHT_CENTER, Y_GAMEMODE_BUTTON + GAMEMODE_BUTTON_HEIGHT + 20, GAMEMODE_BUTTON_WIDTH, GAMEMODE_BUTTON_HEIGHT, "PvAI", GAMEMODE_HOVER_COLOR, WHITE, 36)
			# Thiết lập kiểu con trỏ chuột thành kiểu "hand"
			pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)


		#Hover for level
		#easy
		elif easy_button_rect.collidepoint(pygame.mouse.get_pos()):
			if game.gamemode == 'ai':
				game.draw_button(X_LEVEL_RIGHT_CENTER, Y_LEVEL_BUTTON, LEVEL_BUTTON_WIDTH, LEVEL_BUTTON_HEIGHT, "EASY", LEVEL_HOVER_COLOR, WHITE, 36)
				# Thiết lập kiểu con trỏ chuột thành kiểu "hand"
				pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
		
		#medium
		elif medium_button_rect.collidepoint(pygame.mouse.get_pos()):
			if game.gamemode == 'ai':
				game.draw_button(X_LEVEL_RIGHT_CENTER, Y_LEVEL_BUTTON + (LEVEL_BUTTON_HEIGHT + 20), LEVEL_BUTTON_WIDTH, LEVEL_BUTTON_HEIGHT, "MEDIUM", LEVEL_HOVER_COLOR, WHITE, 36)
				# Thiết lập kiểu con trỏ chuột thành kiểu "hand"
				pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)

		#hard
		elif hard_button_rect.collidepoint(pygame.mouse.get_pos()):
			if game.gamemode == 'ai':
				game.draw_button(X_LEVEL_RIGHT_CENTER, Y_LEVEL_BUTTON + (LEVEL_BUTTON_HEIGHT + 20)*2, LEVEL_BUTTON_WIDTH, LEVEL_BUTTON_HEIGHT, "HARD", LEVEL_HOVER_COLOR, WHITE, 36)
				# Thiết lập kiểu con trỏ chuột thành kiểu "hand"
				pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)

		#Hover for reset & quit
		elif reset_button_rect.collidepoint(pygame.mouse.get_pos()):
			game.draw_button(X_RESET_RIGHT_CENTER, Y_RESET_BUTTON, RESET_BUTTON_WIDTH, RESET_BUTTON_HEIGHT, "RESET", RnQ_HOVER_COLOR, WHITE, 36)
			# Thiết lập kiểu con trỏ chuột thành kiểu "hand"
			pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)

		elif quit_button_rect.collidepoint(pygame.mouse.get_pos()):
			game.draw_button(X_RESET_RIGHT_CENTER, Y_RESET_BUTTON  + RESET_BUTTON_HEIGHT + 10, RESET_BUTTON_WIDTH, RESET_BUTTON_HEIGHT, "QUIT", RnQ_HOVER_COLOR, WHITE, 36)
			# Thiết lập kiểu con trỏ chuột thành kiểu "hand"
			pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)

		else:
			# Thiết lập kiểu con trỏ chuột mặc định
			pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
main()
