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
from PIL import Image, PngImagePlugin, JpegImagePlugin
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


def poslen(pos):
	""" Returns length of 2 length coords
	"""
	fpos = [float(pos[0]), float(pos[1])]
	plen = math.sqrt(fpos[0]*fpos[0] + fpos[1]*fpos[1])
	return plen


def val_clamp(val, _min, _max):
	""" Returns val between _min and _max
	"""
	if val > _max:
		return _max
	if val < _min:
		return _min
	return val


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
