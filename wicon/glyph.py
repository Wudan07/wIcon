# -*- coding: utf-8 -*-
"""wIcon library:
	glyph provides GlyphObject
"""


##from handy import *
##from common import *


### represents a character in a glyphString
class GlyphObject:
	def __init__(self, glyph):
		### set to glyph value
		self.glyph = glyph
		### will be an array of pixels, unique to each glyph
		self.coords = []
		### will be an adjustment to the next characters starting point - I eyeballed this.  Sorry typographers!
		self.flash = 6
		if glyph == 'A':
			self.coords.append([0, 7])
			self.coords.append([0, 8])
			self.coords.append([1, 3])
			self.coords.append([1, 4])
			self.coords.append([1, 5])
			self.coords.append([1, 6])
			self.coords.append([2, 0])
			self.coords.append([2, 1])
			self.coords.append([2, 2])
			self.coords.append([2, 6])
			self.coords.append([3, 0])
			self.coords.append([3, 1])
			self.coords.append([3, 2])
			self.coords.append([3, 6])
			self.coords.append([4, 3])
			self.coords.append([4, 4])
			self.coords.append([4, 5])
			self.coords.append([4, 6])
			self.coords.append([5, 6])
			self.coords.append([5, 7])
			self.coords.append([5, 8])
			self.flash = 7

		elif glyph == 'a':
			self.coords.append([1, 3])
			self.coords.append([2, 3])
			self.coords.append([3, 3])
			self.coords.append([4, 3])
			self.coords.append([0, 4])
			self.coords.append([4, 4])
			self.coords.append([0, 5])
			self.coords.append([4, 5])
			self.coords.append([0, 6])
			self.coords.append([4, 6])
			self.coords.append([0, 7])
			self.coords.append([3, 7])
			self.coords.append([4, 7])
			self.coords.append([1, 8])
			self.coords.append([2, 8])
			self.coords.append([4, 8])
			self.flash = 6

		elif glyph == 'B':
			self.coords.append([0, 0])
			self.coords.append([0, 1])
			self.coords.append([0, 2])
			self.coords.append([0, 3])
			self.coords.append([0, 4])
			self.coords.append([0, 5])
			self.coords.append([0, 6])
			self.coords.append([0, 7])
			self.coords.append([0, 8])
			self.coords.append([1, 0])
			self.coords.append([1, 4])
			self.coords.append([1, 8])
			self.coords.append([2, 0])
			self.coords.append([2, 4])
			self.coords.append([2, 8])
			self.coords.append([3, 0])
			self.coords.append([3, 4])
			self.coords.append([3, 8])
			self.coords.append([4, 1])
			self.coords.append([4, 2])
			self.coords.append([4, 3])
			self.coords.append([4, 5])
			self.coords.append([4, 6])
			self.coords.append([4, 7])
			self.flash = 6

		elif glyph == 'b':
			self.coords.append([0, 0])
			self.coords.append([0, 1])
			self.coords.append([0, 2])
			self.coords.append([0, 3])
			self.coords.append([0, 4])
			self.coords.append([0, 5])
			self.coords.append([0, 6])
			self.coords.append([0, 7])
			self.coords.append([0, 8])
			self.coords.append([1, 4])
			self.coords.append([1, 8])
			self.coords.append([2, 3])
			self.coords.append([2, 8])
			self.coords.append([3, 3])
			self.coords.append([3, 8])
			self.coords.append([4, 4])
			self.coords.append([4, 5])
			self.coords.append([4, 6])
			self.coords.append([4, 7])
			self.flash = 6

		elif glyph == 'C':
			self.coords.append([0, 2])
			self.coords.append([0, 3])
			self.coords.append([0, 4])
			self.coords.append([0, 5])
			self.coords.append([0, 6])
			self.coords.append([1, 1])
			self.coords.append([1, 7])
			self.coords.append([2, 0])
			self.coords.append([2, 8])
			self.coords.append([3, 0])
			self.coords.append([3, 8])
			self.coords.append([4, 0])
			self.coords.append([4, 8])
			self.flash = 6

		elif glyph == 'c':
			self.coords.append([1, 3])
			self.coords.append([2, 3])
			self.coords.append([3, 3])
			self.coords.append([0, 4])
			self.coords.append([4, 4])
			self.coords.append([0, 5])
			self.coords.append([0, 6])
			self.coords.append([0, 7])
			self.coords.append([4, 7])
			self.coords.append([1, 8])
			self.coords.append([2, 8])
			self.coords.append([3, 8])
			self.flash = 6

		elif glyph == 'D':
			self.coords.append([0, 0])
			self.coords.append([0, 1])
			self.coords.append([0, 2])
			self.coords.append([0, 3])
			self.coords.append([0, 4])
			self.coords.append([0, 5])
			self.coords.append([0, 6])
			self.coords.append([0, 7])
			self.coords.append([0, 8])
			self.coords.append([1, 0])
			self.coords.append([1, 8])
			self.coords.append([2, 0])
			self.coords.append([2, 8])
			self.coords.append([3, 0])
			self.coords.append([3, 8])
			self.coords.append([4, 1])
			self.coords.append([4, 7])
			self.coords.append([5, 2])
			self.coords.append([5, 3])
			self.coords.append([5, 4])
			self.coords.append([5, 5])
			self.coords.append([5, 6])
			self.flash = 7

		elif glyph == 'd':
			self.coords.append([4, 0])
			self.coords.append([4, 1])
			self.coords.append([4, 2])
			self.coords.append([1, 3])
			self.coords.append([2, 3])
			self.coords.append([3, 3])
			self.coords.append([4, 3])
			self.coords.append([0, 4])
			self.coords.append([4, 4])
			self.coords.append([0, 5])
			self.coords.append([4, 5])
			self.coords.append([0, 6])
			self.coords.append([4, 6])
			self.coords.append([0, 7])
			self.coords.append([3, 7])
			self.coords.append([4, 7])
			self.coords.append([1, 8])
			self.coords.append([2, 8])
			self.coords.append([4, 8])
			self.flash = 6

		elif glyph == 'E':
			self.coords.append([0, 0])
			self.coords.append([0, 1])
			self.coords.append([0, 2])
			self.coords.append([0, 3])
			self.coords.append([0, 4])
			self.coords.append([0, 5])
			self.coords.append([0, 6])
			self.coords.append([0, 7])
			self.coords.append([0, 8])
			self.coords.append([1, 0])
			self.coords.append([1, 4])
			self.coords.append([1, 8])
			self.coords.append([2, 0])
			self.coords.append([2, 4])
			self.coords.append([2, 8])
			self.coords.append([3, 0])
			self.coords.append([3, 4])
			self.coords.append([3, 8])
			self.coords.append([4, 0])
			self.coords.append([4, 4])
			self.coords.append([4, 8])
			self.flash = 6

		elif glyph == 'e':
			self.coords.append([1, 3])
			self.coords.append([2, 3])
			self.coords.append([3, 3])
			self.coords.append([0, 4])
			self.coords.append([4, 4])
			self.coords.append([0, 5])
			self.coords.append([1, 5])
			self.coords.append([2, 5])
			self.coords.append([3, 5])
			self.coords.append([0, 6])
			self.coords.append([0, 7])
			self.coords.append([4, 7])
			self.coords.append([1, 8])
			self.coords.append([2, 8])
			self.coords.append([3, 8])
			self.flash = 6

		elif glyph == 'F':
			self.coords.append([0, 0])
			self.coords.append([0, 1])
			self.coords.append([0, 2])
			self.coords.append([0, 3])
			self.coords.append([0, 4])
			self.coords.append([0, 5])
			self.coords.append([0, 6])
			self.coords.append([0, 7])
			self.coords.append([0, 8])
			self.coords.append([1, 0])
			self.coords.append([1, 4])
			self.coords.append([2, 0])
			self.coords.append([2, 4])
			self.coords.append([3, 0])
			self.coords.append([3, 4])
			self.coords.append([4, 0])
			self.coords.append([4, 4])
			self.flash = 6

		elif glyph == 'f':
			self.coords.append([2, 1])
			self.coords.append([3, 1])
			self.coords.append([1, 2])
			self.coords.append([0, 3])
			self.coords.append([1, 3])
			self.coords.append([2, 3])
			self.coords.append([3, 3])
			self.coords.append([1, 4])
			self.coords.append([1, 5])
			self.coords.append([1, 6])
			self.coords.append([1, 7])
			self.coords.append([1, 8])
			self.flash = 5

		elif glyph == 'G':
			self.coords.append([0, 2])
			self.coords.append([0, 3])
			self.coords.append([0, 4])
			self.coords.append([0, 5])
			self.coords.append([0, 6])
			self.coords.append([1, 1])
			self.coords.append([1, 7])
			self.coords.append([2, 0])
			self.coords.append([2, 8])
			self.coords.append([3, 0])
			self.coords.append([3, 4])
			self.coords.append([3, 8])
			self.coords.append([4, 0])
			self.coords.append([4, 4])
			self.coords.append([4, 5])
			self.coords.append([4, 6])
			self.coords.append([4, 7])
			self.coords.append([4, 8])
			self.flash = 6

		elif glyph == 'g':
			self.coords.append([1, 3])
			self.coords.append([2, 3])
			self.coords.append([3, 3])
			self.coords.append([4, 3])
			self.coords.append([0, 4])
			self.coords.append([4, 4])
			self.coords.append([0, 5])
			self.coords.append([4, 5])
			self.coords.append([0, 6])
			self.coords.append([4, 6])
			self.coords.append([0, 7])
			self.coords.append([3, 7])
			self.coords.append([4, 7])
			self.coords.append([1, 8])
			self.coords.append([2, 8])
			self.coords.append([4, 8])
			self.coords.append([4, 9])
			self.coords.append([1, 10])
			self.coords.append([2, 10])
			self.coords.append([3, 10])
			self.flash = 6

		elif glyph == 'H':
			self.coords.append([0, 0])
			self.coords.append([0, 1])
			self.coords.append([0, 2])
			self.coords.append([0, 3])
			self.coords.append([0, 4])
			self.coords.append([0, 5])
			self.coords.append([0, 6])
			self.coords.append([0, 7])
			self.coords.append([0, 8])
			self.coords.append([1, 4])
			self.coords.append([2, 4])
			self.coords.append([3, 4])
			self.coords.append([4, 0])
			self.coords.append([4, 1])
			self.coords.append([4, 2])
			self.coords.append([4, 3])
			self.coords.append([4, 4])
			self.coords.append([4, 5])
			self.coords.append([4, 6])
			self.coords.append([4, 7])
			self.coords.append([4, 8])
			self.flash = 6

		elif glyph == 'h':
			self.coords.append([0, 0])
			self.coords.append([0, 1])
			self.coords.append([0, 2])
			self.coords.append([0, 3])
			self.coords.append([1, 3])
			self.coords.append([2, 3])
			self.coords.append([3, 3])
			self.coords.append([0, 4])
			self.coords.append([4, 4])
			self.coords.append([0, 5])
			self.coords.append([4, 5])
			self.coords.append([0, 6])
			self.coords.append([4, 6])
			self.coords.append([0, 7])
			self.coords.append([4, 7])
			self.coords.append([0, 8])
			self.coords.append([4, 8])
			self.flash = 6

		elif glyph == 'I':
			self.coords.append([0, 0])
			self.coords.append([0, 8])
			self.coords.append([1, 0])
			self.coords.append([1, 8])
			self.coords.append([2, 0])
			self.coords.append([2, 1])
			self.coords.append([2, 2])
			self.coords.append([2, 3])
			self.coords.append([2, 4])
			self.coords.append([2, 5])
			self.coords.append([2, 6])
			self.coords.append([2, 7])
			self.coords.append([2, 8])
			self.coords.append([3, 0])
			self.coords.append([3, 8])
			self.coords.append([4, 0])
			self.coords.append([4, 8])
			self.flash = 6

		elif glyph == 'i':
			self.coords.append([1, 1])
			self.coords.append([0, 3])
			self.coords.append([1, 3])
			self.coords.append([1, 4])
			self.coords.append([1, 5])
			self.coords.append([1, 6])
			self.coords.append([1, 7])
			self.coords.append([1, 8])
			self.coords.append([2, 8])
			self.flash = 4

		elif glyph == 'J':
			self.coords.append([0, 8])
			self.coords.append([1, 8])
			self.coords.append([2, 0])
			self.coords.append([2, 8])
			self.coords.append([3, 0])
			self.coords.append([3, 8])
			self.coords.append([4, 0])
			self.coords.append([4, 1])
			self.coords.append([4, 2])
			self.coords.append([4, 3])
			self.coords.append([4, 4])
			self.coords.append([4, 5])
			self.coords.append([4, 6])
			self.coords.append([4, 7])
			self.flash = 6

		elif glyph == 'j':
			self.coords.append([2, 1])
			self.coords.append([0, 3])
			self.coords.append([1, 3])
			self.coords.append([2, 3])
			self.coords.append([2, 4])
			self.coords.append([2, 5])
			self.coords.append([2, 6])
			self.coords.append([2, 7])
			self.coords.append([2, 8])
			self.coords.append([0, 9])
			self.coords.append([1, 9])
			self.flash = 4

		elif glyph == 'K':
			self.coords.append([0, 0])
			self.coords.append([0, 1])
			self.coords.append([0, 2])
			self.coords.append([0, 3])
			self.coords.append([0, 4])
			self.coords.append([0, 5])
			self.coords.append([0, 6])
			self.coords.append([0, 7])
			self.coords.append([0, 8])
			self.coords.append([1, 4])
			self.coords.append([2, 3])
			self.coords.append([2, 5])
			self.coords.append([3, 1])
			self.coords.append([3, 2])
			self.coords.append([3, 6])
			self.coords.append([4, 0])
			self.coords.append([4, 7])
			self.coords.append([5, 8])
			self.flash = 7

		elif glyph == 'k':
			self.coords.append([0, 0])
			self.coords.append([0, 1])
			self.coords.append([0, 2])
			self.coords.append([0, 3])
			self.coords.append([3, 3])
			self.coords.append([0, 4])
			self.coords.append([2, 4])
			self.coords.append([0, 5])
			self.coords.append([1, 5])
			self.coords.append([0, 6])
			self.coords.append([2, 6])
			self.coords.append([0, 7])
			self.coords.append([3, 7])
			self.coords.append([0, 8])
			self.coords.append([4, 8])
			self.flash = 6

		elif glyph == 'L':
			self.coords.append([0, 0])
			self.coords.append([0, 1])
			self.coords.append([0, 2])
			self.coords.append([0, 3])
			self.coords.append([0, 4])
			self.coords.append([0, 5])
			self.coords.append([0, 6])
			self.coords.append([0, 7])
			self.coords.append([0, 8])
			self.coords.append([1, 8])
			self.coords.append([2, 8])
			self.coords.append([3, 8])
			self.coords.append([4, 8])
			self.flash = 6

		elif glyph == 'l':
			self.coords.append([1, 1])
			self.coords.append([1, 2])
			self.coords.append([1, 3])
			self.coords.append([1, 4])
			self.coords.append([1, 5])
			self.coords.append([1, 6])
			self.coords.append([1, 7])
			self.coords.append([1, 8])
			self.coords.append([2, 8])
			self.flash = 4

		elif glyph == 'M':
			self.coords.append([0, 0])
			self.coords.append([0, 1])
			self.coords.append([0, 2])
			self.coords.append([0, 3])
			self.coords.append([0, 4])
			self.coords.append([0, 5])
			self.coords.append([0, 6])
			self.coords.append([0, 7])
			self.coords.append([0, 8])
			self.coords.append([1, 1])
			self.coords.append([1, 2])
			self.coords.append([1, 3])
			self.coords.append([2, 4])
			self.coords.append([2, 5])
			self.coords.append([2, 6])
			self.coords.append([3, 1])
			self.coords.append([3, 2])
			self.coords.append([3, 3])
			self.coords.append([4, 0])
			self.coords.append([4, 1])
			self.coords.append([4, 2])
			self.coords.append([4, 3])
			self.coords.append([4, 4])
			self.coords.append([4, 5])
			self.coords.append([4, 6])
			self.coords.append([4, 7])
			self.coords.append([4, 8])
			self.flash = 6

		elif glyph == 'm':
			self.coords.append([0, 3])
			self.coords.append([1, 3])
			self.coords.append([3, 3])
			self.coords.append([0, 4])
			self.coords.append([2, 4])
			self.coords.append([4, 4])
			self.coords.append([0, 5])
			self.coords.append([2, 5])
			self.coords.append([4, 5])
			self.coords.append([0, 6])
			self.coords.append([2, 6])
			self.coords.append([4, 6])
			self.coords.append([0, 7])
			self.coords.append([2, 7])
			self.coords.append([4, 7])
			self.coords.append([0, 8])
			self.coords.append([2, 8])
			self.coords.append([4, 8])
			self.flash = 6

		elif glyph == 'N':
			self.coords.append([0, 0])
			self.coords.append([0, 1])
			self.coords.append([0, 2])
			self.coords.append([0, 3])
			self.coords.append([0, 4])
			self.coords.append([0, 5])
			self.coords.append([0, 6])
			self.coords.append([0, 7])
			self.coords.append([0, 8])
			self.coords.append([1, 1])
			self.coords.append([1, 2])
			self.coords.append([2, 3])
			self.coords.append([2, 4])
			self.coords.append([2, 5])
			self.coords.append([3, 6])
			self.coords.append([3, 7])
			self.coords.append([4, 0])
			self.coords.append([4, 1])
			self.coords.append([4, 2])
			self.coords.append([4, 3])
			self.coords.append([4, 4])
			self.coords.append([4, 5])
			self.coords.append([4, 6])
			self.coords.append([4, 7])
			self.coords.append([4, 8])
			self.flash = 6

		elif glyph == 'n':
			self.coords.append([0, 3])
			self.coords.append([2, 3])
			self.coords.append([3, 3])
			self.coords.append([0, 4])
			self.coords.append([1, 4])
			self.coords.append([4, 4])
			self.coords.append([0, 5])
			self.coords.append([4, 5])
			self.coords.append([0, 6])
			self.coords.append([4, 6])
			self.coords.append([0, 7])
			self.coords.append([4, 7])
			self.coords.append([0, 8])
			self.coords.append([4, 8])
			self.flash = 6

		elif glyph == 'O':
			self.coords.append([0, 2])
			self.coords.append([0, 3])
			self.coords.append([0, 4])
			self.coords.append([0, 5])
			self.coords.append([0, 6])
			self.coords.append([1, 1])
			self.coords.append([1, 7])
			self.coords.append([2, 0])
			self.coords.append([2, 8])
			self.coords.append([3, 0])
			self.coords.append([3, 8])
			self.coords.append([4, 1])
			self.coords.append([4, 7])
			self.coords.append([5, 2])
			self.coords.append([5, 3])
			self.coords.append([5, 4])
			self.coords.append([5, 5])
			self.coords.append([5, 6])
			self.flash = 7

		elif glyph == 'o':
			self.coords.append([1, 3])
			self.coords.append([2, 3])
			self.coords.append([3, 3])
			self.coords.append([0, 4])
			self.coords.append([4, 4])
			self.coords.append([0, 5])
			self.coords.append([4, 5])
			self.coords.append([0, 6])
			self.coords.append([4, 6])
			self.coords.append([0, 7])
			self.coords.append([4, 7])
			self.coords.append([1, 8])
			self.coords.append([2, 8])
			self.coords.append([3, 8])
			self.flash = 6

		elif glyph == 'P':
			self.coords.append([0, 0])
			self.coords.append([0, 1])
			self.coords.append([0, 2])
			self.coords.append([0, 3])
			self.coords.append([0, 4])
			self.coords.append([0, 5])
			self.coords.append([0, 6])
			self.coords.append([0, 7])
			self.coords.append([0, 8])
			self.coords.append([1, 0])
			self.coords.append([1, 5])
			self.coords.append([2, 0])
			self.coords.append([2, 5])
			self.coords.append([3, 0])
			self.coords.append([3, 4])
			self.coords.append([4, 1])
			self.coords.append([4, 2])
			self.coords.append([4, 3])
			self.flash = 6

		elif glyph == 'p':
			self.coords.append([0, 3])
			self.coords.append([1, 3])
			self.coords.append([2, 3])
			self.coords.append([3, 3])
			self.coords.append([0, 4])
			self.coords.append([4, 4])
			self.coords.append([0, 5])
			self.coords.append([4, 5])
			self.coords.append([0, 6])
			self.coords.append([4, 6])
			self.coords.append([0, 7])
			self.coords.append([4, 7])
			self.coords.append([0, 8])
			self.coords.append([1, 8])
			self.coords.append([2, 8])
			self.coords.append([3, 8])
			self.coords.append([0, 9])
			self.coords.append([0, 10])
			self.flash = 6

		elif glyph == 'Q':
			self.coords.append([0, 2])
			self.coords.append([0, 3])
			self.coords.append([0, 4])
			self.coords.append([0, 5])
			self.coords.append([0, 6])
			self.coords.append([1, 1])
			self.coords.append([1, 7])
			self.coords.append([2, 0])
			self.coords.append([2, 8])
			self.coords.append([3, 0])
			self.coords.append([3, 8])
			self.coords.append([3, 9])
			self.coords.append([4, 1])
			self.coords.append([4, 7])
			self.coords.append([4, 10])
			self.coords.append([5, 2])
			self.coords.append([5, 3])
			self.coords.append([5, 4])
			self.coords.append([5, 5])
			self.coords.append([5, 6])
			self.coords.append([5, 10])
			self.coords.append([6, 10])
			self.flash = 7

		elif glyph == 'q':
			self.coords.append([1, 3])
			self.coords.append([2, 3])
			self.coords.append([3, 3])
			self.coords.append([4, 3])
			self.coords.append([0, 4])
			self.coords.append([4, 4])
			self.coords.append([0, 5])
			self.coords.append([4, 5])
			self.coords.append([0, 6])
			self.coords.append([4, 6])
			self.coords.append([0, 7])
			self.coords.append([3, 7])
			self.coords.append([4, 7])
			self.coords.append([1, 8])
			self.coords.append([2, 8])
			self.coords.append([4, 8])
			self.coords.append([4, 9])
			self.coords.append([4, 10])
			self.flash = 6

		elif glyph == 'R':
			self.coords.append([0, 0])
			self.coords.append([0, 1])
			self.coords.append([0, 2])
			self.coords.append([0, 3])
			self.coords.append([0, 4])
			self.coords.append([0, 5])
			self.coords.append([0, 6])
			self.coords.append([0, 7])
			self.coords.append([0, 8])
			self.coords.append([1, 0])
			self.coords.append([1, 4])
			self.coords.append([2, 0])
			self.coords.append([2, 4])
			self.coords.append([3, 0])
			self.coords.append([3, 3])
			self.coords.append([3, 5])
			self.coords.append([3, 6])
			self.coords.append([4, 1])
			self.coords.append([4, 2])
			self.coords.append([4, 7])
			self.coords.append([4, 8])
			self.flash = 6

		elif glyph == 'r':
			self.coords.append([0, 3])
			self.coords.append([1, 3])
			self.coords.append([3, 3])
			self.coords.append([4, 3])
			self.coords.append([1, 4])
			self.coords.append([2, 4])
			self.coords.append([1, 5])
			self.coords.append([1, 6])
			self.coords.append([1, 7])
			self.coords.append([0, 8])
			self.coords.append([1, 8])
			self.coords.append([2, 8])
			self.flash = 6

		elif glyph == 'S':
			self.coords.append([0, 1])
			self.coords.append([0, 2])
			self.coords.append([0, 3])
			self.coords.append([0, 8])
			self.coords.append([1, 0])
			self.coords.append([1, 4])
			self.coords.append([1, 8])
			self.coords.append([2, 0])
			self.coords.append([2, 4])
			self.coords.append([2, 8])
			self.coords.append([3, 0])
			self.coords.append([3, 5])
			self.coords.append([3, 8])
			self.coords.append([4, 6])
			self.coords.append([4, 7])
			self.flash = 6

		elif glyph == 's':
			self.coords.append([1, 3])
			self.coords.append([2, 3])
			self.coords.append([3, 3])
			self.coords.append([0, 4])
			self.coords.append([4, 4])
			self.coords.append([1, 5])
			self.coords.append([2, 5])
			self.coords.append([3, 6])
			self.coords.append([0, 7])
			self.coords.append([4, 7])
			self.coords.append([1, 8])
			self.coords.append([2, 8])
			self.coords.append([3, 8])
			self.flash = 6

		elif glyph == 'T':
			self.coords.append([0, 0])
			self.coords.append([1, 0])
			self.coords.append([2, 0])
			self.coords.append([3, 0])
			self.coords.append([3, 1])
			self.coords.append([3, 2])
			self.coords.append([3, 3])
			self.coords.append([3, 4])
			self.coords.append([3, 5])
			self.coords.append([3, 6])
			self.coords.append([3, 7])
			self.coords.append([3, 8])
			self.coords.append([4, 0])
			self.coords.append([5, 0])
			self.coords.append([6, 0])
			self.flash = 8

		elif glyph == 't':
			self.coords.append([1, 1])
			self.coords.append([1, 2])
			self.coords.append([0, 3])
			self.coords.append([1, 3])
			self.coords.append([2, 3])
			self.coords.append([3, 3])
			self.coords.append([1, 4])
			self.coords.append([1, 5])
			self.coords.append([1, 6])
			self.coords.append([1, 7])
			self.coords.append([4, 7])
			self.coords.append([2, 8])
			self.coords.append([3, 8])
			self.flash = 6

		elif glyph == 'U':
			self.coords.append([0, 0])
			self.coords.append([0, 1])
			self.coords.append([0, 2])
			self.coords.append([0, 3])
			self.coords.append([0, 4])
			self.coords.append([0, 5])
			self.coords.append([0, 6])
			self.coords.append([0, 7])
			self.coords.append([1, 8])
			self.coords.append([2, 8])
			self.coords.append([3, 8])
			self.coords.append([4, 0])
			self.coords.append([4, 1])
			self.coords.append([4, 2])
			self.coords.append([4, 3])
			self.coords.append([4, 4])
			self.coords.append([4, 5])
			self.coords.append([4, 6])
			self.coords.append([4, 7])
			self.flash = 6

		elif glyph == 'u':
			self.coords.append([0, 3])
			self.coords.append([4, 3])
			self.coords.append([0, 4])
			self.coords.append([4, 4])
			self.coords.append([0, 5])
			self.coords.append([4, 5])
			self.coords.append([0, 6])
			self.coords.append([4, 6])
			self.coords.append([0, 7])
			self.coords.append([3, 7])
			self.coords.append([4, 7])
			self.coords.append([1, 8])
			self.coords.append([2, 8])
			self.coords.append([4, 8])
			self.flash = 6

		elif glyph == 'V':
			self.coords.append([0, 0])
			self.coords.append([0, 1])
			self.coords.append([1, 2])
			self.coords.append([1, 3])
			self.coords.append([1, 4])
			self.coords.append([2, 5])
			self.coords.append([2, 6])
			self.coords.append([3, 7])
			self.coords.append([3, 8])
			self.coords.append([4, 4])
			self.coords.append([4, 5])
			self.coords.append([4, 6])
			self.coords.append([5, 1])
			self.coords.append([5, 2])
			self.coords.append([5, 3])
			self.coords.append([6, 0])
			self.flash = 8

		elif glyph == 'v':
			self.coords.append([0, 3])
			self.coords.append([4, 3])
			self.coords.append([0, 4])
			self.coords.append([4, 4])
			self.coords.append([1, 5])
			self.coords.append([3, 5])
			self.coords.append([1, 6])
			self.coords.append([3, 6])
			self.coords.append([2, 7])
			self.coords.append([2, 8])
			self.flash = 6

		elif glyph == 'W':
			self.coords.append([0, 0])
			self.coords.append([0, 1])
			self.coords.append([0, 2])
			self.coords.append([0, 3])
			self.coords.append([0, 4])
			self.coords.append([1, 5])
			self.coords.append([1, 6])
			self.coords.append([1, 7])
			self.coords.append([1, 8])
			self.coords.append([2, 3])
			self.coords.append([2, 4])
			self.coords.append([2, 5])
			self.coords.append([3, 0])
			self.coords.append([3, 1])
			self.coords.append([3, 2])
			self.coords.append([4, 3])
			self.coords.append([4, 4])
			self.coords.append([4, 5])
			self.coords.append([5, 5])
			self.coords.append([5, 6])
			self.coords.append([5, 7])
			self.coords.append([5, 8])
			self.coords.append([6, 0])
			self.coords.append([6, 1])
			self.coords.append([6, 2])
			self.coords.append([6, 3])
			self.coords.append([6, 4])
			self.flash = 8

		elif glyph == 'w':
			self.coords.append([0, 3])
			self.coords.append([4, 3])
			self.coords.append([0, 4])
			self.coords.append([4, 4])
			self.coords.append([0, 5])
			self.coords.append([2, 5])
			self.coords.append([4, 5])
			self.coords.append([0, 6])
			self.coords.append([2, 6])
			self.coords.append([4, 6])
			self.coords.append([1, 7])
			self.coords.append([3, 7])
			self.coords.append([1, 8])
			self.coords.append([3, 8])
			self.flash = 6

		elif glyph == 'X':
			self.coords.append([0, 0])
			self.coords.append([0, 7])
			self.coords.append([0, 8])
			self.coords.append([1, 1])
			self.coords.append([1, 2])
			self.coords.append([1, 5])
			self.coords.append([1, 6])
			self.coords.append([2, 3])
			self.coords.append([2, 4])
			self.coords.append([3, 1])
			self.coords.append([3, 2])
			self.coords.append([3, 5])
			self.coords.append([3, 6])
			self.coords.append([4, 0])
			self.coords.append([4, 7])
			self.coords.append([4, 8])
			self.flash = 6

		elif glyph == 'x':
			self.coords.append([0, 3])
			self.coords.append([4, 3])
			self.coords.append([1, 4])
			self.coords.append([3, 4])
			self.coords.append([2, 5])
			self.coords.append([2, 6])
			self.coords.append([1, 7])
			self.coords.append([3, 7])
			self.coords.append([0, 8])
			self.coords.append([4, 8])
			self.flash = 6

		elif glyph == 'Y':
			self.coords.append([0, 0])
			self.coords.append([0, 1])
			self.coords.append([1, 2])
			self.coords.append([1, 3])
			self.coords.append([2, 4])
			self.coords.append([2, 5])
			self.coords.append([2, 6])
			self.coords.append([2, 7])
			self.coords.append([2, 8])
			self.coords.append([3, 2])
			self.coords.append([3, 3])
			self.coords.append([4, 0])
			self.coords.append([4, 1])
			self.flash = 6

		elif glyph == 'y':
			self.coords.append([0, 3])
			self.coords.append([4, 3])
			self.coords.append([0, 4])
			self.coords.append([4, 4])
			self.coords.append([1, 5])
			self.coords.append([3, 5])
			self.coords.append([1, 6])
			self.coords.append([3, 6])
			self.coords.append([2, 7])
			self.coords.append([2, 8])
			self.coords.append([1, 9])
			self.coords.append([0, 10])
			self.flash = 6

		elif glyph == 'Z':
			self.coords.append([0, 0])
			self.coords.append([0, 7])
			self.coords.append([0, 8])
			self.coords.append([1, 0])
			self.coords.append([1, 5])
			self.coords.append([1, 6])
			self.coords.append([1, 8])
			self.coords.append([2, 0])
			self.coords.append([2, 4])
			self.coords.append([2, 8])
			self.coords.append([3, 0])
			self.coords.append([3, 2])
			self.coords.append([3, 3])
			self.coords.append([3, 8])
			self.coords.append([4, 0])
			self.coords.append([4, 1])
			self.coords.append([4, 8])
			self.flash = 6

		elif glyph == 'z':
			self.coords.append([0, 3])
			self.coords.append([1, 3])
			self.coords.append([2, 3])
			self.coords.append([3, 3])
			self.coords.append([4, 3])
			self.coords.append([3, 4])
			self.coords.append([2, 5])
			self.coords.append([1, 6])
			self.coords.append([0, 7])
			self.coords.append([0, 8])
			self.coords.append([1, 8])
			self.coords.append([2, 8])
			self.coords.append([3, 8])
			self.coords.append([4, 8])
			self.flash = 6

		elif glyph == '0':
			self.coords.append([1, 0])
			self.coords.append([2, 0])
			self.coords.append([3, 0])
			self.coords.append([0, 1])
			self.coords.append([4, 1])
			self.coords.append([0, 2])
			self.coords.append([4, 2])
			self.coords.append([0, 3])
			self.coords.append([3, 3])
			self.coords.append([4, 3])
			self.coords.append([0, 4])
			self.coords.append([2, 4])
			self.coords.append([4, 4])
			self.coords.append([0, 5])
			self.coords.append([1, 5])
			self.coords.append([4, 5])
			self.coords.append([0, 6])
			self.coords.append([4, 6])
			self.coords.append([0, 7])
			self.coords.append([4, 7])
			self.coords.append([1, 8])
			self.coords.append([2, 8])
			self.coords.append([3, 8])
			self.flash = 6

		elif glyph == '1':
			self.coords.append([2, 0])
			self.coords.append([1, 1])
			self.coords.append([2, 1])
			self.coords.append([0, 2])
			self.coords.append([2, 2])
			self.coords.append([2, 3])
			self.coords.append([2, 4])
			self.coords.append([2, 5])
			self.coords.append([2, 6])
			self.coords.append([2, 7])
			self.coords.append([0, 8])
			self.coords.append([1, 8])
			self.coords.append([2, 8])
			self.coords.append([3, 8])
			self.coords.append([4, 8])
			self.flash = 6

		elif glyph == '2':
			self.coords.append([1, 0])
			self.coords.append([2, 0])
			self.coords.append([3, 0])
			self.coords.append([0, 1])
			self.coords.append([4, 1])
			self.coords.append([4, 2])
			self.coords.append([4, 3])
			self.coords.append([3, 4])
			self.coords.append([2, 5])
			self.coords.append([1, 6])
			self.coords.append([0, 7])
			self.coords.append([0, 8])
			self.coords.append([1, 8])
			self.coords.append([2, 8])
			self.coords.append([3, 8])
			self.coords.append([4, 8])
			self.flash = 6

		elif glyph == '3':
			self.coords.append([1, 0])
			self.coords.append([2, 0])
			self.coords.append([3, 0])
			self.coords.append([0, 1])
			self.coords.append([4, 1])
			self.coords.append([4, 2])
			self.coords.append([4, 3])
			self.coords.append([2, 4])
			self.coords.append([3, 4])
			self.coords.append([4, 5])
			self.coords.append([4, 6])
			self.coords.append([0, 7])
			self.coords.append([4, 7])
			self.coords.append([1, 8])
			self.coords.append([2, 8])
			self.coords.append([3, 8])
			self.flash = 6

		elif glyph == '4':
			self.coords.append([1, 0])
			self.coords.append([3, 0])
			self.coords.append([1, 1])
			self.coords.append([3, 1])
			self.coords.append([0, 2])
			self.coords.append([3, 2])
			self.coords.append([0, 3])
			self.coords.append([3, 3])
			self.coords.append([0, 4])
			self.coords.append([1, 4])
			self.coords.append([2, 4])
			self.coords.append([3, 4])
			self.coords.append([4, 4])
			self.coords.append([3, 5])
			self.coords.append([3, 6])
			self.coords.append([3, 7])
			self.coords.append([3, 8])
			self.flash = 6

		elif glyph == '5':
			self.coords.append([0, 0])
			self.coords.append([1, 0])
			self.coords.append([2, 0])
			self.coords.append([3, 0])
			self.coords.append([4, 0])
			self.coords.append([0, 1])
			self.coords.append([0, 2])
			self.coords.append([0, 3])
			self.coords.append([1, 3])
			self.coords.append([2, 3])
			self.coords.append([3, 3])
			self.coords.append([0, 4])
			self.coords.append([4, 4])
			self.coords.append([4, 5])
			self.coords.append([4, 6])
			self.coords.append([4, 7])
			self.coords.append([0, 8])
			self.coords.append([1, 8])
			self.coords.append([2, 8])
			self.coords.append([3, 8])
			self.flash = 6

		elif glyph == '6':
			self.coords.append([2, 0])
			self.coords.append([3, 0])
			self.coords.append([1, 1])
			self.coords.append([0, 2])
			self.coords.append([0, 3])
			self.coords.append([1, 3])
			self.coords.append([2, 3])
			self.coords.append([3, 3])
			self.coords.append([0, 4])
			self.coords.append([4, 4])
			self.coords.append([0, 5])
			self.coords.append([4, 5])
			self.coords.append([0, 6])
			self.coords.append([4, 6])
			self.coords.append([0, 7])
			self.coords.append([4, 7])
			self.coords.append([1, 8])
			self.coords.append([2, 8])
			self.coords.append([3, 8])
			self.flash = 6

		elif glyph == '7':
			self.coords.append([0, 0])
			self.coords.append([1, 0])
			self.coords.append([2, 0])
			self.coords.append([3, 0])
			self.coords.append([4, 0])
			self.coords.append([5, 0])
			self.coords.append([0, 1])
			self.coords.append([5, 1])
			self.coords.append([5, 2])
			self.coords.append([4, 3])
			self.coords.append([4, 4])
			self.coords.append([3, 5])
			self.coords.append([3, 6])
			self.coords.append([2, 7])
			self.coords.append([2, 8])
			self.flash = 7

		elif glyph == '8':
			self.coords.append([1, 0])
			self.coords.append([2, 0])
			self.coords.append([3, 0])
			self.coords.append([0, 1])
			self.coords.append([4, 1])
			self.coords.append([0, 2])
			self.coords.append([4, 2])
			self.coords.append([1, 3])
			self.coords.append([2, 3])
			self.coords.append([3, 3])
			self.coords.append([0, 4])
			self.coords.append([4, 4])
			self.coords.append([0, 5])
			self.coords.append([4, 5])
			self.coords.append([0, 6])
			self.coords.append([4, 6])
			self.coords.append([0, 7])
			self.coords.append([4, 7])
			self.coords.append([1, 8])
			self.coords.append([2, 8])
			self.coords.append([3, 8])
			self.flash = 6

		elif glyph == '9':
			self.coords.append([1, 0])
			self.coords.append([2, 0])
			self.coords.append([3, 0])
			self.coords.append([0, 1])
			self.coords.append([4, 1])
			self.coords.append([0, 2])
			self.coords.append([4, 2])
			self.coords.append([0, 3])
			self.coords.append([4, 3])
			self.coords.append([1, 4])
			self.coords.append([2, 4])
			self.coords.append([3, 4])
			self.coords.append([4, 4])
			self.coords.append([0, 4])
			self.coords.append([4, 4])
			self.coords.append([4, 5])
			self.coords.append([4, 6])
			self.coords.append([3, 7])
			self.coords.append([1, 8])
			self.coords.append([2, 8])
			self.flash = 6

		elif glyph == '-':
			self.coords.append([0, 4])
			self.coords.append([1, 4])
			self.coords.append([2, 4])
			self.coords.append([3, 4])
			self.flash = 6

		elif glyph == '.':
			self.coords.append([0, 7])
			self.coords.append([1, 7])
			self.coords.append([0, 8])
			self.coords.append([1, 8])
			self.flash = 4

		elif glyph == '!':
			self.coords.append([0, 0])
			self.coords.append([1, 0])
			self.coords.append([0, 1])
			self.coords.append([1, 1])
			self.coords.append([0, 2])
			self.coords.append([1, 2])
			self.coords.append([0, 3])
			self.coords.append([1, 3])
			self.coords.append([0, 4])
			self.coords.append([1, 4])
			self.coords.append([0, 5])
			self.coords.append([1, 5])
			self.coords.append([0, 7])
			self.coords.append([1, 7])
			self.coords.append([0, 8])
			self.coords.append([1, 8])
			self.flash = 4

		elif glyph == ',':
			self.coords.append([0, 7])
			self.coords.append([1, 7])
			self.coords.append([0, 8])
			self.coords.append([1, 8])
			self.coords.append([1, 9])
			self.coords.append([0, 10])
			self.flash = 4

		elif glyph == '\'':
			self.coords.append([0, 0])
			self.coords.append([1, 0])
			self.coords.append([0, 1])
			self.coords.append([1, 1])
			self.coords.append([1, 2])
			self.flash = 4

		elif glyph == '"':
			self.coords.append([0, 0])
			self.coords.append([0, 1])
			self.coords.append([0, 2])
			self.coords.append([2, 0])
			self.coords.append([2, 1])
			self.coords.append([2, 2])
			self.flash = 4

		elif glyph == ' ':
			self.flash = 6

		elif glyph == '\t':
			self.flash = 24

		elif glyph == '(':
			self.coords.append([2, 0])
			self.coords.append([1, 1])
			self.coords.append([0, 2])
			self.coords.append([0, 3])
			self.coords.append([0, 4])
			self.coords.append([0, 5])
			self.coords.append([0, 6])
			self.coords.append([0, 7])
			self.coords.append([0, 8])
			self.coords.append([1, 9])
			self.coords.append([2, 10])
			self.flash = 6

		elif glyph == ')':
			self.coords.append([0, 0])
			self.coords.append([1, 1])
			self.coords.append([2, 2])
			self.coords.append([2, 3])
			self.coords.append([2, 4])
			self.coords.append([2, 5])
			self.coords.append([2, 6])
			self.coords.append([2, 7])
			self.coords.append([2, 8])
			self.coords.append([1, 9])
			self.coords.append([0, 10])
			self.flash = 6

		elif glyph == ')':
			self.coords.append([0, 0])
			self.coords.append([1, 1])
			self.coords.append([2, 2])
			self.coords.append([2, 3])
			self.coords.append([2, 4])
			self.coords.append([2, 5])
			self.coords.append([2, 6])
			self.coords.append([2, 7])
			self.coords.append([2, 8])
			self.coords.append([1, 9])
			self.coords.append([0, 10])
			self.flash = 6

		elif glyph == ':':
			self.coords.append([0, 3])
			self.coords.append([1, 3])
			self.coords.append([0, 4])
			self.coords.append([1, 4])
			self.coords.append([0, 7])
			self.coords.append([1, 7])
			self.coords.append([0, 8])
			self.coords.append([1, 8])
			self.flash = 5

		elif glyph == ';':
			self.coords.append([0, 3])
			self.coords.append([1, 3])
			self.coords.append([0, 4])
			self.coords.append([1, 4])
			self.coords.append([0, 7])
			self.coords.append([1, 7])
			self.coords.append([1, 8])
			self.coords.append([0, 9])
			self.flash = 5

		elif glyph == '_':
			self.coords.append([0, 8])
			self.coords.append([1, 8])
			self.coords.append([2, 8])
			self.coords.append([3, 8])
			self.coords.append([4, 8])
			self.coords.append([5, 8])
			self.flash = 7

		else:
			self.flash = 6

	def center(self, wide=6):
		glwide = self.flash - 2
		adjust = (wide-glwide)/2
		for cor in self.coords:
			cor[0] += adjust
		self._flash(wide+2)

	def _flash(self, flash):
		self.flash = flash


