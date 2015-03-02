# -*- coding: utf-8 -*-
# Copyright (c) 2015 Brad Newbold (wudan07 [at] gmail.com)
# See LICENSE for details.
# common.py
#
"""wIcon library:
	Common functions
"""

import math
import random
#import time
from PIL import Image
#from selection import selection_get
#from selection import SelCoord
#from wicon.handy import *
#from selection import *
#global values
oldFashioned = False
selsaveCrunch = False
#global imgobjs
#global selections
imgobjs = []
selections = []
stLumRange = 0

outputDebugMSGs = False


### These are really general functions I like to use a lot.
def file_exists(path):
	try:
		if path != "":
			out = open(path, 'r')
			if outputDebugMSGs is True:
				print "out.close file_exists"
			out.close()
			return True
	except EnvironmentError:
		if outputDebugMSGs is True:
			print("%s not readable!" % path)
		#out = open(path,'w')
		#		if(outputDebugMSGs is True):
		#				print "out.close file_exists"
		#out.close()
		return False
	return False


### These are really general functions I like to use a lot.
def str_match(name1, name2):
	if isinstance(name1, basestring) is False:
		return name1 == name2
	if isinstance(name2, basestring) is False:
		return name1 == name2
	if (name1 == name2) and (len(name1) == len(name2)):
		return True
	return False


def str_strip_whitespace(name):
		clen = str_strip_end(name, ' ')
		clen = str_strip_start(clen, ' ')
		if len(clen) < len(name):
				len_c = len(clen)
				len_o = len_c + 1
				while len_c < len_o:  # while it is getting smaller
						len_o = len(clen)
						clen = str_strip_end(clen, ' ')
						clen = str_strip_start(clen, ' ')
						len_c = len(clen)
				return clen
		return name


def str_strip_leadingzeroes(name):
		clen = str_strip_start(name, '0')
		if len(clen) < len(name):
				len_c = len(clen)
				len_o = len_c + 1
				while len_c < len_o:  # while it is getting smaller
						len_o = len(clen)
						clen = str_strip_start(clen, '0')
						len_c = len(clen)
				return clen
		return name


def str_strip_end(name, strip):
	if name[len(name)-len(strip):len(name)] == strip:
		return name[0:len(name)-len(strip)]
	return name


def str_strip_start(name, strip):
	if name[0:len(strip)] == strip:
		return name[len(strip):]
	return name


def str_strip_newline(name):
		line = str_strip_end(name, '\n')
		return str_strip_end(line, '\r')


def str_strip_part(name, part):
		vals = name.split(part)
		line = ''
		for val in vals:
				line += val
		return line


def str_match_end(name, strip):
	if name is None:
		return False
	if name[len(name)-len(strip):len(name)] == strip:
		return True
	return False


def str_match_start(name, strip):
	if name[:len(strip)] == strip:
		return True
	return False


def line_to_vars(line):
	""" Return
	"""
	peices = []
	vals = line.split('#')
	val = vals[0]
	vals = val.split('"')
	for i in range(0, len(vals)):
		item = str_strip_whitespace(vals[i])
		if i % 2:
			if len(item) > 0:
				peices.append(item)
		else:
			if len(item) > 0:
				items = item.split(' ')
				for j in items:
					if len(j) > 0:
						peices.append(j)
	return peices


def i_on_list(items, item):
	for obj in items:
		if item == obj:
			return True
	return False


def i_list_add(items, item):
	if i_on_list(items, item) is False:
		items.append(item)
		return True
	return False


def on_list(items, item):
	for obj in items:
		if str_match(item, obj) is True:
			return True
	return False


def list_add(items, item):
	if on_list(items, item) is False:
		items.append(item)
		return True  # add
	return False  # no add


def list_clean(items):
	while len(items) != 0:
		items.remove(items[0])


def list_copy(items):
	arry = []
	for item in items:
		arry.append(item)
	return arry


def list_to_str(items):
	mystr = ''
	for item in items:
		mystr += item
	return mystr


def list_append(dst, items):
	for item in items:
		dst.append(item)


#def removeSameFromTwoLists(list1, list2, term):
#	if on_list(list1, term) and on_list(list2, term):
#		list1.remove(term)
#		list2.remove(term)


