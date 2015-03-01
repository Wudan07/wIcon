#!/c/Python27/python.exe

import sys
from wicon.q_math import *
from wicon.selection import selection_get
from wicon.raster import BlitMatrix, RasterObject

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

	# initialize selectionObject - think of this as a canvas
	my_selection = selection_get('flatland')
	bm = BlitMatrix('flatland')
	ro = RasterObject(bm)


	vN1 = VectorCopy([0.0, 0.0, 1.0])

	for i in range(0, 5):
		ofs = [16.0 * float(i), 16.0 * float(i)]
		v1 = VectorCopy([0.0+ofs[0], 0.0+ofs[1], 0.0])
		v2 = VectorCopy([0.0+ofs[0], 32.0+ofs[1], 0.0])
		v3 = VectorCopy([32.0+ofs[0], 0.0+ofs[1], 0.0])
		ro.add_triangle(v1, v2, v3, vN1, vN1, vN1)

	ro.blit_grunt_work()

	my_selection.save('output_test_03.png', None, tuple(colors_array[COLOR_BLACK]))
	my_selection.wipe()
	return 1

if __name__ == '__main__':
	sys.exit(main(sys.argv[1:]))
