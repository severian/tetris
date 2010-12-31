from numpy import rot90

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