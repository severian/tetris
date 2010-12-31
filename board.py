from numpy import array, matrix, rot90, zeros, int16

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