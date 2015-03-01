# -*- coding: utf-8 -*-
"""wIcon library:

"""

#from common import matchStr, selections
from PIL import Image
import common
from q_math import *


def getselsize(srcpath):
	""" Return size of selObject, the name is provided as an argument to the function
	"""
	srcsel = selection_get(srcpath)
	if len(srcsel.coords) == 0:
		return None
	_max = [None, None]
	for sc in srcsel.coords:
		for i in range(0, 2):
			if _max[i] is None:
				_max[i] = sc.xy[i]
			else:
				if sc.xy[i] > _max[i]:
					_max[i] = sc.xy[i]
	for i in range(0, 2):
		_max[i] += 1
	return _max


def poslen(pos):
	""" Returns the vector length of a vec2 used by SelCoord
	"""
	fpos = [float(pos[0]), float(pos[1])]
	plen = math.sqrt(fpos[0]*fpos[0] + fpos[1]*fpos[1])
	return plen

stLumRange = 0
#stColRange = stLumRange+1
#stSquare = stColRange+1


### represents a coord in a SelectionObject.  It is not stored as an array, it is just on a list, which means you can have overlapping pixels.  This gets handled at blit-time.
class SelCoord:
	def __init__(self, coord, color):
		""" Sets self values of xy and color to provided values
		"""
		### set to coord value, these are not exact pixel coordinates - just picture an infinite cartesian plane.  You are just assigning a dot on the plane, but that may not be what shows up on the image.
		self.xy = coord
		### set to color value, either 3 or 4 channels
		self.color = color
		
	def color_update(self, color):
		""" Modifies self.color to provided value
		"""
		if len(self.color) == 3:
			#solid
			if len(color) == 4:
				#not so solid
				o_color = []
				for val in self.color:
					o_color.append(val)
				smooth = float(float(color[3]) / 255.0)
				asmoth = 1.0 - smooth
				src_color = [int(float(o_color[0])*asmoth), int(float(o_color[1])*asmoth), int(float(o_color[2])*asmoth)]
				dst_color = [int(float(color[0])*smooth), int(float(color[1])*smooth), int(float(color[2])*smooth)]
				self.color = [src_color[0]+dst_color[0], src_color[1]+dst_color[1], src_color[2]+dst_color[2]]
			else:
				self.color = [color[0], color[1], color[2]]
		elif len(self.color) == 4:
			#transparent
			if len(color) == 4:
				#not so solid
				o_color = []
				for val in self.color:
					o_color.append(val)
				smooth = float(float(color[3]) / 255.0)
				asmoth = 1.0 - smooth
				src_color = [int(float(o_color[0])*asmoth), int(float(o_color[1])*asmoth), int(float(o_color[2])*asmoth)]
				dst_color = [int(float(color[0])*smooth), int(float(color[1])*smooth), int(float(color[2])*smooth)]
				self.color = [src_color[0]+dst_color[0], src_color[1]+dst_color[1], src_color[2]+dst_color[2], o_color[3]]
			else:
				alpha = self.color[3]
				self.color = [color[0], color[1], color[2], alpha]


