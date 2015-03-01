#!/c/Python27/python.exe

import sys
from wicon.selection import selection_get
from random import randrange


def main(argv):
	i = 0
	while i < len(argv):
		arg = argv[i]
		i += 1

	my_selection = selection_get('main')
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
	#xkeep = 5
	xjump = 1
	#ykeep = 5
	yjump = 1
	blocksize = 8
	streak_length = 128
	num_streaks = 32
	pos = [0, 0]
	for i in range(0, num_streaks):
		pos[0] = blocksize + randrange(477)
		pos[1] = blocksize + randrange(477)
		cnum = randrange(len(colors_array)-1)
		#cnum = len(colors_array) -1
		xkeep = pos[0]
		ykeep = pos[1]
		szkeep = blocksize
		for j in range(0, streak_length):
			#print '%d %d' % (xkeep,ykeep)
			my_selection.block([xkeep-(szkeep+1), ykeep-(szkeep+1)], [szkeep*2+3, szkeep*2+3], 0.0, [255, 255, 255])
			xkeep += xjump
			ykeep += yjump
			if j % 16 == 0:
				szkeep -= 1

		xkeep = pos[0]
		ykeep = pos[1]
		szkeep = blocksize
		for j in range(0, streak_length):
			#print '%d %d' % (xkeep,ykeep)
			my_selection.mark([xkeep, ykeep], szkeep, colors_array[cnum])
			xkeep += xjump
			ykeep += yjump
			if j % 16 == 0:
				szkeep -= 1

	my_selection.save('output_test_01.png', [512, 512], tuple([96, 160, 192]))
	my_selection.wipe()
	return 1

if __name__ == '__main__':
	sys.exit(main(sys.argv[1:]))
