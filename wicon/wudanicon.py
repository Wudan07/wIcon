# -*- coding: utf-8 -*-
# Copyright (c) 2015 Brad Newbold (wudan07 [at] gmail.com)
# See LICENSE for details.
# wudanicon.py
#
"""wIcon library:
	many functions being moved from here to sub-functions
"""

#import sys
#import getopt
#import math
#import random
#import gzip
#from PIL import Image
#from handy import *
#from common import *
from image_utils import *
from selection import *
from glyph import glyphstr_get, glyphstr_monospace, glyphstr_length
#from q_math import *


def skoo_filler_colors(colors):
	""" Return
	"""
	colen = len(colors)
	trues = []
	for i in range(0, colen):
		print i
		trues.append(False)
	
	i = 0
	while all_true(trues) is False:
		dobac = True
		dofor = True
		if i >= colen:
			i = 0
		color = colors[i]
		if trues[i] is False:
			if color_isblack(color) is True:
				if i < 1:
					dobac = False
				if i >= colen - 1:
					dofor = False
				if dobac is True:
					if color_isblack(colors[i-1]) is False:
						colors[i][0] = colors[i-1][0]
						colors[i][1] = colors[i-1][1]
						colors[i][2] = colors[i-1][2]
						trues[i] = color_isblack(colors[i])
				if dofor is True and trues[i] is False:
					if color_isblack(colors[i+1]) is False:
						colors[i][0] = colors[i+1][0]
						colors[i][1] = colors[i+1][1]
						colors[i][2] = colors[i+1][2]
						trues[i] = color_isblack(colors[i])
			else:
				trues[i] = True
		print i
		i += 1
	print 'ok filled colors!'


def xmatch(coord, mark):
	""" Return
	"""
	if coord[0] > mark[0]+1 or coord[0] < mark[0]-1:
		return False
	if coord[1] > mark[1]+1 or coord[1] < mark[1]-1:
		return False
	if coord[0] == mark[0] and coord[1] == mark[1]:
		return True
	if coord[0] == mark[0]-1 and coord[1] == mark[1]-1:
		return True
	if coord[0] == mark[0]+1 and coord[1] == mark[1]-1:
		return True
	if coord[0] == mark[0]-1 and coord[1] == mark[1]+1:
		return True
	if coord[0] == mark[0]+1 and coord[1] == mark[1]+1:
		return True
	return False


def max_size(image, _max_sz, method=3):
	""" im = max_size(im, (_max_szX, _max_szY), method = Image.BICUBIC)

	Resizes a PIL image to a _maximum size specified while maintaining
	the aspect ratio of the image.  Similar to Image.thumbnail(), but allows
	usage of different resizing methods and does NOT modify the image in
	place."""
	
	im_aspect = float(image.size[0])/float(image.size[1])
	out_aspect = float(_max_sz[0])/float(_max_sz[1])
	
	if im_aspect >= out_aspect:
		#set to _maxWidth x _maxWidth/im_aspect
		return image.resize((_max_sz[0], int((float(_max_sz[0])/im_aspect) + 0.5)), method)
	else:
		#set to _maxHeight*im_aspect x _maxHeight
		return image.resize((int((float(_max_sz[1])*im_aspect) + 0.5), _max_sz[1]), method)


def dump_imagesize(path):
	""" Return
	"""
	src = Image.open(path)
	return src.size


def tiny_dot(sel, x, y, color=None):
	""" Return
	"""
	if color is None:
		color = [0, 0, 0, 255]
	ImageOperation('seladdmark %s %d %d %d %d %d %d 0' % (sel, x, y, color[0], color[1], color[2], color[3]))


def adddot(selection, coord, color=None, mark=0):
	if color is None:
		color = [64, 64, 64, 128]
	ImageOperation('seladdmark %s %d %d %d %d %d %d %d' % (selection, coord[0], coord[1], color[0], color[1], color[2], color[3], mark))


def addline(selection, v1, v2, color=None):
	if color is None:
		color = [64, 64, 64, 128]
	#global fScale
	#scale = fScale / 2.0
	#global xc, yc, zc
	v3 = vec2sub(v2, v1)
	#v3[zc] = 0.0
	vlen = vec2len(v3)
	segs = int(vlen*8.0)
	#if(segs<5):
	#	segs = 5
	if segs == 0:
		return
	v4 = vec2scale(v3, 1.0/float(segs))
	adddot(selection, v1, color)
	v3 = vec2copy(v1)
	for i in range(0, segs):
		v3 = vec2add(v3, v4)
		#print '(%s) dot %s' % (selection, color)
		adddot(selection, v3, color)


def addpolygon(selection, verts, color=None):
	if color is None:
		color = [64, 64, 64, 128]
	if len(verts) < 2:
		return
	lv = verts[0]
	#cv = verts[0]
	for i in range(1, len(verts)):
		cv = verts[i]
		#print '(%s) line %s - %s (%s)' % (selection, lv, cv, color)
		addline(selection, vec2copy(lv), vec2copy(cv), color)
		lv = verts[i]
	cv = verts[0]
	addline(selection, vec2copy(lv), vec2copy(cv), color)


def draw_letter(sel, glyph, pos, color=None, dr=None, rev=None):
	""" Return
	"""
	if color is None:
		color = [0, 0, 0, 255]
	if dr is None:
		dr = [0, 1]
	if rev is None:
		rev = [1, 1]
	x = pos[dr[0]]
	y = pos[dr[1]]
	
	if rev[0] == 1 and rev[1] == -1:
		for cor in glyph.coords:
			tiny_dot(sel, x+cor[dr[0]], y-cor[dr[1]], color)
		return glyph.flash
	elif rev[0] == -1 and rev[1] == -1:
		for cor in glyph.coords:
			tiny_dot(sel, x-cor[dr[0]], y-cor[dr[1]], color)
		return glyph.flash
	elif rev[0] == -1 and rev[1] == 1:
		for cor in glyph.coords:
			tiny_dot(sel, x-cor[dr[0]], y+cor[dr[1]], color)
		return glyph.flash
	for cor in glyph.coords:
		tiny_dot(sel, x+cor[dr[0]], y+cor[dr[1]], color)
	return glyph.flash


def draw_string(sel, _str, pos, color=None, mono=False):
	""" Return
	"""
	if color is None:
		color = [0, 0, 0, 255]
	#xk = pos[0]
	yk = pos[1]
	vals = _str.split('\n')
	for val in vals:
		xk = pos[0]
		gs = glyphstr_get(val)
		if mono is False:
			pass
			#glyphStringJustify(gs, 360)
			#glyphStringCenter(gs, 360)
		if mono:
			glyphstr_monospace(gs)
		for gl in gs:
			xk += draw_letter(sel, gl, [xk, yk], color)  # [0, 1], [1, 1] )
		yk += 10


def string_box(a, mono=False):
	""" Return
	"""
	#xk = 0
	#yk = 0
	xz = 0
	#yz = 10
	print a
	vals = a.split('\n')
	yz = len(vals) * 10
	for val in vals:
		gs = glyphstr_get(val)
		if mono:
			glyphstr_monospace(gs)
		sz = glyphstr_length(gs)
		if sz > xz:
			xz = sz
	return [xz, yz]
		

def text_block(sel, val, pos, color=None, bgcolor=None, margin=None, radius=0.0, mono=False):
	""" Return
	"""
	if color is None:
		color = [0, 0, 0, 255]
	if bgcolor is None:
		bgcolor = [236, 233, 216, 192]
	if margin is None:
		margin = [5, 5]
	print 'textblock %s' % pos
	box = string_box(val, mono)
	box[0] += margin[0]
	box[1] += margin[1]
	bpos = [pos[0]-(box[0]/2), pos[1]-(box[1]/2)]
	transpos = [0, 0]
	selobj = selection_get(sel)
	selbounds = selobj.getbounds()
	if selbounds is None:
		return
	try:
		bpos[0] += selbounds[0][0]
		bpos[1] += selbounds[1][1] + 3
	except:
		return
	if bgcolor[3] > 0:
			ImageOperation('selblock %s %d %d %d %d %d %d %d %d %f' % (sel, bpos[0], bpos[1], box[0], box[1], bgcolor[0], bgcolor[1], bgcolor[2], bgcolor[3], radius))
	if color[3] > 0:
			draw_string(sel, val, [bpos[0]+margin[0]/2, bpos[1]+margin[1]/2], color, mono)

