# -*- coding: utf-8 -*-
# Copyright (c) 2015 Brad Newbold (wudan07 [at] gmail.com)
# See LICENSE for details.
# common.py
#
"""wIcon library:
	Image Utility functions
"""

import math
import random
#import time
from common import *
from PIL import Image, PngImagePlugin, JpegImagePlugin
from selection import SelCoord
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


def is_pil_image(a):
	"""
		a is something that should have been opened using Image.Open
		Return True if this is a PNG or JPEG image, False if anything else
	"""
	if isinstance(a, PngImagePlugin.PngImageFile):
		return True
	elif isinstance(a, JpegImagePlugin.JpegImageFile):
		return True
	return False


def add_pixel(src, cor, color):
	"""
		src is a PIL ImageObject
		cor is a 2 length list of integers
		color is a 3 length list of integers
		todo: better exception
		Return nothing
	"""
	if is_pil_image(src) is False:
		return False
	bounds = src.size
	val_clamp(cor[0], 0, bounds[0]-1)
	val_clamp(cor[1], 0, bounds[1]-1)
	src_color = src.getpixel(cor)
	res_color = (src_color[0] + color[0], src_color[1] + color[1], src_color[2] + color[2])
	res_color = color_clamp(res_color)
	src.putpixel(cor, res_color)
	return True


def color_block(src, start, size, color):
	""" Return
	"""
	bounds = src.size
	#print start
	_min_x = start[0]
	_min_y = start[1]
	_max_x = _min_x+size[0]
	_max_y = _min_y+size[1]
	val_clamp(_min_x, 0, bounds[0])
	val_clamp(_min_y, 0, bounds[1])
	val_clamp(_max_x, 0, bounds[0])
	val_clamp(_max_y, 0, bounds[1])
	j = _min_y

	while j < _max_y:
		i = _min_x
		while i < _max_x:
			add_pixel(src, (i, j), color)
			#src.putpixel((i, j), (color[0], color[1], color[2]))
			i += 1
		j += 1


def make_noise(pwr, level, path):
	""" Return
	"""
	#src = Image.new('RGB', [pwr, pwr], (128, 128, 128))
	src = Image.new('RGB', [pwr, pwr], (0, 0, 0))
	#color_block(src, [32, 32], [128, 128], (255, 0, 0))
	#feather = 1.0
	print pwr
	i = 1
	block_sz = pwr
	if block_sz > 1:
		block_sz = 1
	#feather = 128.0 / block_sz
	feather = 1.0
	while block_sz != 0:
		nums = pwr / block_sz
		nums *= nums
		block_sz /= 2
		if block_sz <= 0:
			block_sz = 1
		timesquel = float(block_sz) * feather
		print '%d, %d (%d) %f' % (i, block_sz, nums, feather)
		j = 0
		while j < pwr:
			k = 0
			while k < pwr:
				randval = random_inrange(0, 255)
				print 'randval %d timesquel %f' % (randval, timesquel)
				color_block(src, [k, j], [block_sz, block_sz], (randval, randval, randval))
				k += block_sz
			j += block_sz
		i += 1
		if block_sz == 1:
			block_sz = 0
	src.save(path)


def add_noise(src, src_bounds, feather, resimg):
	"""
		Return result of image_add
	"""
	i = 2
	level = 1
	while i < src_bounds[0]:
		i *= 2
		level += 1
	while i < src_bounds[1]:
		i *= 2
		level += 1
	level += 1
	#print i
	#print level
	#print src_bounds
	#imageLoaded = False
	outimg = 'noise%05d.png' % i
	if file_exists(outimg) is not True:
		#make noise!
		make_noise(i, level, outimg)
	noz = Image.open(outimg)
	result = image_add(src, src_bounds, noz, noz.size, feather, True, resimg)
	return result


