# -*- coding: utf-8 -*-
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
from common import *
from selection import *
from glyph import glyphstr_get, glyphstr_monospace, glyphstr_length
#from q_math import *


def image_convert_alpha(fn, outpath='img_out.png', trans=None):
	""" Return
	"""
	if trans is None:
		trans = [255, 255, 255]
	print 'a'
	i = Image.open(fn)
	i = i.convert("RGBA")
	datas = i.getdata()
	data_new = list()
	rage = [0.30555, 0.35555]
	span = rage[1] - rage[0]

	print 'b'
	for item in datas:
		diff = [item[0]-trans[0], item[1]-trans[1], item[2]-trans[2]]
		length = 0.0
		for j in range(0, 3):
			length += diff[j]*diff[j]
		length = math.sqrt(length)
		length /= 441.67295593
		if length <= rage[0]:
			data_new.append((item[0], item[1], item[2], 0))
			#data_new.append((0, 0, 0, 255))
		elif (length > rage[0]) and (length <= rage[1]):
			#if length>0.0:
			#	print length
			alpha = int(((length - rage[0])/span)*255.0)
			#print alpha
			data_new.append((item[0], item[1], item[2], alpha))
		else:
			#data_new.append((0, 0, 0, 255))
			data_new.append(item)
		#if item[0] == trans[0] and item[1] == trans[1] and item[2] == trans[2]:
		#	data_new.append((item[0], item[1], item[2], 0))
		#else:
		#	data_new.append(item)
	print 'c'
	i.putdata(data_new)
	i.save(outpath, "PNG")