_TYPE_String = 0
_TYPE_Integer = 1
_TYPE_Float = 2


class VariableObject():
	def __init__(self, a):
		self.type = _TYPE_String
		negative = False
		if str_match_start(a, '-'):
			negative = True
		c = str_strip_start(a, '-')
		self.val = a

		found = False
		if c.isdigit() is True:
			self.type = _TYPE_Integer
			if negative is False:
				self.val = int(c)
			else:
				self.val = -int(c)
			found = True
		else:
			b = c.split('.')
			if len(b) == 2:
				if b[0].isdigit() and b[1].isdigit():
					self.type = _TYPE_Float
					if negative is False:
						self.val = float(c)
					else:
						self.val = -float(c)
					found = True
		if found is False:
			pass

	def __str__(self):
		if self.type == _TYPE_String:
			return '%s' % self.val
		elif self.type == _TYPE_Integer:
			return '%d' % self.val
		elif self.type == _TYPE_Float:
			return '%f' % self.val

	def __int__(self):
		if self.type == _TYPE_Integer:
			return self.val
		elif self.type == _TYPE_Float:
			return int(self.val)
		else:
			return None

	def isnumeric(self):
		if self.type == _TYPE_Float or self.type == _TYPE_Integer:
			return True
		return False

	def isstring(self):
		if self.type == _TYPE_String:
			return True
		return False


def selobj_retrieve_data(selname):
	data = []

	mysel = selection_find(selname)
	if mysel is None:
		return data

	sz = getselsize(selname)

	for j in range(0, sz[1]):
		data.append([])
		for i in range(0, sz[0]):
			data[j].append(None)

	for sc in mysel.coords:
		valid = True
		for i in range(0, 2):
			if sc.xy[i] < 0:
				valid = False
			elif sc.xy[i] >= sz[i]:
				valid = False
			if valid is True:
				data[sc.xy[1]][sc.xy[0]] = sc.color
	return data