def image_greyscale(src, src_bounds, outimg):
	"""
		src
		Return outimg, which is a path that the greyscale image gets saved to
	"""
	media_ct = 0
	if outimg is None:
		outimg = 'out%04d.png' % (media_ct+1)
		while file_exists(outimg) is True:
			outimg = 'out%04d.png' % (media_ct+1)
			if file_exists(outimg) is True:
				media_ct += 1
		print outimg

	# create a new image the size of the source image
	white = Image.new('RGB', src_bounds, (0, 0, 0))
	_min_x = 0
	_min_y = 0
	_max_x = src_bounds[0]
	_max_y = src_bounds[1]

	# iterate through all coordinates
	j = _min_y
	while j < _max_y:
		i = _min_x
		while i < _max_x:
			# get pixel color from source image
			srcpxl = src.getpixel((i, j))
			gr_val = srcpxl[0]*0.3 + srcpxl[1]*0.59 + srcpxl[2]*0.11
			respxl = [gr_val, gr_val, gr_val]
			respxl[0] = val_clamp(respxl[0], 0, 255)
			respxl[1] = val_clamp(respxl[1], 0, 255)
			respxl[2] = val_clamp(respxl[2], 0, 255)
			#print srcpxl
			white.putpixel((i, j), (int(respxl[0]), int(respxl[1]), int(respxl[2])))
			i += 1
			#print i
		j += 1
	white.save(outimg)
	return outimg


def color_scotch(color, gr_val):
	""" Return
	"""
	bsqrd = gr_val * gr_val
	targetlen = math.sqrt(bsqrd+bsqrd+bsqrd)
	lumilen = math.sqrt(color[0]*color[0]+color[1]*color[1]+color[2]*color[2])
	rescolor = [0, 0, 0]
	if lumilen > 0.0:
		rescolor[0] = (color[0] / lumilen) * targetlen
		rescolor[1] = (color[1] / lumilen) * targetlen
		rescolor[2] = (color[2] / lumilen) * targetlen
	else:
		print('lumilen is zero, %d %d %d, target %2.2f\n' % (color[0], color[1], color[2], targetlen))
		rescolor[0] = 0.0
		rescolor[1] = 0.0
		rescolor[2] = 0.0
	return rescolor


def get_skoo_range(gr_val, skoo_sz):
	""" Return
	"""
	k = 0
	while gr_val > skoo_sz:
		gr_val -= skoo_sz
		k += 1
	return k


def image_skoo_apply(src, src_bounds, colors, skoo_sz, outimg):
	""" Return
	"""
	media_ct = 0
	if outimg is None:
		outimg = 'out%04d.png' % (media_ct + 1)
		while file_exists(outimg) is True:
			outimg = 'out%04d.png' % (media_ct+1)
			if file_exists(outimg) is True:
				media_ct += 1
		print outimg

	white = Image.new('RGB', src_bounds, (0, 0, 0))
	#white.save('temp.png')
	#white = Image.open('temp.png')
	_min_x = 0
	_min_y = 0
	_max_x = src_bounds[0]
	_max_y = src_bounds[1]
	j = _min_y
	#i = _min_x
	while j < _max_y:
	#for j in range(_min_y, _max_y):
		#print j
		i = _min_x
		while i < _max_x:
			#print('%d, %d' % (i, j))
			#print '!'
			#break
			srcpxl = src.getpixel((i, j))
			gr_val = srcpxl[0]*0.3 + srcpxl[1]*0.59 + srcpxl[2]*0.11
			color = colors[get_skoo_range(gr_val, skoo_sz)]
			respxl = color_scotch(color, gr_val)
			#respxl[0] *= 255.0
			#respxl[1] *= 255.0
			#respxl[2] *= 255.0
			respxl[0] = val_clamp(respxl[0], 0, 255)
			respxl[1] = val_clamp(respxl[1], 0, 255)
			respxl[2] = val_clamp(respxl[2], 0, 255)
			#print srcpxl
			white.putpixel((i, j), (int(respxl[0]), int(respxl[1]), int(respxl[2])))
			i += 1
			#print i
		j += 1
	white.save(outimg)
	return outimg


