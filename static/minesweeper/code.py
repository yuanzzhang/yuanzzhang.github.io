from AI import AI
from Action import Action
import numpy as np
import time


class MyAI( AI ):

	def __init__(self, rowDimension, colDimension, totalMines, startX, startY):
		self.__rowD = rowDimension
		self.__colD = colDimension
		self.__totalMines = totalMines
		self.__x = startX
		self.__y = startY
		self.__board = np.full((colDimension, rowDimension), '.')
		self.__uncovered = 0
		self.__safeCells = set()
		self.__founded = 0
		self.__frontier = set()
		self.__waitToDrop = set()


	def getAction(self, number: int) -> "Action Object":
		x, y = self.__x, self.__y
		self.__updateACell(x, y, number)

		if self.check_complete():
			return Action(AI.Action.LEAVE)

		self.__frontier.add( (x, y) )
		if self.__safeCells:
			return self.__uncover_safe_tile()


		for row in range(0, self.__colD):
			for col in range(0, self.__rowD):

				# add all neighbors of a zero into a set and uncover them.
				if self.__board[row][col] == '0':
					self.__safeCells.update(self.__get_covered_unmarked_neighbor(row, col))

					if self.__safeCells:
						return self.__uncover_safe_tile()


		action = self.single_point_logic()
		if action:
			return action
		else:
			action = self.single_point_logic()
			if action:
				return action


		if self.__founded == self.__totalMines:
			for row in range(0, self.__colD):
				for col in range(0, self.__rowD):
					if self.__board[row][col] == '.':
						self.__safeCells.add( (row, col) )


		#self.printBoard()
		#print("Frontier")

		self.__build_froniter()

		#self.print_frontier(self.__uncovered_frontier)
		#self.print_frontier(self.__covered_frontier)
		#print()
		#print(self.__x + 1, self.__y + 1)
		return self.__model_checking()

		return Action(AI.Action.LEAVE)