def list_getlast(items):
		return items[len(items)-1]


class ImageObject:
	def __init__(self, name):
		self.name = name
		self.path = ''

	def set_path(self, path):
		if len(path) == 0:
			self.path = None
			print('imgObj \'%s\' set to \'%s\'' % (self.name, self.path))
			return
		self.path = path
		print('imgObj \'%s\' set to \'%s\'' % (self.name, self.path))


def imageobject_find(name):
	""" Return ImageObject from list imgobjs whose name matches, does not append to array
	"""
	global imgobjs
	for imo in imgobjs:
		if str_match(imo.name, name) is True:
			return imo
	return None


def imageobject_get(name):
	""" Return ImageObject from list imgobjs whose name matches, if not on list, creates new ImageObject and appends to array
	"""
	for imo in imgobjs:
		if str_match(imo.name, name) is True:
			return imo
	imo = ImageObject(name)
	imgobjs.append(imo)
	return imgobjs[len(imgobjs)-1]


def paint_smooth(target, actualpxl, box, color, smooth):
	""" Return
	"""
	#print 'paintSmooth'
	if actualpxl[0] < 0 or actualpxl[0] >= box[0] or actualpxl[1] < 0 or actualpxl[1] >= box[1]:
		return
	#print 'go go gadget paint'
	if smooth >= 1.0:
		if oldFashioned is True:
			target.putpixel((actualpxl[0], actualpxl[1]), (color[0], color[1], color[2]))
		else:
			target[actualpxl[0], actualpxl[1]] = (color[0], color[1], color[2])
	else:
		src_color = target.getpixel((actualpxl[0], actualpxl[1]))
		if src_color[0] == color[0] and src_color[1] == color[1] and src_color[2] == color[2]:
			return
		#print src_color
		#return
		dst_color = [int(float(color[0])*smooth), int(float(color[1])*smooth), int(float(color[2])*smooth)]
		res_color = [src_color[0]+dst_color[0], src_color[1]+dst_color[1], src_color[2]+dst_color[2]]

		#if res_color[0]>color[0]:
		#	res_color[0] = color[0]
		#if res_color[1]>color[1]:
		#	res_color[1] = color[1]
		#if res_color[2]>color[2]:
		#	res_color[2] = color[2]
		#respxl[0] = val_clamp(respxl[0], 0, 255)
		#respxl[1] = val_clamp(respxl[1], 0, 255)
		#respxl[2] = val_clamp(respxl[2], 0, 255)
		if oldFashioned is True:
			target.putpixel((actualpxl[0], actualpxl[1]), (int(res_color[0]), int(res_color[1]), int(res_color[2])))
		else:
			target[actualpxl[0], actualpxl[1]] = (res_color[0], res_color[1], res_color[2])


class CircleObject:
	def __init__(self, radius, feather):
		self.radius = float(radius)
		self.feather = feather
		self.blits = []
		sqsize = radius*2+1
		rsquared = radius * radius
		coords = []
		#i = 0
		#j = 0
		x_start = -radius
		y_start = radius
		for i in range(0, sqsize):
			coords.append([])
			for j in range(0, sqsize):
				#print i, j
				coords[i].append([])

		count = 0
		y_keep = y_start
		for pair in coords:
			x_keep = x_start
			for cor in pair:
				cor.append(x_keep)
				cor.append(y_keep)
				cor.append(1.0)
				#print cor
				x_keep += 1
				count += 1
			#print ''
			y_keep -= 1
		#print count

		for row in coords:
			for pair in row:
				sqlen = float(pair[0]*pair[0])+(pair[1]*pair[1])
				if sqlen <= rsquared:
					pair[2] = 1.0 - (float(sqlen))/rsquared
					pair[2] *= self.feather
					print('circle radius %f, coord %d %d, smooth %f' % (self.radius, pair[0], pair[1], pair[2]))
					self.blits.append(pair)

	def draw(self):
		print 'circle draw'

	def blit(self, target, coord, box, color):
		global oldFashioned
		#print 'circle blit'
		#print coord, box, color
		#print len(self.blits)
		#print self.blits
		for spot in self.blits:
			#print spot
			actualpxl = [spot[0]+coord[0], spot[1]+coord[1]]
			paint_smooth(target, actualpxl, box, color, spot[2])
			#paintSmooth(target,actualpxl,box,color,1.1)
			#if(actualpxl[0]>=0 and actualpxl[0]<box[0] and actualpxl[1]>=0 and actualpxl[1]<box[1]):
			#	#print actualpxl
			#	if(oldFashioned is True):
			#		target.putpixel((actualpxl[0],actualpxl[1]),(color[0],color[1],color[2]))
			#	else:
			#		target[actualpxl[0],actualpxl[1]] = (color[0],color[1],color[2])

	def selblit(self, tsel, cor):
		for spot in self.blits:
			actualpxl = [spot[0]+cor.xy[0], spot[1]+cor.xy[1]]
			actualclr = [cor.color[0], cor.color[1], cor.color[2], int(spot[2]*255.0)]
			sc = SelCoord(actualpxl, actualclr)
			tsel.coord_add(sc)