def image_scotch_apply(src, src_bounds, color, outimg):
	""" Return
	"""
	media_ct = 0
	if outimg is None:
		outimg = 'out%04d.png' % (media_ct+1)
		while file_exists(outimg) is True:
			outimg = 'out%04d.png' % (media_ct+1)
			if file_exists(outimg) is True:
				media_ct += 1
		print outimg

	white = Image.new('RGB', src_bounds, (0, 0, 0))
	#white.save('temp.png')
	#white = Image.open('temp.png')
	_min_x = 0
	_min_y = 0
	_max_x = src_bounds[0]
	_max_y = src_bounds[1]
	j = _min_y
	#i = _min_x
	while j < _max_y:
	#for j in range(_min_y, _max_y):
		#print j
		i = _min_x
		while i < _max_x:
			#print('%d, %d' % (i, j))
			#print '!'
			#break
			srcpxl = src.getpixel((i, j))
			gr_val = srcpxl[0]*0.3 + srcpxl[1]*0.59 + srcpxl[2]*0.11
			respxl = color_scotch(color, gr_val)
			#respxl[0] *= 255.0
			#respxl[1] *= 255.0
			#respxl[2] *= 255.0
			respxl[0] = val_clamp(respxl[0], 0, 255)
			respxl[1] = val_clamp(respxl[1], 0, 255)
			respxl[2] = val_clamp(respxl[2], 0, 255)
			#print srcpxl
			white.putpixel((i, j), (int(respxl[0]), int(respxl[1]), int(respxl[2])))
			i += 1
			#print i
		j += 1
	white.save(outimg)
	return outimg


def image_tone_apply(src, src_bounds, feather, color, outimg):
	""" Return
	"""
	media_ct = 0
	if outimg is None:
		outimg = 'out%04d.png' % (media_ct+1)
		while file_exists(outimg) is True:
			outimg = 'out%04d.png' % (media_ct+1)
			if file_exists(outimg) is True:
				media_ct += 1
		print outimg

	white = Image.new('RGB', src_bounds, (0, 0, 0))
	#white.save('temp.png')
	#white = Image.open('temp.png')
	_min_x = 0
	_min_y = 0
	_max_x = src_bounds[0]
	_max_y = src_bounds[1]
	j = _min_y
	#i = _min_x
	while j < _max_y:
	#for j in range(_min_y, _max_y):
		#print j
		i = _min_x
		while i < _max_x:
			#print('%d, %d' % (i, j))
			#print '!'
			#break
			srcpxl = src.getpixel((i, j))
			respxl = [srcpxl[0]*(color[0]*feather), srcpxl[1]*(color[1]*feather), srcpxl[2]*(color[2]*feather)]
			respxl[0] = val_clamp(respxl[0], 0, 255)
			respxl[1] = val_clamp(respxl[1], 0, 255)
			respxl[2] = val_clamp(respxl[2], 0, 255)
			#print srcpxl
			white.putpixel((i, j), (int(respxl[0]), int(respxl[1]), int(respxl[2])))
			i += 1
			#print i
		j += 1
	white.save(outimg)
	return outimg


def image_bleach(src, src_bounds, feather, outimg):
	""" Return
	"""
	media_ct = 0
	if outimg is None:
		outimg = 'out%04d.png' % (media_ct+1)
		while file_exists(outimg) is True:
			outimg = 'out%04d.png' % (media_ct+1)
			if file_exists(outimg) is True:
				media_ct += 1
		print outimg

	white = Image.new('RGB', src_bounds, (0, 0, 0))
	#white.save('temp.png')
	#white = Image.open('temp.png')
	_min_x = 0
	_min_y = 0
	_max_x = src_bounds[0]
	_max_y = src_bounds[1]
	j = _min_y
	#i = _min_x
	while j < _max_y:
	#for j in range(_min_y, _max_y):
		#print j
		i = _min_x
		while i < _max_x:
			#print('%d, %d' % (i, j))
			#print '!'
			#break
			srcpxl = src.getpixel((i, j))
			gr_val = srcpxl[0]*0.3 + srcpxl[1]*0.59 + srcpxl[2]*0.11
			respxl = [srcpxl[0]*feather+gr_val, srcpxl[1]*feather+gr_val, srcpxl[2]*feather+gr_val]
			respxl[0] = val_clamp(respxl[0], 0, 255)
			respxl[1] = val_clamp(respxl[1], 0, 255)
			respxl[2] = val_clamp(respxl[2], 0, 255)
			#print srcpxl
			white.putpixel((i, j), (int(respxl[0]), int(respxl[1]), int(respxl[2])))
			i += 1
			#print i
		j += 1
	white.save(outimg)
	return outimg