######################################################################################
######################################################################################
######################################################################################
	def __model_checking(self):
		bit_vector = np.zeros(len(self.__covered_frontier), dtype = int)
		valid_model = np.zeros(len(self.__covered_frontier), dtype = int)
		reference = list(self.__covered_frontier)
		valid_count = 0

		if self.__check_constraint(bit_vector, reference) == True:
			valid_model += bit_vector
			valid_count += 1

		start_time = time.time()
		stop = False
		while not stop and (time.time() - start_time < 3):
			if bit_vector[0] == 0:
				bit_vector[0] = 1

				if sum(bit_vector) == len(bit_vector):
					stop = True

			else:
				for i in range(0, len(bit_vector)):
					if bit_vector[i] == 1:
						bit_vector[i] = 0
					else:
						bit_vector[i] = 1
						break

			if self.__check_constraint(bit_vector, reference) == True:
					valid_model += bit_vector
					valid_count += 1
		
		for i, num in enumerate(valid_model):
			if num == valid_count:
				x, y = reference[i]
				self.__board[x][y] = 'f'
				self.__founded += 1

		x, y = reference[np.argmin(valid_model)]
		self.__x, self.__y = x, y
		return Action(AI.Action.UNCOVER, x, y)


	def __check_constraint(self, array, reference):
		for x, y in self.__uncovered_frontier:
			label = 0
			covered = self.__get_covered_unmarked_neighbor(x, y)

			for xp, yp in covered:
				index = reference.index((xp, yp))
				label += array[index]
			
			if label != self.__get_effective_label(x, y):
				return False

		return True


	def __get_effective_label(self, x, y):
		return int(self.__board[x][y]) - self.__get_num_marked_neighbor(x, y)


	def __get_num_marked_neighbor(self, x, y):
		marked = 0

		for xp, yp in self.__generate_neighbor(x, y):
			if self.__board[xp][yp] == 'f':
				marked += 1

		return marked


	def __build_froniter(self):
		self.__uncovered_frontier = set()
		self.__covered_frontier = set()

		if self.__frontier:
			x, y = self.__frontier.pop()
			self.__frontier.add( (x, y) )
			self.__uncovered_frontier.add( (x, y) )

			uncovered = {(x, y)}
			covered = True
			start_time = time.time()

			while (covered or uncovered) and (time.time() - start_time < 2):
				covered = set()
				for x, y in uncovered:
					covered.update(self.__get_covered_unmarked_neighbor(x, y))
				covered.difference_update(self.__covered_frontier)
				self.__covered_frontier.update(covered)

				uncovered = set()
				for x, y in covered:
					uncovered.update(self.__get_uncovered_neighbor(x, y))
				uncovered.difference_update(self.__uncovered_frontier)
				self.__uncovered_frontier.update(uncovered)


	def __get_uncovered_neighbor(self, x, y):
		uncovered = set()

		for xp, yp in self.__generate_neighbor(x, y):
			if (self.__board[xp][yp] not in ('f', '.')):
				uncovered.add( (xp, yp) )

		return uncovered


	def __get_covered_unmarked_neighbor(self, x, y):
		unmarked = set()

		for xp, yp in self.__generate_neighbor(x, y):
			if self.__check_covered_unmarked_tile(xp, yp):
				unmarked.add( (xp, yp) )

		return unmarked


	def __check_covered_unmarked_tile(self, x, y):
		if self.__board[x][y] == '.':
			return True

		return False


	def __generate_neighbor(self, x, y):
		for i in range(-1, 2):
			for j in range(-1, 2):
				xp, yp = x + i, y + j

				if (self.__check_bounds(xp, yp)) == True and (xp != x or yp != y):
					yield (xp, yp)


	def __check_bounds(self, x, y):
		if 0 <= x < self.__colD and 0 <= y < self.__rowD:
			return True

		return False


	def single_point_logic(self):
		for row, col in self.__frontier:
			unknown = set()
			a = 0			#all
			u = 0			#uncovered
			c = 0			#covered
			m = 0			#mine
			for xp, yp in self.__generate_neighbor(row, col):
					if self.__board[xp][yp] == '.':
						c += 1
						unknown.add( (xp, yp) )
					elif self.__board[xp][yp] == 'f':
						m += 1
					else:
						u += 1
					a += 1

			if str(m) == self.__board[row][col]:
				self.__safeCells.update(unknown)
			elif str(c + m) == self.__board[row][col]:
				while unknown:
					x, y = unknown.pop()
					self.__board[x][y] = 'f'
					self.__founded += 1
			if str(u + m) == str(a):
				self.__waitToDrop.add( (row, col) )

		for row, col in self.__waitToDrop:
			self.__frontier.discard( (row, col) )
		self.__waitToDrop.clear()

		if self.__safeCells:
			return self.__uncover_safe_tile()


	def check_complete(self):
		if self.__rowD * self.__colD - self.__uncovered == self.__totalMines:
			return True
		else:
			return False


######################################################################################
######################################################################################
######################################################################################
	def __updateACell(self, x, y, n):
		self.__board[x][y] = n
		self.__uncovered += 1


	def __uncover_safe_tile(self):
		self.__x, self.__y = self.__safeCells.pop()
		return Action(AI.Action.UNCOVER, self.__x, self.__y)


	def printBoard(self):
		for j in reversed(range(0, self.__rowD)):
			print(str(j + 1).ljust(2) + '|', end = ' ')
			for i in range(0, self.__colD):
				print(self.__board[i][j], end = '  ')
			print()

		column_label = "    "
		column_border = "   "
		for c in range(1, self.__colD + 1):
			column_border += "---"
			column_label += str(c).ljust(3)

		print(column_border)
		print(column_label + '\n')


	def print_frontier(self, frontier):
		for each in frontier:
			print((each[0] + 1, each[1] + 1), end = '	')
		print()