def glyphstr_length(gls):
	""" Returns length of glyphstr gls
	"""
	length = 0
	for gl in gls:
		length += gl.flash
	return length - 2


def glyphstr_monospace(gls, wide=6):
	""" for each GlyphObject in gls, calls .center(wide)
	"""
	for gl in gls:
		gl.center(wide)


def glyphstr_center(gls, width=100):
	""" given a width of an area (such as column heading width) it will adjust the start point of each glyph in a glyphstr_, centering the string
	"""
	length = glyphstr_length(gls)
	glen = len(gls)
	#addlen = (width-length)/(glen))
	print length
	print width - length
	hl = (width-length)/2
	for i in range(0, glen):
		gl = gls[i]
		flash = gl.flash
		gl._flash(flash+hl)


def glyphstr_justify(gls, width=100):
	""" given a width of an area (such as column heading width) it will adjust the start point of each glyph in a glyphstr_, justifying the string
	"""
	length = glyphstr_length(gls)
	glen = len(gls)
	#addlen = (width-length)/(glen))
	print length
	print width - length
	ct = 0
	for i in range(0, width-length):
		if ct >= glen-1:
			ct = 0
		gl = gls[ct]
		flash = gl.flash
		gl._flash(flash+1)
		ct += 1


def glyphstr_bounds_get(string, mono=False):
	""" Returns 2 len integer array, size and height of string as glyphstr_
	"""
	#xk = 0
	#yk = 0
	xz = 0
	#yz = 10
	vals = string.split('\n')
	yz = len(vals) * 10
	for val in vals:
		gs = glyphstr_get(val)
		if mono:
			glyphstr_monospace(gs)
		sz = glyphstr_length(gs)
		if sz > xz:
			xz = sz
	return [xz, yz]


def glyphstr_get(string):
	""" given a string, Returns glyphs, a list of glyphs
	"""
	glyphs = []
	i = 0
	while i < len(string):
		letter = string[i:i+1]
		glyphs.append(GlyphObject(letter))
		i += 1
	return glyphs