def images_multiply(src, src_bounds, dst, dst_bounds, feather, outimg):
	""" Return
	"""
	#print src_bounds
	#print dst_bounds
	if src_bounds[0] != dst_bounds[0]:
		return
	if src_bounds[1] != dst_bounds[1]:
		return

	media_ct = 0
	if outimg is None:
		outimg = 'out%04d.png' % (media_ct+1)
		while file_exists(outimg) is True:
			outimg = 'out%04d.png' % (media_ct+1)
			if file_exists(outimg) is True:
				media_ct += 1
		print outimg

	white = Image.new('RGB', src_bounds, (0, 0, 0))
	#white.save('temp.png')
	#white = Image.open('temp.png')

	srcclip = src.copy()
	white.paste(srcclip)
	_min_x = 0
	_min_y = src_bounds[0]
	_max_x = 0
	_max_y = src_bounds[1]
	j = _min_y
	#i = _min_x
	while j < _max_y:
	#for j in range(_min_y, _max_y):
		i = _min_x
		while i < _max_x:
		#for i in range(_min_x, _max_x):
			#print('%d, %d' % (i, j))
			#print '!'
			#break
			srcpxl = src.getpixel((i, j))
			dstpxl = dst.getpixel((i, j))
			respxl = [srcpxl[0]*dstpxl[0]*feather, srcpxl[1]*dstpxl[1]*feather, srcpxl[2]*dstpxl[2]*feather]
			respxl[0] = val_clamp(respxl[0], 0, 255)
			respxl[1] = val_clamp(respxl[1], 0, 255)
			respxl[2] = val_clamp(respxl[2], 0, 255)
			#print srcpxl
			white.putpixel((i, j), (int(respxl[0]), int(respxl[1]), int(respxl[2])))
			i += 1
			#print i
		j += 1
	white.save(outimg)
	return outimg


def image_subtract(src, src_bounds, dst, dst_bounds, feather, outimg):
	""" Return
	"""
	#print src_bounds
	#print dst_bounds
	if src_bounds[0] != dst_bounds[0]:
		return
	if src_bounds[1] != dst_bounds[1]:
		return

	media_ct = 0
	if outimg is None:
		outimg = 'out%04d.png' % (media_ct+1)
		while file_exists(outimg) is True:
			outimg = 'out%04d.png' % (media_ct+1)
			if file_exists(outimg) is True:
				media_ct += 1
		print outimg

	white = Image.new('RGB', src_bounds, (0, 0, 0))
	#white.save('temp.png')
	#white = Image.open('temp.png')

	srcclip = src.copy()
	white.paste(srcclip)
	dstnz = dst.getbbox()
	print dstnz
	_min_x = dstnz[0]
	_min_y = dstnz[1]
	_max_x = dstnz[2]
	_max_y = dstnz[3]
	j = _min_y
	#i = _min_x
	while j < _max_y:
	#for j in range(_min_y, _max_y):
		i = _min_x
		while i < _max_x:
		#for i in range(_min_x, _max_x):
			#print('%d, %d' % (i, j))
			#print '!'
			#break
			srcpxl = src.getpixel((i, j))
			dstpxl = dst.getpixel((i, j))
			respxl = [srcpxl[0]-dstpxl[0]*feather, srcpxl[1]-dstpxl[1]*feather, srcpxl[2]-dstpxl[2]*feather]
			respxl[0] = val_clamp(respxl[0], 0, 255)
			respxl[1] = val_clamp(respxl[1], 0, 255)
			respxl[2] = val_clamp(respxl[2], 0, 255)
			#print srcpxl
			white.putpixel((i, j), (int(respxl[0]), int(respxl[1]), int(respxl[2])))
			i += 1
			#print i
		j += 1
	white.save(outimg)
	return outimg