def add_pixel(src, cor, color):
	""" Return
	"""
	bounds = src.size
	#print bounds
	try:
		val_clamp(cor[0], 0, bounds[0]-1)
		val_clamp(cor[1], 0, bounds[1]-1)
		src_color = src.getpixel(cor)
		res_color = (src_color[0] + color[0], src_color[1] + color[1], src_color[2] + color[2])
		res_color = color_clamp(res_color)
		src.putpixel(cor, res_color)
	except:
		print('failed to put coord %d %d' % (cor[0], cor[1]))


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
	""" Return
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
	print i
	print level
	print src_bounds
	#imageLoaded = False
	outimg = 'noise%05d.png' % i
	if file_exists(outimg) is not True:
		#make noise!
		make_noise(i, level, outimg)
	noz = Image.open(outimg)
	result = image_add(src, src_bounds, noz, noz.size, feather, True, resimg)
	print outimg
	return result


def image_greyscale(src, src_bounds, outimg):
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


def op_noise(peices):
	""" Return
	"""
	image_keep = None
	#imo_src = None
	
	try:
		imgpath = peices[1]
	except:
		imgpath = ''
	try:
		noiseval = float(peices[2])
	except:
		noiseval = 0.5
	try:
		targval = peices[3]
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


def op_selset(peices):
	""" Return
	"""
	#imo_src = None
	#imo_dst = None
	
	try:
		srcpath = peices[1]
	except:
		srcpath = ''
	
	selection_get(srcpath)


def op_selsquare(peices):
	#srcsel = None
	#imo_dst = None
	colormask = None
	offset = [0, 0]
	scale_do = False
	scale = 1
	alpha = False

	try:
		srcpath = peices[1]
	except:
		srcpath = ''
	try:
		imgpath = peices[2]
	except:
		imgpath = ''
	try:
		_min = [int(peices[3]), int(peices[4])]
		_max = [int(peices[5]) + _min[0], int(peices[6]) + _min[1]]
	except:
		#no pixels selected
		_min = [0, 0]
		_max = [None, None]
		#return
	i = 3

	while i < len(peices):
		if str_match(peices[i], 'cm'):
			#color mask
			try:
				colormask = [int(peices[i+1]), int(peices[i+2]), int(peices[i+3])]
				i += 3
			except:
				pass
		elif str_match(peices[i], 'of'):
			#offset
			try:
				offset = [int(peices[i+1]), int(peices[i+2])]
				i += 2
			except:
				pass
		elif str_match(peices[i], 'sc'):
			#offset
			try:
				scale = int(peices[i+1])
				i += 1
			except:
				scale_do = False
				pass
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

	for i in range(0, 2):
		if _max[i] is None:
			_max[i] = srcbox[i]
		if _min[i] < 0:
			_min[i] = 0
		if _max[i] > srcbox[i]:
			_max[i] = srcbox[i]

	#print('_min %d, %d' % (_min[0], _min[1]))
	#print('_max %d, %d' % (_max[0], _max[1]))
	#print('%s, %d, %d, %d, %d' % (imgpath, srcbox[0], srcbox[1], offset[0], offset[1]))
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
	count = (_max[0] - _min[0]) * (_max[1] - _min[1])
	for i in range(_min[0], _max[0]):
		for j in range(_min[1], _max[1]):
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
							sc = SelCoord([i-_min[0]+offset[0]+k, j-_min[1]+offset[1]+l], [srcpxl[0], srcpxl[1], srcpxl[2]])
							srcsel.coord_add(sc)
				else:
					sc = None
					if alpha:
						if srcpxl[3] > 0:
							sc = SelCoord([i-_min[0]+offset[0], j-_min[1]+offset[1]], [srcpxl[0], srcpxl[1], srcpxl[2], srcpxl[3]])
					else:
						sc = SelCoord([i-_min[0]+offset[0], j-_min[1]+offset[1]], [srcpxl[0], srcpxl[1], srcpxl[2]])
					if sc is not None:
						srcsel.coord_add(sc)
			zed += 1


def op_selappend(peices):
	""" Return
	"""
	#srcsel = None
	#dstsel = None
	#imo_dst = None
	ofs = None
	scale_do = False
	scale = 1
	_min = None
	_max = None
	colc = None
	#alph = None
	
	try:
		srcpath = peices[1]
	except:
		srcpath = ''
	try:
		dstpath = peices[2]
	except:
		dstpath = ''
	try:
		ofs = [int(peices[3]), int(peices[4])]
	except:
		#no pixels selected
		pass
	try:
		_min = [int(peices[5]), int(peices[6])]
	except:
		#no pixels selected
			pass
	try:
		_max = [int(peices[7]), int(peices[8])]
	except:
		#no pixels selected
		pass

	if _min is not None:
		if _max is None:
			_min = None

	i = 3
	
	while i < len(peices):
			#print peices[i]
			if str_match(peices[i], 'of'):
				#offset
				try:
					ofs = [int(peices[i+1]), int(peices[i+2])]
					i += 2
				except:
					pass
			elif str_match(peices[i], 'sc'):
				try:
					scale = int(peices[i+1])
					scale_do = True
					i += 1
				except:
					scale_do = False
					pass
			elif str_match(peices[i], 'cl'):
				try:
					colc = [int(peices[i+1]), int(peices[i+2]), int(peices[i+3])]
					i += 3
				except:
					pass
			#elif str_match(peices[i], 'al'):
			#	try:
			#		alph = int(peices[i+1])
			#		i += 1
			#	except:
			#		pass
			i += 1

	if ofs is None:
		return

	#print srcpath
	#print dstpath
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
			print colc
			print selc.color
			print target_color
		#print 'coord'
		if _min is None:
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
			if (selc.xy[0] >= _min[0] and selc.xy[1] >= _min[1]) and (selc.xy[0] < _max[0] and selc.xy[1] < _max[1]):
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


def op_seladdmark(peices):
	""" options are [selectionName] [posX] [posY] [colorR] [colorG] [colorB] [colorA] [xSize] [xMark]
	"""
	#srcsel = None
	#imo_dst = None

	try:
		srcpath = peices[1]
	except:
		srcpath = ''
	try:
		power = [int(peices[2]), int(peices[3])]
	except:
		power = [1, 1]
	try:
		color = [int(peices[4]), int(peices[5]), int(peices[6])]
	except:
		color = [255, 255, 255]
	try:
		alpha = int(peices[7])
		color.append(alpha)
	except:
		color.append(255)
	try:
		xsize = int(peices[8])
	except:
		xsize = 1
	try:
		xmark = int(peices[9])
	except:
		xmark = None
	xm = False
	if xmark is not None:
		xm = True

	srcsel = selection_get(srcpath)
	srcsel.mark(power, xsize, color, xm)


def op_selwipe(peices):
	""" options are [selectionName]
	calls SelectionObject.wipe(), which obliterates the contents of the SelectionObject.
	"""
	try:
		srcpath = peices[1]
	except:
		srcpath = ''
	
	srcsel = selection_get(srcpath)
	srcsel.wipe()


def op_selremovecolor(peices):
	""" options are [selectionName] [colorR] [colorG] [colorB]
	calls SelectionObject.removecolor()
	"""
	color = None
	try:
		srcpath = peices[1]
	except:
		srcpath = ''
	try:
		color = [int(peices[2]), int(peices[3]), int(peices[4])]
	except:
		pass
	if color is None:
		return
	srcsel = selection_get(srcpath)
	srcsel.removecolor(color)


def op_selgrid(peices):
	""" options are [selectionName] [cols] [rows] [colorR] [colorG] [colorB]
	calls SelectionObject.grid()
	"""
	try:
		srcpath = peices[1]
	except:
		srcpath = ''
	try:
		power = [int(peices[2]), int(peices[3])]
	except:
		power = [0, 0]
	try:
		color = [int(peices[4]), int(peices[5]), int(peices[6])]
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


def op_selblock(peices):
	""" Return
	"""
	try:
		srcpath = peices[1]
	except:
		srcpath = ''
	try:
		start = [int(peices[2]), int(peices[3])]
	except:
		start = [0, 0]
	try:
		size = [int(peices[4]), int(peices[5])]
	except:
		size = [0, 0]
	try:
		color = [int(peices[6]), int(peices[7]), int(peices[8])]
	except:
		color = [255, 255, 255]
	try:
		alpha = int(peices[9])
		color.append(alpha)
	except:
		pass
	try:
		radius = float(peices[10])
	except:
		radius = None
	#print color
	
	srcsel = selection_get(srcpath)
	srcsel.block(start, size, radius, color)


def op_selbounds(peices):
	""" Return
	"""
	power = [0, 0]
	print 'ok selbounds (%s)' % (str(peices))
	try:
		srcpath = peices[1]
	except:
		srcpath = ''
	try:
		power = [int(peices[2]), int(peices[3])]
	except:
		pass

	try:
		clamp = str_match(peices[4], '1')
	except:
		clamp = True
	
	srcsel = selection_get(srcpath)
	srcsel.size(power, clamp)


def op_selrotate(peices):
	""" Return
	"""
	fulcrum = [0, 0]
	
	try:
		srcpath = peices[1]
	except:
		srcpath = ''
	try:
		power = float(peices[2])
	except:
		power = 45.0
	try:
		fulcrum = [int(peices[3]), int(peices[4])]
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


def op_sellumrange(peices):
	""" Return
	"""
	try:
		srcpath = peices[1]
	except:
		srcpath = ''
	try:
		imgpath = peices[2]
	except:
		imgpath = ''
	try:
		_min = int(peices[3])
		_max = int(peices[4])
	except:
		#no pixels selected
		return
	
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


def op_selcrop(peices):
	""" Return
	"""
	start = [0, 0]
	size = [0, 0]
	srcpath = None
	
	i = 0
	while i < len(peices):
		if str_match(peices[i], '-i'):
			srcpath = peices[i+1]
			i += 1
		elif str_match(peices[i], '-st'):
			start[0] = int(peices[i+1])
			start[1] = int(peices[i+2])
			i += 2
		elif str_match(peices[i], '-sz'):
			size[0] = int(peices[i+1])
			size[1] = int(peices[i+2])
			i += 2
		i += 1
	
	srcsel = selection_get(srcpath)
	if srcsel is not None:
		srcsel.crop(start, size)


def op_selbloom(peices):
	""" Return
	"""
	#image_keep = None
	#feather = 1.0
	#imo_src = None
	try:
		srcpath = peices[1]
	except:
		srcpath = ''
	try:
		dstpath = peices[2]
	except:
		dstpath = 'defaultsel'
	try:
		radius = float(peices[3])
	except:
		radius = 3.0
	try:
		feather = float(peices[4])
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


def op_selsave(peices):
	""" options are [selectionName] [outPath] [sizeX] [sizeY] [colorR] [colorG] [colorB]
	"""
	image_keep = None
	#imo_src = None
	
	try:
		srcpath = peices[1]
	except:
		srcpath = ''
	try:
		targval = peices[2]
	except:
		targval = 'default'
	try:
		box = [int(peices[3]), int(peices[4])]
	except:
		box = None
	try:
		color = [int(peices[5]), int(peices[6]), int(peices[7])]
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


def op_setobj(peices):
	""" Return
	"""
	imo_src = None
	#imo_dst = None
	
	try:
		srcpath = peices[1]
	except:
		srcpath = ''
	try:
		dstpath = peices[2]
	except:
		dstpath = ''
	
	if file_is_image(srcpath) is not True:
		imo_src = imageobject_get(srcpath)
		srcpath = imo_src.path
	
	if file_is_image(dstpath) is not True:
		imo_dst = imageobject_get(dstpath)
		dstpath = imo_dst.path
	
	if len(dstpath) == 0:
		print '%s: dst image path is empty!' % (peices[0])
		return
	
	if imo_src is not None:
		imo_src.set_path(dstpath)


def op_rotate(peices):
	""" Return
	"""
	#imo_add = None
	#imo_src = None
	imo_res = None
	#power = 0
	
	try:
		imgpath = peices[1]
	except:
		imgpath = ''
	try:
		power = float(peices[2])
	except:
		power = 0.0
	try:
		targval = peices[3]
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


def op_funkyfresh(peices):
	""" Return
	"""
	image_keep = None
	#imo_src = None
	#color = [0, 0, 0]
	
	try:
		imgpath = peices[1]
	except:
		imgpath = ''
	try:
		targval = peices[2]
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


def op_bleach(peices):
	""" Return
	"""
	image_keep = None
	imo_src = None
	
	try:
		imgpath = peices[1]
	except:
		imgpath = ''
	try:
		bleachval = float(peices[2])
	except:
		bleachval = 0.5
	try:
		targval = peices[3]
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


def op_skoo(peices):
	""" Return
	"""
	imo_col = None
	imo_src = None
	imo_dst = None
	colors = []
	
	try:
		colpath = peices[1]
	except:
		colpath = ''
	try:
		numslice = int(peices[2])
	except:
		numslice = 4
	try:
		imgpath = peices[3]
	except:
		imgpath = ''
	try:
		dstpath = peices[4]
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


def op_scotch(peices):
	""" Return
	"""
	image_keep = None
	imo_src = None
	color = [0, 0, 0]
	
	try:
		imgpath = peices[1]
	except:
		imgpath = ''
	#try:
	#	bleachval = float(peices[2])
	#except:
	#	bleachval = float(255)
	try:
		color[0] = float(peices[2])
	except:
		color[0] = 0.5
	try:
		color[1] = float(peices[3])
	except:
		color[1] = 1.0
	try:
		color[2] = float(peices[4])
	except:
		color[2] = 1.0
	try:
		targval = peices[5]
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


def op_tone(peices):
	""" Return
	"""
	image_keep = None
	imo_src = None
	color = [0, 0, 0]
	
	try:
		imgpath = peices[1]
	except:
		imgpath = ''
	try:
		bleachval = float(peices[2])
	except:
		bleachval = 0.5
	try:
		color[0] = float(peices[3])
	except:
		color[0] = 0.5
	try:
		color[1] = float(peices[4])
	except:
		color[1] = 1.0
	try:
		color[2] = float(peices[5])
	except:
		color[2] = 1.0
	try:
		targval = peices[6]
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


def op_greyscale(peices):
	""" Return
	"""
	image_keep = None
	imo_src = None
	
	try:
		imgpath = peices[1]
	except:
		imgpath = ''
	try:
		targval = peices[2]
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
	
	result = image_greyscale(src, srcbox, target)
	if image_keep is not None:
		image_keep.set_path(result)


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


def op_xmark(peices):
	""" Return
	"""
	imo_add = None
	imo_src = None
	imo_res = None
	power = [0, 0]
	
	try:
		imgpath = peices[1]
	except:
		imgpath = ''
	try:
		power[0] = int(peices[2])
	except:
		power[0] = 16
	try:
		power[1] = int(peices[3])
	except:
		power[1] = 16
	try:
		targval = peices[4]
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


def op_grid(peices):
	""" Return
	"""
	imo_add = None
	imo_src = None
	imo_res = None
	power = [4, 4]
	
	try:
		imgpath = peices[1]
	except:
		imgpath = ''
	try:
		power[0] = int(peices[2])
	except:
		power[0] = 16
	try:
		power[1] = int(peices[3])
	except:
		power[1] = 16
	try:
		targval = peices[4]
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


def op_add(peices):
	""" Return
	"""
	imo_add = None
	imo_src = None
	imo_res = None
	print peices
	
	try:
		srcpath = peices[1]
	except:
		srcpath = ''
	try:
		dstpath = peices[2]
	except:
		dstpath = ''
	try:
		feather = float(peices[3])
	except:
		feather = 0.5
	try:
		target = peices[4]
	except:
		target = 'default'
	
	if file_is_image(srcpath) is not True:
		imo_src = imageobject_get(srcpath)
		srcpath = imo_src.path
	
	if file_is_image(dstpath) is not True:
		imo_dst = imageobject_get(dstpath)
		dstpath = imo_dst.path
	
	if len(srcpath) == 0:
		print '%s: src image path is empty!' % (peices[0])
		return
	
	if len(dstpath) == 0:
		print '%s: dst image path is empty!' % (peices[0])
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


def op_subtract(peices):
	""" Return
	"""
	imo_add = None
	imo_src = None
	imo_res = None
	
	try:
		srcpath = peices[1]
	except:
		srcpath = ''
	try:
		dstpath = peices[2]
	except:
		dstpath = ''
	try:
		feather = float(peices[3])
	except:
		feather = 0.5
	try:
		target = peices[4]
	except:
		target = 'default'
	
	if file_is_image(srcpath) is not True:
		imo_src = imageobject_get(srcpath)
		srcpath = imo_src.path
	
	if file_is_image(dstpath) is not True:
		imo_dst = imageobject_get(dstpath)
		dstpath = imo_dst.path
	
	if len(srcpath) == 0:
		print '%s: src image path is empty!' % (peices[0])
		return
	
	if len(dstpath) == 0:
		print '%s: dst image path is empty!' % (peices[0])
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


def op_multiply(peices):
	""" Return
	"""
	#imo_add = None
	#imo_src = None
	imo_res = None
	
	try:
		srcpath = peices[1]
	except:
		srcpath = ''
	try:
		dstpath = peices[2]
	except:
		dstpath = ''
	try:
		feather = float(peices[3])
	except:
		feather = 0.5
	try:
		target = peices[4]
	except:
		target = 'default'
	
	if file_is_image(srcpath) is not True:
		imo_src = imageobject_get(srcpath)
		srcpath = imo_src.path
	
	if file_is_image(dstpath) is not True:
		imo_dst = imageobject_get(dstpath)
		dstpath = imo_dst.path
	
	if len(srcpath) == 0:
		print '%s: src image path is empty!' % (peices[0])
		return
	
	if len(dstpath) == 0:
		print '%s: dst image path is empty!' % (peices[0])
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


def op_zoom(peices):
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
	while i < len(peices):
		if str_match(peices[i], '-i'):
			imgpath = peices[i+1]
			i += 1
		elif str_match(peices[i], '-l'):
			zc[0] = float(peices[i+1])
			zc[1] = float(peices[i+2])
			#zoom_val = True
			i += 2
		#elif str_match(peices[i], '-o'):
		#	targval = peices[i+1]
		#	i += 1
		elif str_match(peices[i], '-m'):
			mode = peices[i+1]
			i += 1
		elif str_match(peices[i], '-z'):
			zoomstart = float(peices[i+1])
			zoomfinish = float(peices[i+2])
			i += 2
		elif str_match(peices[i], '-ct'):
			zoomsteps = int(peices[i+1])
			i += 1
		i += 1
	
	if imgpath is None:
		print 'no image path in peices(%s)' % peices
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
		image_operation('resize -i outzoom.png -w %d -h %d -m %s -o %s' % (srcbox[0], srcbox[1], mode, outimage))
		zoomval -= zoomdelta
	#image_operation('selwipe zoomsel')


def op_resize(peices):
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
	while i < len(peices):
		if str_match(peices[i], '-i'):
			imgpath = peices[i+1]
			i += 1
		elif str_match(peices[i], '-w'):
			wide_val = int(peices[i+1])
			i += 1
		elif str_match(peices[i], '-h'):
			high_val = int(peices[i+1])
			i += 1
		elif str_match(peices[i], '-o'):
			targval = peices[i+1]
			i += 1
		elif str_match(peices[i], '-m'):
			mode_val = peices[i+1]
			i += 1
		i += 1
	
	if imgpath is None:
		print 'no image path in peices(%s)' % peices
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


def tiny_dot(sel, x, y, color=None):
	""" Return
	"""
	if color is None:
		color = [0, 0, 0, 255]
	image_operation('seladdmark %s %d %d %d %d %d %d 0' % (sel, x, y, color[0], color[1], color[2], color[3]))


def adddot(selection, coord, color=None, mark=0):
	if color is None:
		color = [64, 64, 64, 128]
	image_operation('seladdmark %s %d %d %d %d %d %d %d' % (selection, coord[0], coord[1], color[0], color[1], color[2], color[3], mark))


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
			image_operation('selblock %s %d %d %d %d %d %d %d %d %f' % (sel, bpos[0], bpos[1], box[0], box[1], bgcolor[0], bgcolor[1], bgcolor[2], bgcolor[3], radius))
	if color[3] > 0:
			draw_string(sel, val, [bpos[0]+margin[0]/2, bpos[1]+margin[1]/2], color, mono)


def image_operation(line):
	""" Return
	"""
	#print line
	#peices = []
	peices = line_to_vars(line)
#	return
#	vals = line.split(' ')
#	for bit in vals:
#		val = str_strip_whitespace(bit)
#		peices.append(val)
	
#	for bit in peices:
#		print bit
#		if '"' in bit:
#			print 'QUOTATION MARK, OMG!'
#	return
	#print peices

	if len(peices) < 1:
		return None
	if len(peices[0]) < 1:
		return None

	if str_match(peices[0], 'setobj') is True:
		op_setobj(peices)
	elif str_match(peices[0], 'noise') is True:
		op_noise(peices)
	elif str_match(peices[0], 'bleach') is True:
		op_bleach(peices)
	elif str_match(peices[0], 'greyscale') is True:
		op_greyscale(peices)
	elif str_match(peices[0], 'tone') is True:
		op_tone(peices)
	elif str_match(peices[0], 'scotch') is True:
		op_scotch(peices)
	elif str_match(peices[0], 'skoo') is True:
		op_skoo(peices)
	elif str_match(peices[0], 'funkyfresh') is True:
		op_funkyfresh(peices)
	elif str_match(peices[0], 'rotate') is True:
		op_rotate(peices)
	elif str_match(peices[0], 'resize') is True:
		op_resize(peices)
	elif str_match(peices[0], 'add') is True:
		op_add(peices)
	elif str_match(peices[0], 'subtract') is True:
		op_subtract(peices)
	elif str_match(peices[0], 'multiply') is True:
		op_multiply(peices)
	elif str_match(peices[0], 'grid') is True:
		op_grid(peices)
	elif str_match(peices[0], 'xmark') is True:
		op_xmark(peices)
	elif str_match(peices[0], 'zoom') is True:
		op_zoom(peices)
	elif str_match(peices[0], 'selset') is True:
		op_selset(peices)
	elif str_match(peices[0], 'selappend') is True:
		op_selappend(peices)
	elif str_match(peices[0], 'seladdmark') is True:
		op_seladdmark(peices)
	elif str_match(peices[0], 'selgrid') is True:
		op_selgrid(peices)
	elif str_match(peices[0], 'selwipe') is True:
		op_selwipe(peices)
	elif str_match(peices[0], 'selremovecolor') is True:
		op_selremovecolor(peices)
	elif str_match(peices[0], 'selbounds') is True:
		op_selbounds(peices)
	elif str_match(peices[0], 'selrotate') is True:
		op_selrotate(peices)
	elif str_match(peices[0], 'selsquare') is True:
		op_selsquare(peices)
	elif str_match(peices[0], 'selblock') is True:
		op_selblock(peices)
	elif str_match(peices[0], 'sellumrange') is True:
		op_sellumrange(peices)
	elif str_match(peices[0], 'selcrop') is True:
		op_selcrop(peices)
	elif str_match(peices[0], 'selbloom') is True:
		op_selbloom(peices)
	elif str_match(peices[0], 'selsave') is True:
		op_selsave(peices)
	else:
		print('unrecognized line: %s' % line)