def getimagesize(srcpath):
	""" Returns PIL Image.size
	"""
	if file_exists(srcpath) is False:
		return None
	src = Image.open(srcpath)
	srcbox = src.size
	return srcbox


def color_match(col1, col2):
	""" Returns True if both colors are exact match
	"""
	matchint = 0
	if col1[0] == col2[0]:
		matchint += 1
	if col1[1] == col2[2]:
		matchint += 1
	if col1[1] == col2[2]:
		matchint += 1
	if matchint == 3:
		return True
	return False


def poslen(pos):
	""" Returns length of 2 length coords
	"""
	fpos = [float(pos[0]), float(pos[1])]
	plen = math.sqrt(fpos[0]*fpos[0] + fpos[1]*fpos[1])
	return plen


def color_match_threshold(pxl, ink, thresh):
	""" Returns True if both colors match, within threshhold
	"""
	diff = [0, 0, 0]
	diff[0] = abs(pxl[0] - ink[0])
	diff[1] = abs(pxl[1] - ink[1])
	diff[2] = abs(pxl[2] - ink[2])
	#print diff
	if(diff[0]+diff[1]+diff[2]) <= thresh:
		return True
	return False


#def setResultColor(res, r, g, b):
#	""" This does not appear to be a working function?
#	"""
#	res[0] = r
#	res[1] = g
#	res[2] = b


#def setRange(ran, bot, top):
#	""" This does not appear to be a working function?
#	"""
#	ran[0] = bot
#	ran[1] = top


def val_clamp(val, _min, _max):
	""" Returns val between _min and _max
	"""
	if val > _max:
		return _max
	if val < _min:
		return _min
	return val


def color_clamp(color):
	""" Returns a 3 value array using color as input, clamps range from 0 to 255
	"""
	res = [0, 0, 0]
	res[0] = val_clamp(color[0], 0, 255)
	res[1] = val_clamp(color[1], 0, 255)
	res[2] = val_clamp(color[2], 0, 255)
	return (res[0], res[1], res[2])


def random_inrange(_min, _max):
	""" Returns a random number between _min and _max (integer)
	"""
	return random.randint(_min, _max)


def all_true(trues):
	""" Return True if all values of list are True, else returns False
	"""
	for true in trues:
		if true is False:
			return False
	return True


def color_isblack(color):
	""" Returns True if all 3 values are less than 1, e.g. Black, else returns False
	"""
	if color[0] + color[1] + color[2] < 1:
		return True
	return False


def get_outimage():
	""" Return outfile path, searches for files that are out%04d.jpg
	"""
	media_ct = 0
	outimg = 'out%04d.jpg' % (media_ct+1)
	while file_exists(outimg) is True:
		outimg = 'out%04d.jpg' % (media_ct+1)
		if file_exists(outimg) is True:
			media_ct += 1
	return outimg


def file_is_image(path):
	""" Returns True if path ends in .jpg, .jpeg, or .png
	"""
	if path is None:
		return False
	if str_match_end(path.lower(), '.jpg') is True:
		return True
	if str_match_end(path.lower(), '.jpeg') is True:
		return True
	elif str_match_end(path.lower(), '.png') is True:
		return True
	return False