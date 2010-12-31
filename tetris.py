import board, block, clock
from numpy import array
		
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
			
		board = board.Board(50, 50)
		block = block.Block(board, array([[1, 1], [0, 1], [0, 1]]))
		
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