class SelectionObject:
	""" represents a buffer of pixels to be written or handled in some way.  Think clip-board.
	"""
	def __init__(self, name):
		""" Sets self.name to argument and initializes coords, type, bounds, clamp
		"""
		self.name = name
		self.coords = []
		self.type = stLumRange
		self.bounds = []
		self.clamp = False
		#self.color = [0,0,0]
		#self.ran = 0
		
	def coord_get(self, xy):
		""" Returns a SelCoord object if it can find one that matches supplied xy
		"""
		print len(self.coords)
		for cor in self.coords:
			if cor.xy[0] == xy[0] and cor.xy[1] == xy[1]:
				return cor
		return None
	
	def coord_add(self, coord):
		""" Appends value of coord to self.coords (coord is a SelCoord)
		if self.clamp is True it will test if coord is in self.bounds (self.bounds is a 2 length array of 2 length arrays (int values))
		"""
		#sc = self.coord_get(coord.xy)
		#if(sc is not None):
		#	sc.color_update(coord.color)
		#	return
		#for coord in self.coords:
		#	if(coord[0]==x and coord[1]==y):
		#		return
		if self.clamp:
			addc = True
			for i in range(0, 2):
				if coord.xy[i] >= self.bounds[i]:
					addc = False
				if coord.xy[i] < 0:
					addc = False
				if addc:
					self.coords.append(coord)
		else:
			#print 'ac %s' % (str(coord.xy))
			self.coords.append(coord)
	
	## def setType(self, path):
	## 	""" Sets path to type (type is string)
	## 	 FIXME: What is this used for?
	## 	"""
	## 	if len(path) == 0:
	## 		self.path = None
	## 		print('imgObj \'%s\' set to \'%s\'' % (self.name, self.path))
	## 		return
	## 	self.path = path
	## 	print('imgObj \'%s\' set to \'%s\'' % (self.name, self.path))

	## boudns is 2 length int list
	def size(self, bounds, clamp):
		""" Sets self.bounds and self.clamp to supplied values
		"""
		self.bounds = bounds
		self.clamp = clamp

	## SelectionObject.mark
	# calls \ref SelectionObject.coord_add
	# \ref SelCoord
	def mark(self, power, size, color, x=False):
		""" Adds SelCoords to self.coords based on provided power, size, color
		 if x is true, adds the mark in the shape of an x
		"""
		pos = [int(power[0]), int(power[1])]
		if size == 0:
			sc = SelCoord([pos[0], pos[1]], color)
			self.coord_add(sc)
			return
		sz = size
		if size < 0:
			sz = -size
		if x is True:
			keep = sz
			while keep > 0:
				sc = SelCoord([pos[0]-keep, pos[1]-keep], color)
				self.coord_add(sc)
				sc = SelCoord([pos[0]+keep, pos[1]-keep], color)
				self.coord_add(sc)
				sc = SelCoord([pos[0]-keep, pos[1]+keep], color)
				self.coord_add(sc)
				sc = SelCoord([pos[0]+keep, pos[1]+keep], color)
				self.coord_add(sc)
				keep -= 1
		else:
			for i in range(-sz, sz+1):
				for j in range(-sz, sz+1):
					sc = SelCoord([pos[0]+i, pos[1]+j], color)
					self.coord_add(sc)

	def line(self, v1, v2, color):
		v3 = vec2sub(v2, v1)
		vlen = vec2len(v3)
		segs = int(vlen*8.0)
		#if(segs<5):
		#	segs = 5
		if segs == 0:
			return
		v4 = vec2scale(v3, 1.0/float(segs))
		self.mark(v1, 0, color)
		v3 = vec2copy(v1)
		for i in range(0, segs):
			v3 = vec2add(v3, v4)
			self.mark(v3, 0, color)

	def grid(self, cols, rows, bounds, color):
		""" Adds coords to self, lines spaced distances apart by int values cols and rows (FIXME, variable names misleading) within space defined by bounds (2 length int array) of color (any value accepted by SelCoord)
		"""
		#i = 0
		#j = 0
		wide = bounds[0]
		high = bounds[1]
		#half = srcbox[0]/2
		#block = int(half/wide)
		if cols is not None:
						i = 0
						while i < wide:
								for j in range(0, high):
										#print('col:%d,%d' % (j,i))
										sc = SelCoord([i, j], color)
										self.coord_add(sc)
								i += cols

		if rows is not None:
						i = 0
						while i < high:
								for j in range(0, wide):
										#print('row:%d,%d' % (j,i))
										sc = SelCoord([j, i], color)
										self.coord_add(sc)
								i += rows

	def block(self, start, size, radius, color):
		""" Adds a block to SelectionObject starting and start pixels of size
		 FIXME: need to review function
		"""

		#print start
		_min_x = start[0]
		_min_y = start[1]
		_max_x = _min_x+size[0]
		_max_y = _min_y+size[1]
		_min_rad_x = _min_x
		_min_rad_y = _min_y
		_max_rad_x = _max_x
		_max_rad_y = _max_y
		if radius is not None:
			_min_rad_x = _min_x+radius
			_min_rad_y = _min_y+radius
			_max_rad_x = _max_x-radius-1
			_max_rad_y = _max_y-radius-1
		j = _min_y
		#i = _min_x
		while j < _max_y:
			i = _min_x
			while i < _max_x:
					if (i >= _min_rad_x) and (i <= _max_rad_x) and (j >= _min_rad_y) and (j <= _max_rad_y):
							sc = SelCoord([i, j], color)
							self.coord_add(sc)
					else:
							if (i >= _min_rad_x) and (i <= _max_rad_x) or (j >= _min_rad_y) and (j <= _max_rad_y):
									sc = SelCoord([i, j], color)
									self.coord_add(sc)
							else:
									if radius is not None:
											#upper left
											if (i < _min_rad_x) and (j < _min_rad_y):
													diff = [_min_rad_x - i, _min_rad_y - j]
													if poslen(diff) <= radius:
															sc = SelCoord([i, j], color)
															self.coord_add(sc)
											#bottom left
											if (i < _min_rad_x) and (j > _max_rad_y):
													diff = [_min_rad_x - i, _max_rad_y - j]
													if poslen(diff) <= radius:
															sc = SelCoord([i, j], color)
															self.coord_add(sc)
											#upper right
											elif (i > _max_rad_x) and (j < _min_rad_y):
													diff = [_max_rad_x - i, _min_rad_y - j]
													if poslen(diff) <= radius:
															sc = SelCoord([i, j], color)
															self.coord_add(sc)
											#bottom right
											elif (i > _max_rad_x) and (j > _max_rad_y):
													diff = [_max_rad_x - i, _max_rad_y - j]
													if poslen(diff) <= radius:
															sc = SelCoord([i, j], color)
															self.coord_add(sc)
					i += 1
			j += 1
			
	def crop(self, start, size):
		""" given a start position and size, should remove any extraneous pixels
		"""
		cruft = []
		for sc in self.coords:
			if (sc.xy[0] < start[0]) or (sc.xy[1] < start[1]) or (sc.xy[0] > (start[0]+size[0])) or (sc.xy[1] > (start[1]+size[1])):
				cruft.append(sc)
		for sc in cruft:
			self.coords.remove(sc)

	def remove_color(self, color):
		""" Searches through self.coords for matches to color, and removes those coords
		"""
		cruft = []
		for sc in self.coords:
					if common.color_match(sc.color, color):
						cruft.append(sc)
			#if(sc.color[0]==color[0] and sc.color[1]==color[1] and sc.color[2]==color[2]):
				#cruft.append(sc)
		for sc in cruft:
			self.coords.remove(sc)

	def wipe(self):
		""" Empties coords array
		FIXME: possibly reset other values?
		"""
		del self.coords[:]

	## returns a list where list item 0 is _minimum coords and list item 1 is _maximum coords
	def getbounds(self):
		""" returns self.coords size, should be fairly resilient
		FIXME: Test against really really off-center renders (far from 0,0)
		"""
		_min = [None, None]
		_max = [None, None]
		for coord in self.coords:
			for i in range(0, 2):
				if _min[i] is None:
					_min[i] = coord.xy[i]
					_max[i] = coord.xy[i]
				if coord.xy[i] < _min[i]:
					_min[i] = coord.xy[i]
				if coord.xy[i] > _max[i]:
					_max[i] = coord.xy[i]
		if _max[0] is not None:
			_max[0] += 1
		if _max[1] is not None:
			_max[1] += 1
		return [_min, _max]

	def get_coords(self, _min, _max, expect_size=None, remove=True):
		items = []
		#cruft = []
		deletelist = []
		get_ct = 0
		coords_size = len(self.coords)
		k = 0
		while k < coords_size:
			coord = self.coords[k]
		#for coord in self.coords:
			good = 0
			for j in range(0, 2):
				if (coord.xy[j] >= _min[j]) and (coord.xy[j] < _max[j]):
					good += 1
			if good == 2:
				items.append(coord)
				get_ct += 1
				if remove:
					#cruft.append(coord)
					deletelist.append(k)
			if expect_size is not None:
				if get_ct >= expect_size:
					k = coords_size - 1
			k += 1
		if remove:
			#for sc in items:
			#	self.coords.remove(sc)
			k = 0
			for val in deletelist:
				coord = self.coords.pop(val-k)
				k += 1
		#print 'finished get_coords %s %s' % (_min, _max)
		return items

	#def remove_coords(self,_min,_max):

	def get_average_color(self, _min=None, _max=None, expect_size=None, remove=True):
		""" returns average color, should be fairly resilient
		FIXME:
		"""
		bc = [0, 0, 0]
		ct = 0
		if _min is None or _max is None:
			for coord in self.coords:
				for i in range(0, 3):
					bc[i] += coord.color[i]
				ct += 1
		else:
			coords = self.get_coords(_min, _max, expect_size, remove)
			for coord in coords:
				for i in range(0, 3):
					bc[i] += coord.color[i]
				ct += 1
		if ct > 0:
			for i in range(0, 3):
				bc[i] /= ct
			return bc
		return [255, 255, 255]

	## SelectionObject.save
	def save(self, outimg, bbox, color):
		""" Saves the selection contents as outimg.
		PIL / Pillow handles the writing of the file (obviously)
		"""
		media_ct = 0
		if outimg is None:
			outimg = 'out%04d.png' % (media_ct+1)
			while common.file_exists(outimg) is True:
				outimg = 'out%04d.png' % (media_ct+1)
				if common.file_exists(outimg) is True:
					media_ct += 1

		_min = [None, None]
		_max = [None, None]
		if bbox is None and self.clamp is False:
			_min, _max = self.getbounds()
		else:
			_min = [0, 0]
			_max = [16, 16]
			if bbox is not None:
				_max = [bbox[0], bbox[1]]
			if self.clamp is True:
				_max = [self.bounds[0], self.bounds[1]]
		
		if _min[0] is None or _min[1] is None:
			return None
		
		print('_min %d,%d' % (_min[0], _min[1]))
		print('_max %d,%d' % (_max[0], _max[1]))
		
		bounds = [_max[0]-_min[0], _max[1]-_min[1]]
		white = Image.new('RGBA', bounds, color)
		
		for coord in self.coords:
				#print('coord %d %d' % (coord.xy[0]-_min[0],coord.xy[1]-_min[1]))
				#print('color %d %d %d' % (coord.color[0],coord.color[1],coord.color[2]))
				power = [coord.xy[0]-_min[0], coord.xy[1]-_min[1]]
				if (power[0] >= 0) and (power[0] < bounds[0]) and (power[1] >= 0) and (power[1] < bounds[1]):
						if len(coord.color) <= 3:
								white.putpixel((coord.xy[0]-_min[0], coord.xy[1]-_min[1]), (coord.color[0], coord.color[1], coord.color[2], 255))
						else:
								o_color = white.getpixel((coord.xy[0]-_min[0], coord.xy[1]-_min[1]))
								#print o_color
								color = coord.color
								#print len(o_color)
								#print len(color)
								smooth = float(float(color[3]) / 255.0)
								asmoth = 1.0 - smooth
								src_color = None
								dst_color = None
								if len(o_color) == 3:
									src_color = [int(float(o_color[0])*asmoth), int(float(o_color[1])*asmoth), int(float(o_color[2])*asmoth), 255]
								elif len(o_color) == 4:
									src_color = [int(float(o_color[0])*asmoth), int(float(o_color[1])*asmoth), int(float(o_color[2])*asmoth), int(float(o_color[3])*asmoth)]
								if len(color) == 3:
									dst_color = [int(float(color[0])*smooth), int(float(color[1])*smooth), int(float(color[2])*smooth), 255]
								elif len(color) == 4:
									dst_color = [int(float(color[0])*smooth), int(float(color[1])*smooth), int(float(color[2])*smooth), int(float(color[3])*smooth)]
								#print src_color
								#print dst_color
								res_color = [src_color[0]+dst_color[0], src_color[1]+dst_color[1], src_color[2]+dst_color[2], src_color[3]+dst_color[3]]
								#print res_color
								white.putpixel((coord.xy[0]-_min[0], coord.xy[1]-_min[1]), (res_color[0], res_color[1], res_color[2], res_color[3]))
								#print '%d %d - %d %d %d %d' % (coord.xy[0],coord.xy[1],coord.color[0],coord.color[1],coord.color[2],coord.color[3])
		white.save(outimg)
		return outimg


def selection_find(name):
	""" Search through selections array (an array that grows with new selections, and is comprised of SelectionObjects)
	Does not create new selections, will return None if not found
	"""

	for sel in common.selections:
		if common.str_match(sel.name, name) is True:
			return sel
	return None


def selection_get(name):
	""" Search through selections array (an array that grows with new selections, and is comprised of SelectionObjects)
	Creates new selections, will return the new SelectionObject
	"""
	for sel in common.selections:
		if common.str_match(sel.name, name) is True:
			return sel
	sel = SelectionObject(name)
	common.selections.append(sel)
	return common.selections[len(common.selections)-1]
