#!/c/Python27/python.exe

import sys
from wicon.selection import selection_get
from random import randrange

COLOR_RED = 0
COLOR_ORANGE = 1
COLOR_YELLOW = 2
COLOR_GREEN = 3
COLOR_BLUE = 4
COLOR_INDIGO = 5
COLOR_VIOLET = 6
COLOR_BLACK = 7
COLOR_WHITE = 8


def main(argv):
	i = 0
	while i < len(argv):
		arg = argv[i]
		i += 1

	# initialize selectionObject - think of this as a canvas
	my_selection = selection_get('flatland')

	alpha = 64
	colors_array = []
	colors_array.append([255, 0, 0, alpha])        # RED
	colors_array.append([255, 165, 0, alpha])      # ORANGE
	colors_array.append([255, 255, 0, alpha])      # YELLOW
	colors_array.append([0, 128, 0, alpha])        # GREEN
	colors_array.append([0, 0, 255, alpha])        # BLUE
	colors_array.append([75, 0, 130, alpha])       # INDIGO
	colors_array.append([238, 130, 238, alpha])    # VIOLET
	colors_array.append([0, 0, 0, 255])            # BLACK
	colors_array.append([255, 255, 255, 255])      # WHITE

	xkeep = 5
	xjump = 1
	ykeep = 5
	yjump = 1
	blocksize = 8
	streak_length = 64
	num_streaks = 16
	pos = [0, 0]
	for i in range(0, num_streaks):
		pos[0] = randrange(640) - 128
		pos[1] = randrange(640) - 128
		#cnum = randrange(len(colors_array)-2)
		cnum = COLOR_INDIGO

		xkeep = pos[0]
		ykeep = pos[1]
		print pos
		szkeep = blocksize
		endpos = [pos[0] + streak_length, pos[1] + streak_length]
		print endpos
		for j in range(0, 32):
			pos[0] += 1
			#startpos = [xkeep+j,ykeep]
			endpos[0] += 1
			my_selection.line(pos, endpos, colors_array[cnum])
	my_selection.save('output_test_02.png', [512, 512], tuple(colors_array[COLOR_BLACK]))
	my_selection.wipe()
	return 1

if __name__ == '__main__':
	sys.exit(main(sys.argv[1:]))