class ImageOperation():
	def __init__(self, line):
		items = line_to_vars(line)
		self.peices = []
		for item in items:
			vo = VariableObject(item)
			self.peices.append(vo)

		cmdstr = ''
		for peice in self.peices:
			cmdstr += str(peice) + ' '
		#print 'ImageOperation: %s' % cmdstr

		found = False
		command = self.peices[0]
		if command.isstring():
			cstr = str(command).lower()
			if str_match(cstr, 'setobj') is True:
				self.op_setobj()
				found = True
			elif str_match(cstr, 'noise') is True:
				self.op_noise()
				found = True
			elif str_match(cstr, 'bleach') is True:
				self.op_bleach()
				found = True
			elif str_match(cstr, 'greyscale') is True:
				self.op_greyscale()
				found = True
			elif str_match(cstr, 'tone') is True:
				self.op_tone()
				found = True
			elif str_match(cstr, 'scotch') is True:
				self.op_scotch()
				found = True
			elif str_match(cstr, 'skoo') is True:
				self.op_skoo()
				found = True
			elif str_match(cstr, 'funkyfresh') is True:
				self.op_funkyfresh()
				found = True
			elif str_match(cstr, 'rotate') is True:
				self.op_rotate()
				found = True
			elif str_match(cstr, 'resize') is True:
				self.op_resize()
				found = True
			elif str_match(cstr, 'add') is True:
				self.op_add()
				found = True
			elif str_match(cstr, 'subtract') is True:
				self.op_subtract()
				found = True
			elif str_match(cstr, 'multiply') is True:
				self.op_multiply()
				found = True
			elif str_match(cstr, 'grid') is True:
				self.op_grid()
				found = True
			elif str_match(cstr, 'xmark') is True:
				self.op_xmark()
				found = True
			elif str_match(cstr, 'zoom') is True:
				self.op_zoom()
				found = True
			elif str_match(cstr, 'selset') is True:
				self.op_selset()
				found = True
			elif str_match(cstr, 'selappend') is True:
				self.op_selappend()
				found = True
			elif str_match(cstr, 'seladdmark') is True:
				self.op_seladdmark()
				found = True
			elif str_match(cstr, 'selgrid') is True:
				self.op_selgrid()
				found = True
			elif str_match(cstr, 'selwipe') is True:
				self.op_selwipe()
				found = True
			elif str_match(cstr, 'selremovecolor') is True:
				self.op_selremovecolor()
				found = True
			elif str_match(cstr, 'selbounds') is True:
				self.op_selbounds()
				found = True
			elif str_match(cstr, 'selrotate') is True:
				self.op_selrotate()
				found = True
			elif str_match(cstr, 'selsquare') is True:
				self.op_selsquare()
				found = True
			elif str_match(cstr, 'selblock') is True:
				self.op_selblock()
				found = True
			elif str_match(cstr, 'sellumrange') is True:
				self.op_sellumrange()
				found = True
			elif str_match(cstr, 'selcrop') is True:
				self.op_selcrop()
				found = True
			elif str_match(cstr, 'selbloom') is True:
				self.op_selbloom()
				found = True
			elif str_match(cstr, 'selsave') is True:
				self.op_selsave()
				found = True
		if found is False:
			print 'You have an error in your syntax, "%s"' % self.peices_to_str()

	def peices_to_str(self):
		line = ''
		for peice in self.peices:
			line += '%s ' % peice
		return str_strip_end(line, ' ')

	def get_peice(self, num, _asrt=None):
		"""
			retrieve peices num of type _assrt

		"""
		if len(self.peices) > num:
			if _asrt is None:
				return self.peices[num].val
			else:
				if self.peices[num].type == _asrt:
					return self.peices[num].val
				else:
					print 'SEEK TYPE %d, FOUND %d' % (_asrt, self.peices[num].type)
		return None

	def op_setobj(self):
		"""
			function needs self.peices to contain 2 strings,
			one is name of image_object,
			the second is the value it will be set to.
		"""
		imo_src = None
		srcpath = None
		dstpath = None

		if len(self.peices) >= 2:
			if self.peices[1].isstring():
				srcpath = self.peices[1].val
		if len(self.peices) >= 3:
			if self.peices[2].isstring():
				dstpath = self.peices[2].val

		if srcpath is None:
			print 'ERROR: op_setobj - srcpath is None COMMAND: %s' % self.peices_to_str()
			return
		if dstpath is None:
			print 'ERROR: op_setobj - dstpath is None COMMAND: %s' % self.peices_to_str()
			return

		if file_is_image(srcpath) is not True:
			imo_src = imageobject_get(srcpath)
			srcpath = imo_src.path

		if file_is_image(dstpath) is not True:
			imo_dst = imageobject_get(dstpath)
			dstpath = imo_dst.path

		if len(dstpath) == 0:
			print 'ERROR: op_setobj - dst image path is empty!'
			return

		if imo_src is not None:
			imo_src.set_path(dstpath)

	def op_noise(self):
		""" Return
		"""
		image_keep = None
		#imo_src = None

		try:
			imgpath = self.peices[1]
		except:
			imgpath = ''
		try:
			noiseval = float(self.peices[2])
		except:
			noiseval = 0.5
		try:
			targval = self.peices[3]
		except:
			targval = 'default'

		if file_is_image(imgpath) is not True:
			imo_src = imageobject_get(imgpath)
			srcpath = imo_src.path
		else:
			srcpath = imgpath

		if len(srcpath) == 0:
			print 'src image path is empty!'
			return

		src = Image.open(srcpath)
		srcbox = src.size

		if file_is_image(targval) is not True:
			image_keep = imageobject_get(targval)
			target = image_keep.path
		else:
			target = targval
		if len(target) == 0:
			target = None

		result = add_noise(src, srcbox, noiseval, target)
		if image_keep is not None:
			image_keep.set_path(result)

	def op_bleach(self):
		""" Return
		"""
		image_keep = None
		imo_src = None

		try:
			imgpath = self.peices[1]
		except:
			imgpath = ''
		try:
			bleachval = float(self.peices[2])
		except:
			bleachval = 0.5
		try:
			targval = self.peices[3]
		except:
			targval = 'default'

		if file_is_image(imgpath) is not True:
			imo_src = imageobject_get(imgpath)
			srcpath = imo_src.path
		else:
			srcpath = imgpath

		if len(srcpath) == 0:
			print 'src image path is empty!'
			return
		src = Image.open(srcpath)
		srcbox = src.size

		if file_is_image(targval) is not True:
			image_keep = imageobject_get(targval)
			target = image_keep.path
		else:
			target = targval
		if len(target) == 0:
			target = None

		result = image_bleach(src, srcbox, bleachval, target)
		if image_keep is not None:
			image_keep.set_path(result)

	def op_greyscale(self):
		"""
			needs to have at least one string in peices[1]
			converts it to greyscale using image_greyscale
		"""
		image_keep = None
		imo_src = None
		imgpath = ''
		targval = 'default'

		if len(self.peices) >= 2:
			if self.peices[1].isstring():
				imgpath = self.peices[1].val
		if len(self.peices) >= 3:
			if self.peices[2].isstring():
				targval = self.peices[2].val

		if file_is_image(imgpath) is not True:
			imo_src = imageobject_get(imgpath)
			srcpath = imo_src.path
		else:
			srcpath = imgpath

		if len(srcpath) == 0:
			print 'ERROR: op_greyscale - src image path is empty!'
			return
		src = Image.open(srcpath)
		srcbox = src.size

		if file_is_image(targval) is not True:
			image_keep = imageobject_get(targval)
			target = image_keep.path
		else:
			target = targval

		if len(target) == 0:
			target = None

		result = image_greyscale(src, srcbox, target)
		if image_keep is not None:
			image_keep.set_path(result)

	def op_tone(self):
		""" Return
		"""
		image_keep = None
		imo_src = None
		color = [0, 0, 0]

		try:
			imgpath = self.peices[1]
		except:
			imgpath = ''
		try:
			bleachval = float(self.peices[2])
		except:
			bleachval = 0.5
		try:
			color[0] = float(self.peices[3])
		except:
			color[0] = 0.5
		try:
			color[1] = float(self.peices[4])
		except:
			color[1] = 1.0
		try:
			color[2] = float(self.peices[5])
		except:
			color[2] = 1.0
		try:
			targval = self.peices[6]
		except:
			targval = 'default'

		if file_is_image(imgpath) is not True:
			imo_src = imageobject_get(imgpath)
			srcpath = imo_src.path
		else:
			srcpath = imgpath

		if len(srcpath) == 0:
			print 'src image path is empty!'
			return
		src = Image.open(srcpath)
		srcbox = src.size

		if file_is_image(targval) is not True:
			image_keep = imageobject_get(targval)
			target = image_keep.path
		else:
			target = targval
		if len(target) == 0:
			target = None

		result = image_tone_apply(src, srcbox, bleachval, color, target)
		if image_keep is not None:
			image_keep.set_path(result)


	def op_scotch(self):
		""" Return
		"""
		image_keep = None
		imo_src = None
		color = [0, 0, 0]

		try:
			imgpath = self.peices[1]
		except:
			imgpath = ''
		#try:
		#	bleachval = float(self.peices[2])
		#except:
		#	bleachval = float(255)
		try:
			color[0] = float(self.peices[2])
		except:
			color[0] = 0.5
		try:
			color[1] = float(self.peices[3])
		except:
			color[1] = 1.0
		try:
			color[2] = float(self.peices[4])
		except:
			color[2] = 1.0
		try:
			targval = self.peices[5]
		except:
			targval = 'default'

		#bsqrd = bleachval * bleachval
		#targetlen = math.sqrt(bsqrd+bsqrd+bsqrd)
		#lumilen = math.sqrt(color[0]*color[0]+color[1]*color[1]+color[2]+color[2])
		#color[0] = (color[0]/lumilen)*targetlen
		#color[1] = (color[1]/lumilen)*targetlen
		#color[2] = (color[2]/lumilen)*targetlen

		if file_is_image(imgpath) is not True:
			imo_src = imageobject_get(imgpath)
			srcpath = imo_src.path
		else:
			srcpath = imgpath

		if len(srcpath) == 0:
			print 'src image path is empty!'
			return
		src = Image.open(srcpath)
		srcbox = src.size

		if file_is_image(targval) is not True:
			image_keep = imageobject_get(targval)
			target = image_keep.path
		else:
			target = targval
		if len(target) == 0:
			target = None

		result = image_scotch_apply(src, srcbox, color, target)
		if image_keep is not None:
			image_keep.set_path(result)


	def op_skoo(self):
		""" Return
		"""
		imo_col = None
		imo_src = None
		imo_dst = None
		colors = []

		try:
			colpath = self.peices[1]
		except:
			colpath = ''
		try:
			numslice = int(self.peices[2])
		except:
			numslice = 4
		try:
			imgpath = self.peices[3]
		except:
			imgpath = ''
		try:
			dstpath = self.peices[4]
		except:
			dstpath = 'default'

		if file_is_image(imgpath) is not True:
			imo_src = imageobject_get(imgpath)
			srcpath = imo_src.path
		else:
			srcpath = imgpath

		if file_is_image(colpath) is not True:
			imo_col = imageobject_get(colpath)
			colpath = imo_col.path

		if file_is_image(dstpath) is not True:
			imo_dst = imageobject_get(dstpath)
			dstpath = imo_dst.path
		#bsqrd = bleachval * bleachval
		#targetlen = math.sqrt(bsqrd+bsqrd+bsqrd)
		#lumilen = math.sqrt(color[0]*color[0]+color[1]*color[1]+color[2]+color[2])
		#color[0] = (color[0]/lumilen)*targetlen
		#color[1] = (color[1]/lumilen)*targetlen
		#color[2] = (color[2]/lumilen)*targetlen

		src = Image.open(colpath)
		srcbox = src.size
		colorCounts = []
		ranges = []
		slice_sz = int(256 / numslice)
		for i in range(0, numslice):
			ranges.append([])
		for j in range(0, srcbox[1]):
			for i in range(0, srcbox[0]):
				srcpxl = src.getpixel((i, j))
				gr_val = int(srcpxl[0]*0.3 + srcpxl[1]*0.59 + srcpxl[2]*0.11)
				k = get_skoo_range(gr_val, slice_sz)
				ranges[k].append(srcpxl)
		j = 0
		for ran in ranges:
			count = len(ran)
			color = [0, 0, 0]
			for item in ran:
				for i in range(0, 3):
					color[i] += item[i]
			for i in range(0, 3):
				if count > 0:
					color[i] /= count
				else:
					color[i] = 0
					print('color count %d is %d' % (j, count))
					#if j != 0:
					#	color[i] = colors[j-1][i]
					#else:
					#	color[i] = 0
			print color
			colors.append(color)
			j += 1
		skoo_filler_colors(colors)

		src = Image.open(srcpath)
		srcbox = src.size
		result = image_skoo_apply(src, srcbox, colors, slice_sz, None)
		if imo_dst is not None:
			imo_dst.set_path(result)


	def op_funkyfresh(self):
		""" Return
		"""
		image_keep = None
		#imo_src = None
		#color = [0, 0, 0]

		try:
			imgpath = self.peices[1]
		except:
			imgpath = ''
		try:
			targval = self.peices[2]
		except:
			targval = 'default'

		power = 256

		srcbox = [power, power]
		white = Image.new('RGB', srcbox, (0, 0, 0))

		if file_is_image(imgpath) is not True:
			imo_src = imageobject_get(imgpath)
			srcpath = imo_src.path
		else:
			srcpath = imgpath

		if file_is_image(targval) is not True:
			image_keep = imageobject_get(targval)
			target = image_keep.path
		else:
			target = targval
		if len(target) == 0:
			target = None

		funky_color_blocks = False

		if funky_color_blocks is True:
			#i = 0
			#j = 0
			wide = 256
			half = srcbox[0]/2
			block = int(half/wide)

			#grad = 0.0
			flw = float(wide)
			for i in range(0, wide):
				for j in range(0, wide):
					gri = float(i)/flw
					grj = float(j)/flw
					#print('%d, %d = %2.4f  %2.4f' % (i, j, gri, grj))
					color_block(white, [i*block+0, j*block+0], 	  [block, block], (gri*255.0, grj*255.0, 0))
					color_block(white, [i*block+half, j*block+0], [block, block], (gri*255.0, 0, grj*255.0))
					color_block(white, [i*block+0, j*block+half], [block, block], (0, gri*255.0, grj*255.0))
					color_block(white, [i*block+half, j*block+half], [block, block], (gri+grj*255.0, gri+grj*255.0, gri+grj*255.0))
					#(src, start, size, color):

		src = Image.open(srcpath)
		srcbox = src.size
		#colorCounts = []
		print srcbox
		ranges = []
		for i in range(0, 8):
			ranges.append([])
		for j in range(0, srcbox[1]):
			for i in range(0, srcbox[0]):
		#for j in range(0, 32):
		#	for i in range(0, 32):
				srcpxl = src.getpixel((i, j))
				gr_val = int(srcpxl[0]*0.3 + srcpxl[1]*0.59 + srcpxl[2]*0.11)
				#print gr_val
				k = 0
				while gr_val > 32:
					gr_val -= 32
					k += 1
				#print('%d - %d' % (gr_val, k))
				ranges[k].append(srcpxl)

		for ran in ranges:
			count = len(ran)
			color = [0, 0, 0]
			for item in ran:
				for i in range(0, 3):
					color[i] += item[i]
			if count > 0:
				for i in range(0, 3):
					color[i] /= count
			else:
				color = [0, 0, 0]
			print('pro_minent color in range is %d %d %d\n' % (color[0], color[1], color[2]))
		#print len(colorCounts)
		#for clr in colorCounts:
		#	print('%d, %d %d %d' % (clr.total(), clr.color[0], clr.color[1], clr.color[2]))

		if 0:
			media_ct = 0
			outimg = None
			if outimg is None:
				outimg = 'out%04d.png' % (media_ct+1)
				while file_exists(outimg) is True:
					outimg = 'out%04d.png' % (media_ct+1)
					if file_exists(outimg) is True:
						media_ct += 1
				print outimg

			white.save(outimg)
			if image_keep is not None:
				image_keep.set_path(outimg)
			return outimg

	def op_rotate(self):
		""" Return
		"""
		#imo_add = None
		#imo_src = None
		imo_res = None
		#power = 0

		try:
			imgpath = self.peices[1]
		except:
			imgpath = ''
		try:
			power = float(self.peices[2])
		except:
			power = 0.0
		try:
			targval = self.peices[3]
		except:
			targval = 'default'

		if file_is_image(imgpath) is not True:
			imo_src = imageobject_get(imgpath)
			srcpath = imo_src.path
		else:
			srcpath = imgpath

		if file_is_image(targval) is not True:
			imo_res = imageobject_get(targval)
			target = imo_res.path
		else:
			target = targval
		if len(target) == 0:
			target = None

		src = Image.open(srcpath)
		srcbox = src.size
		#white = Image.new('RGB', srcbox, (0, 0, 0))
		white = src.rotate(power, Image.BICUBIC, True)
		#whitebox = white.size
		#if _miniscule(power) is False:
		#	white = white.crop((1, 1, whitebox[0], whitebox[1]))
		print power
		#white.rotate(power, Image.BICUBIC)

		funky_color_blocks = False

		if funky_color_blocks is True:
			#i = 0
			#j = 0
			wide = srcbox[0]
			high = srcbox[1]
			#half = srcbox[0]/2
			#block = int(half/wide)

			#grad = 0.0
			#flw = float(wide)
			for i in range(0, wide):
				for j in range(0, high):

					if xmatch([i, j], power) is True:
						add_pixel(white, (i, j), (255, 255, 255))
					else:
						srcpxl = src.getpixel((i, j))
						add_pixel(white, (i, j), srcpxl)
					#(src, start, size, color):

		media_ct = 0
		outimg = target
		if outimg is None:
			outimg = 'out%04d.png' % (media_ct+1)
			while file_exists(outimg) is True:
				outimg = 'out%04d.png' % (media_ct+1)
				if file_exists(outimg) is True:
					media_ct += 1
			print outimg

		white.save(outimg)
		if imo_res is not None:
			imo_res.set_path(outimg)
		return outimg

	def op_resize(self):
		""" options are [-i ImagePath] [-w imageWidth] [-h imageHeight] [-o outpath] [-m resizeMode]
		"""
		#imo_add = None
		#imo_src = None
		imo_res = None
		#power = 0
		imgpath = None
		targval = None
		wide_val = None
		high_val = None
		mode_val = None
		mode = Image.ANTIALIAS

		i = 0
		while i < len(self.peices):
			if str_match(self.peices[i], '-i'):
				imgpath = self.peices[i+1]
				i += 1
			elif str_match(self.peices[i], '-w'):
				wide_val = int(self.peices[i+1])
				i += 1
			elif str_match(self.peices[i], '-h'):
				high_val = int(self.peices[i+1])
				i += 1
			elif str_match(self.peices[i], '-o'):
				targval = self.peices[i+1]
				i += 1
			elif str_match(self.peices[i], '-m'):
				mode_val = self.peices[i+1]
				i += 1
			i += 1

		if imgpath is None:
			print 'no image path in peices(%s)' % self.peices
			return None

		if wide_val is None and high_val is None:
			print 'resize: no width or height values supplied, no resize!'
			return None

		if mode_val is not None:
			if str_match(mode_val, 'antialias'):
				mode = Image.ANTIALIAS
			elif str_match(mode_val, 'bicubic'):
				mode = Image.BICUBIC
			elif str_match(mode_val, 'bilinear'):
				mode = Image.BILINEAR
			elif str_match(mode_val, 'nearest'):
				mode = Image.NEAREST

		if file_is_image(imgpath) is not True:
			imo_src = imageobject_get(imgpath)
			srcpath = imo_src.path
		else:
			srcpath = imgpath

		if file_is_image(targval) is not True:
			imo_res = imageobject_get(targval)
			target = imo_res.path
		else:
			target = targval
		if len(target) == 0:
			target = None

		src = Image.open(srcpath)
		srcbox = src.size
		white = None
		#white = Image.new('RGB', srcbox, (0, 0, 0))
		#white = src.resize((wide_val, high_val), Image.BICUBIC)
		if wide_val is not None and high_val is not None:
			white = max_size(src, [wide_val, high_val], mode)
		else:
			if wide_val is not None:
				im_aspect = float(srcbox[1])/float(srcbox[0])
				high_val = int(float(wide_val) * im_aspect)
				white = max_size(src, [wide_val, high_val], mode)
			elif high_val is not None:
				im_aspect = float(srcbox[0])/float(srcbox[1])
				wide_val = int(float(high_val) * im_aspect)
				white = max_size(src, [wide_val, high_val], mode)

		media_ct = 0
		outimg = target
		if outimg is None:
			outimg = 'out%04d.png' % (media_ct+1)
			while file_exists(outimg) is True:
				outimg = 'out%04d.png' % (media_ct+1)
				if file_exists(outimg) is True:
					media_ct += 1
			print outimg

		if white is not None:
			white.save(outimg)
		if imo_res is not None:
			imo_res.set_path(outimg)
		return outimg

	def op_add(self):
		""" Return
		"""
		imo_add = None
		imo_src = None
		imo_res = None
		#print peices

		try:
			srcpath = self.peices[1]
		except:
			srcpath = ''
		try:
			dstpath = self.peices[2]
		except:
			dstpath = ''
		try:
			feather = float(self.peices[3])
		except:
			feather = 0.5
		try:
			target = self.peices[4]
		except:
			target = 'default'

		if file_is_image(srcpath) is not True:
			imo_src = imageobject_get(srcpath)
			srcpath = imo_src.path

		if file_is_image(dstpath) is not True:
			imo_dst = imageobject_get(dstpath)
			dstpath = imo_dst.path

		if len(srcpath) == 0:
			print '%s: src image path is empty!' % (self.peices[0])
			return

		if len(dstpath) == 0:
			print '%s: dst image path is empty!' % (self.peices[0])
			return

		src = Image.open(srcpath)
		srcbox = src.size
		dst = Image.open(dstpath)
		dstbox = dst.size
		print 'check!'

		if file_is_image(target) is not True:
			imo_res = imageobject_get(target)
			target = imo_res.path
		if len(target) == 0:
			target = None

		print srcbox
		print dstbox
		result = image_add(src, srcbox, dst, dstbox, feather, False, target)
		if imo_res is not None:
			if result is not None:
				imo_res.set_path(result)


	def op_subtract(self):
		""" Return
		"""
		imo_add = None
		imo_src = None
		imo_res = None

		try:
			srcpath = self.peices[1]
		except:
			srcpath = ''
		try:
			dstpath = self.peices[2]
		except:
			dstpath = ''
		try:
			feather = float(self.peices[3])
		except:
			feather = 0.5
		try:
			target = self.peices[4]
		except:
			target = 'default'

		if file_is_image(srcpath) is not True:
			imo_src = imageobject_get(srcpath)
			srcpath = imo_src.path

		if file_is_image(dstpath) is not True:
			imo_dst = imageobject_get(dstpath)
			dstpath = imo_dst.path

		if len(srcpath) == 0:
			print '%s: src image path is empty!' % (self.peices[0])
			return

		if len(dstpath) == 0:
			print '%s: dst image path is empty!' % (self.peices[0])
			return
		src = Image.open(srcpath)
		srcbox = src.size
		dst = Image.open(dstpath)
		dstbox = dst.size

		if file_is_image(target) is not True:
			imo_res = imageobject_get(target)
			target = imo_res.path
		if len(target) == 0:
			target = None

		result = image_subtract(src, srcbox, dst, dstbox, feather, target)
		if imo_res is not None:
			imo_res.set_path(result)


	def op_multiply(self):
		""" Return
		"""
		#imo_add = None
		#imo_src = None
		imo_res = None

		try:
			srcpath = self.peices[1]
		except:
			srcpath = ''
		try:
			dstpath = self.peices[2]
		except:
			dstpath = ''
		try:
			feather = float(self.peices[3])
		except:
			feather = 0.5
		try:
			target = self.peices[4]
		except:
			target = 'default'

		if file_is_image(srcpath) is not True:
			imo_src = imageobject_get(srcpath)
			srcpath = imo_src.path

		if file_is_image(dstpath) is not True:
			imo_dst = imageobject_get(dstpath)
			dstpath = imo_dst.path

		if len(srcpath) == 0:
			print '%s: src image path is empty!' % (self.peices[0])
			return

		if len(dstpath) == 0:
			print '%s: dst image path is empty!' % (self.peices[0])
			return
		src = Image.open(srcpath)
		srcbox = src.size
		dst = Image.open(dstpath)
		dstbox = dst.size

		if file_is_image(target) is not True:
			imo_res = imageobject_get(target)
			target = imo_res.path
		if len(target) == 0:
			target = None

		#image_bleach(srcimg, srcbox, 0.20)
		result = images_multiply(src, srcbox, dst, dstbox, feather, target)
		if imo_res is not None:
			imo_res.set_path(result)


	def op_grid(self):
		""" Return
		"""
		imo_add = None
		imo_src = None
		imo_res = None
		power = [4, 4]

		try:
			imgpath = self.peices[1]
		except:
			imgpath = ''
		try:
			power[0] = int(self.peices[2])
		except:
			power[0] = 16
		try:
			power[1] = int(self.peices[3])
		except:
			power[1] = 16
		try:
			targval = self.peices[4]
		except:
			targval = 'default'

		if file_is_image(imgpath) is not True:
			imo_src = imageobject_get(imgpath)
			srcpath = imo_src.path
		else:
			srcpath = imgpath

		if file_is_image(targval) is not True:
			imo_res = imageobject_get(targval)
			target = imo_res.path
		else:
			target = targval
		if len(target) == 0:
			target = None

		src = Image.open(srcpath)
		srcbox = src.size
		#white = Image.new('RGB', srcbox, (0, 0, 0))
		white = src.copy()

		funky_color_blocks = True

		print power[0]
		print power[1]

		if funky_color_blocks is True:
			wide = srcbox[0]
			high = srcbox[1]
			#half = srcbox[0]/2
			#block = int(half/wide)

			#grad = 0.0
			#flw = float(wide)
			for i in range(0, wide):
				for j in range(0, high):
					if ((i+1) % power[0]) == 0 or ((j+1) % power[1]) == 0:
						add_pixel(white, (i, j), (255, 255, 255))
					#else:
					#	srcpxl = src.getpixel((i, j))
					#	add_pixel(white, (i, j), srcpxl)

		media_ct = 0
		outimg = target
		if outimg is None:
			outimg = 'out%04d.png' % (media_ct+1)
			while file_exists(outimg) is True:
				outimg = 'out%04d.png' % (media_ct+1)
				if file_exists(outimg) is True:
					media_ct += 1
			print outimg

		white.save(outimg)
		if imo_res is not None:
			imo_res.set_path(outimg)
		return outimg

	def op_xmark(self):
		""" Return
		"""
		imgpath = ''
		imo_add = None
		imo_src = None
		imo_res = None
		targval = None
		power = [16, 16]

		if len(self.peices) >= 2:
			if self.peices[1].isstring():
				imgpath = self.peices[1].val
		if len(self.peices) >= 3:
			if self.peices[2].isnumber():
				power[0] = self.peices[2].val
		if len(self.peices) >= 4:
			if self.peices[3].isnumber():
				power[1] = self.peices[3].val
		if len(self.peices) >= 5:
			if self.peices[4].isstring():
				targval = self.peices[4].val

		if len(imgpath) == 0:
			print 'ERROR: op_xmark - src image path is empty!'
			return

		if file_is_image(imgpath) is not True:
			imo_src = imageobject_get(imgpath)
			srcpath = imo_src.path
		else:
			srcpath = imgpath

		if file_is_image(targval) is not True:
			imo_res = imageobject_get(targval)
			target = imo_res.path
		else:
			target = targval
		if len(target) == 0:
			target = None

		src = Image.open(srcpath)
		srcbox = src.size
		white = Image.new('RGB', srcbox, (0, 0, 0))

		funky_color_blocks = True

		if funky_color_blocks is True:
			wide = srcbox[0]
			high = srcbox[1]
			#half = srcbox[0]/2
			#block = int(half/wide)

			#grad = 0.0
			#flw = float(wide)
			for i in range(0, wide):
				for j in range(0, high):
					if xmatch([i, j], power) is True:
						add_pixel(white, (i, j), (255, 255, 255))
					else:
						srcpxl = src.getpixel((i, j))
						add_pixel(white, (i, j), srcpxl)
					#(src, start, size, color):

		media_ct = 0
		outimg = target
		if outimg is None:
			outimg = 'out%04d.png' % (media_ct+1)
			while file_exists(outimg) is True:
				outimg = 'out%04d.png' % (media_ct+1)
				if file_exists(outimg) is True:
					media_ct += 1
			print outimg

		white.save(outimg)
		if imo_res is not None:
			imo_res.set_path(outimg)
		return outimg

	def op_zoom(self):
		""" Return
		"""
		#imo_add = None
		#imo_src = None
		#imo_res = None
		#power = 0
		zc = [0.0, 0.0]
		imgpath = None
		#targval = 'default'
		#zoom_val = False
		mode = 'bicubic'
		zoomstart = 0.25
		zoomfinish = 1.00
		zoomsteps = 10

		i = 0
		while i < len(self.peices):
			if str_match(self.peices[i], '-i'):
				imgpath = self.peices[i+1]
				i += 1
			elif str_match(self.peices[i], '-l'):
				zc[0] = float(self.peices[i+1])
				zc[1] = float(self.peices[i+2])
				#zoom_val = True
				i += 2
			#elif str_match(self.peices[i], '-o'):
			#	targval = self.peices[i+1]
			#	i += 1
			elif str_match(self.peices[i], '-m'):
				mode = self.peices[i+1]
				i += 1
			elif str_match(self.peices[i], '-z'):
				zoomstart = float(self.peices[i+1])
				zoomfinish = float(self.peices[i+2])
				i += 2
			elif str_match(self.peices[i], '-ct'):
				zoomsteps = int(self.peices[i+1])
				i += 1
			i += 1

		if imgpath is None:
			print 'no image path in peices(%s)' % self.peices
			return None

		if file_is_image(imgpath) is not True:
			imo_src = imageobject_get(imgpath)
			srcpath = imo_src.path
		else:
			srcpath = imgpath

		#if file_is_image(targval) is not True:
		#	imo_res = imageobject_get(targval)
		#	target = imo_res.path
		#else:
		#	target = targval
		#if len(target) == 0:
		#	target = None

		src = Image.open(srcpath)
		srcbox = src.size
		#zoomval = 1.0
		zoomdelta = (zoomstart-zoomfinish)/float(zoomsteps)
		middle = [srcbox[0]/2, srcbox[1]/2]
		center = [middle[0] - int(zc[0]*float(middle[0])), middle[1] - int(zc[1]*float(middle[1]))]
		#image_operation('selsquare zoomsel %s %d %d %d %d' % (srcpath, start[0], start[1], targsize[0], targsize[1]))
		#image_operation('selsave zoomsel outzoom.png')
		#image_operation('resize -i outzoom.png -w %d -h %d -m %s -o %s' % (srcbox[0], srcbox[1], mode, targval))
		#image_operation('selwipe zoomsel')
		#image_operation('selsquare zoomsel %s 0 0 %d %d' % (srcpath, srcbox[0], srcbox[1]))

		#zoomval = zoomstart - zoomdelta
		#centers = []
		zoomval = zoomstart
		targsize = [int(float(srcbox[0])*zoomval), int(float(srcbox[1])*zoomval)]
		start = [center[0]-(targsize[0]/2), center[1]-(targsize[1]/2)]
		for j in range(0, 2):
			if start[j] < 0:
				start[j] = 0
			if start[j] + targsize[j] > srcbox[j]:
				start[j] = srcbox[j]-targsize[j]
		center_start = [start[0]+targsize[0]/2, start[1]+targsize[1]/2]

		zoomval = zoomfinish
		targsize = [int(float(srcbox[0])*zoomval), int(float(srcbox[1])*zoomval)]
		start = [center[0]-(targsize[0]/2), center[1]-(targsize[1]/2)]
		for j in range(0, 2):
			if start[j] < 0:
				start[j] = 0
			if start[j] + targsize[j] > srcbox[j]:
				start[j] = srcbox[j] - targsize[j]
		center_finish = [start[0]+targsize[0]/2, start[1]+targsize[1]/2]

		center_diff = [float(center_finish[0]-center_start[0]), float(center_finish[1]-center_start[1])]
		print center_diff
		center_delta = [float(center_diff[0])/float(zoomsteps), float(center_diff[1])/float(zoomsteps)]

		zoomval = zoomstart
		center[0] = center_start[0]
		center[1] = center_start[1]
		for i in range(0, zoomsteps+1):
			print('zoom value is %f' % zoomval)
			center[0] = center_start[0] + int(center_delta[0]*i)
			center[1] = center_start[1] + int(center_delta[1]*i)
			print('center is %s' % center)
			ftargsz = [float(srcbox[0])*zoomval, float(srcbox[1])*zoomval]
			targsize = [int(ftargsz[0]), int(ftargsz[1])]
			print ftargsz
			print targsize
			for j in range(0, 2):
				if ftargsz[j] > float(targsize[j]):
					targsize[j] = int(ftargsz[j]+1.0)
			start = [center[0]-(targsize[0]/2), center[1]-(targsize[1]/2)]
			for j in range(0, 2):
				if start[j] < 0:
					start[j] = 0
				if start[j] + targsize[j] > srcbox[j]:
					start[j] = srcbox[j] - targsize[j]
			white = src.crop((start[0], start[1], start[0]+targsize[0], start[1]+targsize[1]))
			#image_operation('selcrop zoomsel %d %d %d %d' % (start[0], start[1], targsize[0], targsize[1]))
			#image_operation('selsave zoomsel outzoom.png')
			white.save('outzoom.png')
			sz = dump_imagesize('outzoom.png')
			print('outzoom size %d x %d' % (sz[0], sz[1]))
			outimage = get_outimage()
			ImageOperation('resize -i outzoom.png -w %d -h %d -m %s -o %s' % (srcbox[0], srcbox[1], mode, outimage))
			zoomval -= zoomdelta
		#image_operation('selwipe zoomsel')

	def op_selset(self):
		""" Return
		"""
		#imo_src = None
		#imo_dst = None

		try:
			srcpath = self.peices[1]
		except:
			srcpath = ''

		selection_get(srcpath)

	def op_selappend(self):
		""" Return
		"""
		debug_this = False
		#srcsel = None
		#dstsel = None
		#imo_dst = None
		ofs = None
		scale_do = False
		scale = 1
		sel_min = None
		sel_max = None
		colc = None
		#alph = None

		srcpath = self.get_peice(1, _TYPE_String)
		dstpath = self.get_peice(2, _TYPE_String)

		#try:
		#	sel_min = [int(self.peices[5]), int(self.peices[6])]
		#except:
		#	#no pixels selected
		#	pass
		#try:
		#	sel_max = [int(self.peices[7]), int(self.peices[8])]
		#except:
		#	#no pixels selected
		#	pass

		if sel_min is not None:
			if sel_max is None:
				sel_min = None

		i = 3

		while i < len(self.peices):
				#print self.peices[i]
				peice = str(self.peices[i])
				if str_match(peice, 'of'):
					#offset
					if debug_this:
						print "OFFSET"
					ofs_x = self.get_peice(i+1, _TYPE_Integer)
					ofs_y = self.get_peice(i+2, _TYPE_Integer)
					if (ofs_x is not None) and (ofs_y is not None):
						ofs = [ofs_x, ofs_y]
						if debug_this:
							print 'OFS [%d x %d]' % (ofs[0], ofs[1])
						i += 2
					else:
						if debug_this:
							print 'FAIL X %s' % ofs_x
							print 'FAIL Y %s' % ofs_y
				elif str_match(peice, 'sc'):
					if debug_this:
						print "SCALE"
					scale = self.get_peice(i+1, _TYPE_Integer)
					if scale is not None:
						scale_do = True
						i += 1
				elif str_match(peice, 'cl'):
					col_r = self.get_peice(i+1, _TYPE_Integer)
					col_g = self.get_peice(i+2, _TYPE_Integer)
					col_b = self.get_peice(i+3, _TYPE_Integer)
					if (col_r is not None) and (col_g is not None) and (col_b is not None):
						colc = [col_r, col_g, col_b]
						if debug_this:
							print 'COLOR [%d %d %d]' % (colc[0], colc[1], colc[2])
							print colc
						i += 3
					else:
						if debug_this:
							print 'FAIL R %s' % col_r
							print 'FAIL G %s' % col_g
							print 'FAIL B %s' % col_b
				i += 1

		if ofs is None:
			print 'Error(selappend): offset is None'
			return

		#print 'SELAPPEND source is %s' % srcpath
		#print 'SELAPPEND destination is %s' % dstpath
		#print scale
		#print scale_do
		#print _min

		srcsel = selection_get(srcpath)
		dstsel = selection_get(dstpath)
		if srcsel is dstsel:
			print 'Error(selappend): SAME SEL %s vs %s' % (srcpath, dstpath)
			return
		#print srcpath
		#print dstpath
		#print ofs
		## clen = len(srcsel.coords)
		#print clen
		_debug = False
		ct = 0
		for selc in srcsel.coords:
			if _debug is True:
				print '--- COORDS'
			#if colc is not None:
			#	print 'WTF GUYS'
			target_color = [0, 0, 0, 255]
			if colc is None:
				for i in range(0, 3):
					target_color[i] = selc.color[i]
			else:
				for i in range(0, 3):
					#print colc[i]
					#print selc.color[i]
					target_color[i] = colc[i] * (float(selc.color[i]/255.0))
			#target_color = [0, 0, 0, 255]
			if _debug is True:
				print '!!!'
				print colc
				print selc.color
				print target_color
			#print 'coord'
			if sel_min is None:
				if scale_do:
					#print 'selappend'
					for k in range(0, scale):
						for l in range(0, scale):
							sc = SelCoord([selc.xy[0]*scale+ofs[0]+k, selc.xy[1]*scale+ofs[1]+l], target_color)
							dstsel.coord_add(sc)
				else:
					sc = SelCoord([selc.xy[0]+ofs[0], selc.xy[1]+ofs[1]], target_color)
					dstsel.coord_add(sc)
					#print '%d / %d : (%s) %d' % (ct, clen, str(selc.xy), len(srcsel.coords))
			else:
				pixel_ok = False
				if (selc.xy[0] >= sel_min[0] and selc.xy[1] >= sel_min[1]) and (selc.xy[0] < sel_max[0] and selc.xy[1] < sel_max[1]):
					pixel_ok = True
				if pixel_ok:
					if scale_do:
						for k in range(0, scale):
							for l in range(0, scale):
								sc = SelCoord([selc.xy[0]*scale+ofs[0]+k, selc.xy[1]*scale+ofs[1]+l], target_color)
								dstsel.coord_add(sc)
					else:
						sc = SelCoord([selc.xy[0]+ofs[0], selc.xy[1]+ofs[1]], target_color)
						dstsel.coord_add(sc)
			ct += 1

	def op_seladdmark(self):
		""" options are [selectionName] [posX] [posY] [colorR] [colorG] [colorB] [colorA] [xSize] [xMark]
		"""
		#srcsel = None
		#imo_dst = None

		srcpath = self.get_peice(1, _TYPE_String)
		power = [self.get_peice(2, _TYPE_Integer), self.get_peice(3, _TYPE_Integer)]
		color = [self.get_peice(4, _TYPE_Integer), self.get_peice(5, _TYPE_Integer), self.get_peice(6, _TYPE_Integer)]
		alpha = self.get_peice(7, _TYPE_Integer)
		xsize = self.get_peice(8, _TYPE_Integer)
		xmark = self.get_peice(9, _TYPE_Integer)
		if srcpath is None:
			srcpath = ''
		if power[0] is None or power[1] is None:
			power = [1, 1]
		if color[0] is None or color[1] is None or color[2] is None:
			color = [255, 255, 255]
		if alpha is None:
			alpha = 255
		color.append(alpha)
		if xsize is None:
			xsize = 1
		xm = False
		if xmark is not None:
			xm = True

		srcsel = selection_get(srcpath)
		srcsel.mark(power, xsize, color, xm)

	def op_selgrid(self):
		""" options are [selectionName] [cols] [rows] [colorR] [colorG] [colorB]
		calls SelectionObject.grid()
		"""
		try:
			srcpath = self.peices[1]
		except:
			srcpath = ''
		try:
			power = [int(self.peices[2]), int(self.peices[3])]
		except:
			power = [0, 0]
		try:
			color = [int(self.peices[4]), int(self.peices[5]), int(self.peices[6])]
		except:
			color = [255, 255, 255]
		print color

		srcsel = selection_get(srcpath)
		#grid(self, cols, rows, bounds, color):
		cols = None
		rows = None
		if power[0] != 0:
			cols = power[0]
		if power[1] != 0:
			rows = power[1]
		srcsel.grid(cols, rows, srcsel.bounds, color)

	def op_selwipe(self):
		""" options are [selectionName]
		calls SelectionObject.wipe(), which obliterates the contents of the SelectionObject.
		"""
		srcpath = self.get_peice(1, _TYPE_String)

		srcsel = selection_get(srcpath)
		srcsel.wipe()

	def op_selremovecolor(self):
		""" options are [selectionName] [colorR] [colorG] [colorB]
		calls SelectionObject.removecolor()
		"""
		color = None
		try:
			srcpath = self.peices[1]
		except:
			srcpath = ''
		try:
			color = [int(self.peices[2]), int(self.peices[3]), int(self.peices[4])]
		except:
			pass
		if color is None:
			return
		srcsel = selection_get(srcpath)
		srcsel.removecolor(color)

	def op_selbounds(self):
		""" Return
		"""
		debug_this = False
		power = [0, 0]
		#print 'ok selbounds (%s)' % (str(self.peices))
		#try:
		srcpath = self.get_peice(1, _TYPE_String)
		pwr_a = self.get_peice(2, _TYPE_Integer)
		pwr_b = self.get_peice(3, _TYPE_Integer)
		if pwr_a is not None and pwr_b is not None:
			power = [pwr_a, pwr_b]
		clm = str(self.get_peice(4))
		if debug_this:
			print 'CLAMP STR %s' % clm
		clamp = str_match(clm, '1')
		if debug_this:
			print 'SELBOUDNDS: %s' % srcpath
			if clamp:
				print 'CLAMP IS TRUE'
			else:
				print 'CLAMP IS FALSE'
		srcsel = selection_get(srcpath)
		srcsel.size(power, clamp)

	def op_selrotate(self):
		""" Return
		"""
		fulcrum = [0, 0]

		try:
			srcpath = self.peices[1]
		except:
			srcpath = ''
		try:
			power = float(self.peices[2])
		except:
			power = 45.0
		try:
			fulcrum = [int(self.peices[3]), int(self.peices[4])]
		except:
			pass

		srcsel = selection_get(srcpath)
		print power
		print fulcrum

		for sc in srcsel.coords:
			cosf = math.cos(math.radians(power))
			sinf = math.sin(math.radians(power))
			ofs = [sc.xy[0]-fulcrum[0], sc.xy[1]-fulcrum[1]]
			pos = [ofs[0]*cosf-ofs[1]*sinf, ofs[1]*cosf+ofs[0]*sinf]
			sc.xy[0] = pos[0]+fulcrum[0]
			sc.xy[1] = pos[1]+fulcrum[1]

	def op_selsquare(self):
		debug_this = True
		#srcsel = None
		#imo_dst = None
		colormask = None
		ofs = [0, 0]
		scale_do = False
		scale = 1
		alpha = False
		sel_min = None
		sel_max = None

		srcpath = self.get_peice(1, _TYPE_String)
		imgpath = self.get_peice(2, _TYPE_String)
		pwr_a = self.get_peice(3, _TYPE_Integer)
		pwr_b = self.get_peice(4, _TYPE_Integer)
		if pwr_a is not None and pwr_b is not None:
			sel_min = [pwr_a, pwr_b]
		pwr_a = self.get_peice(5, _TYPE_Integer)
		pwr_b = self.get_peice(6, _TYPE_Integer)
		if (pwr_a is not None) and (pwr_b is not None) and (sel_min[0] is not None) and (sel_min[1] is not None):
			sel_max = [pwr_a + sel_min[0], pwr_b + sel_min[1]]
		else:
			sel_min = [0, 0]
			sel_max = [None, None]
		#print 'MIN %s MAX %s' % (sel_min, sel_max)

		i = 3
		while i < len(self.peices):
			peice = str(self.peices[i])
			if str_match(peice, 'cm'):
				#color mask
				col_r = self.get_peice(i+1, _TYPE_Integer)
				col_g = self.get_peice(i+2, _TYPE_Integer)
				col_b = self.get_peice(i+3, _TYPE_Integer)
				if (col_r is not None) and (col_g is not None) and (col_b is not None):
					colormask = [col_r, col_g, col_b]
					if debug_this:
						print 'COLOR [%d %d %d]' % (colormask[0], colormask[1], colormask[2])
					i += 3
				else:
					if debug_this:
						print 'FAIL R %s' % col_r
						print 'FAIL G %s' % col_g
						print 'FAIL B %s' % col_b
			elif str_match(peice, 'of'):
				#ofs
				if debug_this:
					print "OFFSET"
				#try:
				ofs_x = self.get_peice(i+1, _TYPE_Integer)
				ofs_y = self.get_peice(i+2, _TYPE_Integer)
				if (ofs_x is not None) and (ofs_y is not None):
					ofs = [ofs_x, ofs_y]
					if debug_this:
						print 'OFS [%d x %d]' % (ofs[0], ofs[1])
					i += 2
				else:
					if debug_this:
						print 'FAIL X %s' % ofs_x
						print 'FAIL Y %s' % ofs_y
			elif str_match(peice, 'sc'):
				if debug_this:
					print "SCALE"
				scale = self.get_peice(i+1, _TYPE_Integer)
				if scale is not None:
					scale_do = True
					i += 1
			i += 1

		srcsel = selection_get(srcpath)

		if file_is_image(imgpath) is not True:
			imo_dst = imageobject_get(imgpath)
			imgpath = imo_dst.path

		try:
			srcimg = Image.open(imgpath)
			srcbox = srcimg.size
		except:
			return

		#print '--- SELSQUARE ---'
		#print imgpath
		#print srcbox
		#print sel_min
		#print sel_max
		#print ofs

		for i in range(0, 2):
			if sel_max[i] is None:
				sel_max[i] = srcbox[i]
			if sel_min[i] < 0:
				sel_min[i] = 0
			if sel_max[i] > srcbox[i]:
				sel_max[i] = srcbox[i]

		#print('_min %d, %d' % (_min[0], _min[1]))
		#print('_max %d, %d' % (_max[0], _max[1]))
		#print('%s, %d, %d, %d, %d' % (imgpath, srcbox[0], srcbox[1], ofs[0], ofs[1]))
		#print dir(srcimg)
		## i = _min[0]
		## j = _min[1]
		## palette = None
		## pixdata = list(srcimg.getdata())
		bands = list(srcimg.getbands())

		#print bands
		if str_match(bands[0], 'P'):
			srcimg = srcimg.convert("RGBA")
			alpha = True
		if len(bands) == 4:
			if str_match(bands[3], 'A'):
				alpha = True
		zed = 0
		count = (sel_max[0] - sel_min[0]) * (sel_max[1] - sel_min[1])
		for i in range(sel_min[0], sel_max[0]):
			for j in range(sel_min[1], sel_max[1]):
				#print('%d, %d' % (i, j))
				if (zed > 0) and ((zed % 8192) == 0):
					perc = float(zed) / float(count)
					print ' - %4.2f%%' % perc
				srcpxl = srcimg.getpixel((i, j))
				pixel_ok = True
				#print srcpxl
				#else:
				#	srcpxl = pixdata[i * srcbox[0] + j] * 3
				#	val = [pal[srcpxl], pal[srcpxl+1], pal[srcpxl+2]]
				#	srcpxl = val
				#	print srcpxl
				#	print 'ugh'
				if colormask is not None:
					#print 'ugh'
					if color_match(srcpxl, colormask) is not True:
						#pixel_ok = True
						pass
					else:
						pixel_ok = False
						#print srcpxl
						#print colormask
					#if srcpxl[0]!=colormask[0] and srcpxl[1]!=colormask[1] and srcpxl[2]!=colormask[2]:
				if pixel_ok:
					if scale_do:
						for k in range(0, scale):
							for l in range(0, scale):
								sc = SelCoord([i-sel_min[0]+ofs[0]+k, j-sel_min[1]+ofs[1]+l], [srcpxl[0], srcpxl[1], srcpxl[2]])
								srcsel.coord_add(sc)
					else:
						sc = None
						if alpha:
							if srcpxl[3] > 0:
								sc = SelCoord([i-sel_min[0]+ofs[0], j-sel_min[1]+ofs[1]], [srcpxl[0], srcpxl[1], srcpxl[2], srcpxl[3]])
						else:
							sc = SelCoord([i-sel_min[0]+ofs[0], j-sel_min[1]+ofs[1]], [srcpxl[0], srcpxl[1], srcpxl[2]])
						if sc is not None:
							srcsel.coord_add(sc)
				zed += 1
		#print 'SELSQUARE %s len coords %d' % (srcpath, len(srcsel.coords))

	def op_selblock(self):
		""" Return
		"""
		srcpath = self.get_peice(1, _TYPE_String)
		start = [self.get_peice(2, _TYPE_Integer), self.get_peice(3, _TYPE_Integer)]
		size = [self.get_peice(4, _TYPE_Integer), self.get_peice(5, _TYPE_Integer)]
		color = [self.get_peice(6, _TYPE_Integer), self.get_peice(7, _TYPE_Integer), self.get_peice(8, _TYPE_Integer)]
		alpha = self.get_peice(9, _TYPE_Integer)
		if alpha is None:
			color.append(255)
		else:
			color.append(alpha)
		radius = self.get_peice(10, _TYPE_Float)
		#print color
		#print 'SELBLOCK: %s' % (srcpath)
		#print 'SELBLOCK: %s' % (str(color))
		srcsel = selection_get(srcpath)
		srcsel.block(start, size, radius, color)

	def op_sellumrange(self):
		""" Return
		"""
		try:
			srcpath = self.peices[1]
		except:
			srcpath = ''
		try:
			imgpath = self.peices[2]
		except:
			imgpath = ''
		try:
			_max = int(self.peices[4])
		except:
			#no pixels selected
			return
			_min = int(self.peices[3])

		srcsel = selection_get(srcpath)

		if file_is_image(imgpath) is not True:
			imo_dst = imageobject_get(imgpath)
			imgpath = imo_dst.path

		srcimg = Image.open(imgpath)
		srcbox = srcimg.size

		print('_min %d _max %d' % (_min, _max))
		#i = 0
		#j = 0
		#return
		for i in range(0, srcbox[0]):
			for j in range(0, srcbox[1]):
				#print('%d, %d' % (i, j))

				#if oldFashioned is True:
				srcpxl = srcimg.getpixel((i, j))
				#else:
				#	pxl = pxls[x, y]
				gr_val = srcpxl[0]*0.3 + srcpxl[1]*0.59 + srcpxl[2]*0.11

				#print ' -'
				if (gr_val >= _min) and (gr_val < _max):
									#backup = 233
									#if i-backup >= 0:
									#		print('				self.tiny_dot( x + %d, y + %d )' % ((i-backup)%14, j-7))
					sc = SelCoord([i, j], [srcpxl[0], srcpxl[1], srcpxl[2]])
					srcsel.coord_add(sc)

	def op_selcrop(self):
		""" Return
		"""
		start = [0, 0]
		size = [0, 0]
		srcpath = None

		i = 0
		while i < len(self.peices):
			peice = str(self.peices[i])
			if str_match(peice, '-i'):
				srcpath = self.peices[i+1]
				i += 1
			elif str_match(peice, '-st'):
				start[0] = int(self.peices[i+1])
				start[1] = int(self.peices[i+2])
				i += 2
			elif str_match(peice, '-sz'):
				size[0] = int(self.peices[i+1])
				size[1] = int(self.peices[i+2])
				i += 2
			i += 1

		srcsel = selection_get(srcpath)
		if srcsel is not None:
			srcsel.crop(start, size)

	def op_selbloom(self):
		""" Return
		"""
		#image_keep = None
		#feather = 1.0
		#imo_src = None
		try:
			srcpath = self.peices[1]
		except:
			srcpath = ''
		try:
			dstpath = self.peices[2]
		except:
			dstpath = 'defaultsel'
		try:
			radius = float(self.peices[3])
		except:
			radius = 3.0
		try:
			feather = float(self.peices[4])
		except:
			feather = 0.25

		srcsel = selection_get(srcpath)
		dstsel = selection_get(dstpath)

		cir = CircleObject(radius, feather)
		for cor in srcsel.coords:
			cir.selblit(dstsel, cor)

		#result = srcsel.save(target, box, tuple(color))
		#if image_keep is not None:
		#	image_keep.set_path(result)

	def op_selsave(self):
		""" options are [selectionName] [outPath] [sizeX] [sizeY] [colorR] [colorG] [colorB]
		"""
		image_keep = None
		#imo_src = None
		target = ''

		try:
			srcpath = str(self.peices[1])
		except:
			srcpath = ''
		try:
			targval = str(self.peices[2])
		except:
			targval = 'default'
		try:
			box = [int(self.peices[3]), int(self.peices[4])]
		except:
			box = None
		try:
			color = [int(self.peices[5]), int(self.peices[6]), int(self.peices[7])]
		except:
			color = [255, 255, 255]

		srcsel = selection_get(srcpath)

		if file_is_image(targval) is not True:
			image_keep = imageobject_get(targval)
			target = image_keep.path
		else:
			target = targval
		if len(target) == 0:
			target = None

		result = srcsel.save(target, box, tuple(color))
		if result is not None:
			if image_keep is not None:
				image_keep.set_path(result)