def image_add(src, src_bounds, dst, dst_bounds, feather, ignore_sz, outimg):
	""" Return
	"""
	#print src_bounds
	#print dst_bounds
	if ignore_sz is not True:
		if src_bounds[0] != dst_bounds[0]:
			return None
		if src_bounds[1] != dst_bounds[1]:
			return None

	media_ct = 0
	if outimg is None:
		outimg = 'out%04d.png' % (media_ct+1)
		while file_exists(outimg) is True:
			outimg = 'out%04d.png' % (media_ct+1)
			if file_exists(outimg) is True:
				media_ct += 1
		print outimg

	white = Image.new('RGB', src_bounds, (0, 0, 0))
	#white.save('temp.png')
	#white = Image.open('temp.png')

	srcclip = src.copy()
	white.paste(srcclip)
	if ignore_sz is True:
		_min_x = 0
		_min_y = 0
		_max_x = src_bounds[0]
		_max_y = src_bounds[1]
	else:
		dstnz = dst.getbbox()
		print dstnz
		_min_x = dstnz[0]
		_min_y = dstnz[1]
		_max_x = dstnz[2]
		_max_y = dstnz[3]
	j = _min_y
	#i = _min_x
	while j < _max_y:
	#for j in range(_min_y, _max_y):
		i = _min_x
		while i < _max_x:
		#for i in range(_min_x, _max_x):
			#print('%d, %d' % (i, j))
			#print '!'
			#break
			srcpxl = src.getpixel((i, j))
			dstpxl = dst.getpixel((i, j))
			respxl = [srcpxl[0]+dstpxl[0]*feather, srcpxl[1]+dstpxl[1]*feather, srcpxl[2]+dstpxl[2]*feather]
			respxl[0] = val_clamp(respxl[0], 0, 255)
			respxl[1] = val_clamp(respxl[1], 0, 255)
			respxl[2] = val_clamp(respxl[2], 0, 255)
			#print srcpxl
			white.putpixel((i, j), (int(respxl[0]), int(respxl[1]), int(respxl[2])))
			i += 1
			#print i
		j += 1
	white.save(outimg)
	print outimg
	return outimg


def image_convert_alpha(fn, outpath='img_out.png', trans=None):
	"""
		fn is a path to an image file
		outpath is the path to the output file (should be PNG file)
		trans is a color to be converted to transparent (think green-screen)
		Return nothing
	"""
	if trans is None:
		trans = [255, 255, 255]
	i = Image.open(fn)
	if is_pil_image(i) is False:
		return
	i = i.convert("RGBA")
	datas = i.getdata()
	data_new = list()
	rage = [0.30555, 0.35555]
	span = rage[1] - rage[0]

	for item in datas:
		diff = [item[0]-trans[0], item[1]-trans[1], item[2]-trans[2]]
		length = 0.0
		for j in range(0, 3):
			length += diff[j]*diff[j]
		length = math.sqrt(length)
		length /= 441.67295593
		if length <= rage[0]:
			data_new.append((item[0], item[1], item[2], 0))
		elif (length > rage[0]) and (length <= rage[1]):
			alpha = int(((length - rage[0])/span)*255.0)
			data_new.append((item[0], item[1], item[2], alpha))
		else:
			data_new.append(item)

	i.putdata(data_new)
	i.save(outpath, "PNG")


class ImageObject:
	def __init__(self, name):
		self.name = name
		self.path = ''

	def set_path(self, path):
		if len(path) == 0:
			self.path = None
			print('imgObj \'%s\' set to \'%s\'' % (self.name, self.path))
			return
		self.path = str(path)
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


def color_clamp(color):
	""" Returns a 3 value array using color as input, clamps range from 0 to 255
	"""
	res = [0, 0, 0]
	res[0] = val_clamp(color[0], 0, 255)
	res[1] = val_clamp(color[1], 0, 255)
	res[2] = val_clamp(color[2], 0, 255)
	return (res[0], res[1], res[2])


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
	a = str(path).lower()
	if str_match_end(a, '.jpg') is True:
		return True
	if str_match_end(a, '.jpeg') is True:
		return True
	elif str_match_end(a, '.png') is True:
		return True
	return False