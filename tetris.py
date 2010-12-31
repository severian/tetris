from numpy import array, matrix, rot90, zeros, int16
import clock

COUNTERCLOCKWISE = matrix([[0, -1], [1, 0]])
CLOCKWISE = matrix([[0, 1], [-1, 0]])

def rotate_point(point, clockwise=True):
	rotate_matrix = CLOCKWISE if clockwise else COUNTERCLOCKWISE
	rotated = rotate_matrix * matrix([[point[0]], [point[1]]])
	return [rotated[0, 0], rotated[1, 0]]

class Board(object):
	def __init__(self, width, height):
		self.width = width
		self.height = height
		self.board = zeros((width, height), dtype=int16)
		
	def hit_test(self, shape, pos, block_id):
		row_index = 0
		for row in shape:
			col_index = 0
			for val in row:
				x = pos[0] + row_index
				y = pos[1] + col_index
				
				if (x < 0 or x >= self.width or y < 0 or y >= self.height):
					return True
				
				board_val = self.board[x, y]
				if val and board_val and board_val != block_id:
					return True
				col_index += 1
			
			row_index += 1
		
		return False
		
	def shape_at(self, x, y):
		return self.board[x, y]
		
	def add_shape(self, shape, pos, block_id):
		row_index = 0
		for row in shape:
			col_index = 0
			for val in row:
				x = pos[0] + row_index
				y = pos[1] + col_index
				if val:
					self.board[x, y] = block_id
				col_index += 1
			
			row_index += 1
		
	def remove_shape(self, shape, pos):
		row_index = 0
		for row in shape:
			col_index = 0
			for val in row:
				x = pos[0] + row_index
				y = pos[1] + col_index
				if val:
					self.board[x, y] = 0
				col_index += 1
			
			row_index += 1
	
	def dump(self, f):
		for x in xrange(self.width):
			for y in xrange(self.height):
				if self.shape_at(x, y):
					f.write("#")
				else:
					f.write(" ")
			f.write("\n")

def get_block_id():
	Block.block_id += 1
	return Block.block_id

class Block(object):
	block_id = 0
	
	def __init__(self, board, shape):
		self.id = get_block_id()
		self.pos = [0, 0]
		self.board = board
		self.shape = shape
		self.shapes = (shape, rot90(shape), rot90(rot90(shape)), rot90(rot90(rot90(shape))))
		self.shape_index = 0
		self.board.add_shape(self.shape, self.pos, self.id)
		
	def rotate(self, clockwise=True):
		new_index = (self.shape_index - 1 if clockwise else self.shape_index + 1) % 4
		new_shape = self.shapes[new_index]
		
		if self.mutate(new_shape, self.pos):
			self.shape_index = new_index
			
	def translate(self, direction="down"):
		new_pos = list(self.pos)
		if direction == "down":
			new_pos[0] += 1
		elif direction == "up":
			new_pos[0] -= 1
		elif direction == "left":
			new_pos[1] -= 1
		elif direction == "right":
			new_pos[1] += 1
			
		self.mutate(self.shape, new_pos)
			
	def mutate(self, new_shape, new_pos):
		if not self.board.hit_test(new_shape, new_pos, self.id):
			self.board.remove_shape(self.shape, self.pos)
			self.board.add_shape(new_shape, new_pos, self.id)
			self.shape = new_shape
			self.pos = new_pos
			return True
		
		return False
		
if __name__ == "__main__":
	# provide a simple curses based client
	import curses, sys
	screen = curses.initscr()
	curses.noecho()
	screen.keypad(1)
	
	directions = { curses.KEY_DOWN: "down", curses.KEY_LEFT: "left", curses.KEY_RIGHT: "right" }
	try:
		down_delay = 1 # seconds
		board_clock = clock.Clock(down_delay)
			
		board = Board(50, 50)
		block = Block(board, array([[1, 1], [0, 1], [0, 1]]))
		
		#board.dump(sys.stdout)
		while 1:
			if (board_clock.time_elapsed() >= down_delay):
				block.translate("down")
				board_clock.tick()
				
			for x in xrange(52):
				for y in xrange(52):
					if (x == 0 or y == 0 or x == 51 or y == 51):
						screen.addch(x, y, "*")
					elif board.shape_at(x - 1, y - 1):
						screen.addch(x, y, "#")
					else:
						screen.addch(x, y, " ")
			
			# (h, w) = screen.getmaxyx()
			# screen.addstr(0, 0, "%d, %d" % (w, h))
			screen.refresh()
			curses.halfdelay(max(int(board_clock.time_remaining() * 10), 1))
			ch = screen.getch()
			if ch == 0x20:
				block.rotate()
			elif ch in directions:
				block.translate(directions[ch])
			
	finally:
		curses.nocbreak()
		screen.keypad(0)
		curses.echo()
		curses.endwin()