#!/usr/bin/python
## raster.py Brad Newbold;
# version 0.0.1a
# attempts to extract files from capcom .arc files and write them out with appropriate file extensions
# todo: must check to make sure we're not overwriting files?
#

#import os
#import sys
#import operator
#import struct
#import zlib
#import math
#import binascii
#from common import *
#from handy import *
from wudanicon import *
from q_math import *
from selection import selection_get
#from q_shared import *
#from datetime import datetime

fScale = 8.0
isometric = True
xc = 0
yc = 1
zc = 2
worldmat = []
_wires = False
_solid = False
_ogre3d = False
shfloats = []
_lod = 1


## research use
class BlitCoord:
	def __init__(self, pos, uvw, color):
		self.pos = pos
		self.uvw = uvw
		self.color = color
		self.rastered = False
	
	def __getitem__(self, i):
		return self.pos[i]
	
	def getpos2(self):
		return self.pos[2]
	
	def update_uvw_color(self, uvw, color):
		self.uvw = uvw
		self.color = color
		#self.color[3] = 255
	
	def blend_color(self, color):
		fval = float(self.color[3]) / 255.0
		o_color = [float(self.color[0])*fval, float(self.color[1])*fval, float(self.color[2])*fval, 255]
		#if(o_color[3]==255):
		smooth = float(color[3]) / 255.0
		asmoth = 1.0 - smooth
		src_color = [int(float(o_color[0])*asmoth), int(float(o_color[1])*asmoth), int(float(o_color[2])*asmoth)]
		dst_color = [int(float(color[0])*smooth), int(float(color[1])*smooth), int(float(color[2])*smooth)]
		res_color = [src_color[0]+dst_color[0], src_color[1]+dst_color[1], src_color[2]+dst_color[2], color[3]]
		self.color = res_color
		#else:
		#	smooth = float(color[3]) / 255.0
		#	for i in range(0,3):
		#		self.color[i] += (int(float(color[i]) * smooth))
		#		if(self.color[i]>255):
		#			self.color[i] = 255
		#	self.color[3] += color[3]
		#	if(self.color[3]>255):
		#		self.color[3] = 255

	def rastered(self):
		self.rastered = True


## provided a list of coords (\ref BlitCoord) and a background color, determine a final color
# called by \ref BlitMatrix.blit_coords
def get_final_color(coords, bcolor=None, depth=None):
	if bcolor is None:
		bcolor = [255.0, 255.0, 255.0, 255]
	if len(coords) == 0:
		return None
	fbc = BlitCoord(coords[0].pos, coords[0].uvw, coords[0].color)
	#print '=-=-=-'
	#dlist = []
	color = [bcolor[0], bcolor[1], bcolor[2], bcolor[3]]
	coords.sort(key=BlitCoord.getpos2, reverse=True)
	ct = 0
		#if(o_color[3]==255):
	for cor in coords:
		if depth is not None:
			if cor[2] <= depth+64.0:
				#print cor.pos
				#dlist.append(cor.pos[2])
				#print cor.uvw
				alpha = float(color[3]) / 255.0
				o_color = [float(color[0])*alpha, float(color[1])*alpha, float(color[2])*alpha, 255]
				smooth = float(cor.color[3]) / 255.0
				asmoth = 1.0 - smooth
				src_color = [int(float(o_color[0])*asmoth), int(float(o_color[1])*asmoth), int(float(o_color[2])*asmoth)]
				dst_color = [int(float(cor.color[0])*smooth), int(float(cor.color[1])*smooth), int(float(cor.color[2])*smooth)]
				color = [src_color[0]+dst_color[0], src_color[1]+dst_color[1], src_color[2]+dst_color[2], color[3]]
				#print cor.color
				#print cor.uvw
				ct += 1
		else:
			alpha = float(color[3]) / 255.0
			o_color = [float(color[0])*alpha, float(color[1])*alpha, float(color[2])*alpha, 255]
			smooth = float(cor.color[3]) / 255.0
			asmoth = 1.0 - smooth
			src_color = [int(float(o_color[0])*asmoth), int(float(o_color[1])*asmoth), int(float(o_color[2])*asmoth)]
			dst_color = [int(float(cor.color[0])*smooth), int(float(cor.color[1])*smooth), int(float(cor.color[2])*smooth)]
			color = [src_color[0]+dst_color[0], src_color[1]+dst_color[1], src_color[2]+dst_color[2], color[3]]
			ct += 1
	if ct == 0:
		return None
	for i in range(0, 4):
		color[i] = int(color[i])
		if color[i] > 255:
			color[i] = 255
	fbc.update_uvw_color(fbc.uvw, color)
	return fbc


## research use
# coords list populated by \ref BlitCoord
class BlitMatrix:
	def __init__(self, selname='blitmatrix'):
		self.min = None
		self.max = None
		self.size = None
		self.coords = []
		self.matrix = []
		self.tmatrix = []
		self.selname = selname
		self.ofs = [960, 540]
		self.sel = selection_get(self.selname)

	## override for getitem provide pixel pos
	# memberOf BlitMatrix
	def __getitem__(self, i):
		if (self.size is None) or (self.min is None) or (self.max is None):
			return None
		_t = False
		if len(i) == 3:
			_t = i[2]
		try:
			if _t is False:
				#print i
				#pos = [i[0]-self.min[0],i[1]-self.min[1]]
				pos = [int(i[0]-self.min[0]), int(i[1]-self.min[1])]
				if pos[0] > self.size[0] or pos[0] < 0:
					return None
				if pos[1] > self.size[1] or pos[1] < 0:
					return None
				#print self.matrix[pos[0]][pos[1]]
				return self.matrix[pos[0]][pos[1]]
			else:
				pos = [int(i[0]-self.min[0]), int(i[1]-self.min[1])]
				if pos[0] > self.size[0] or pos[0] < 0:
					return None
				if pos[1] > self.size[1] or pos[1] < 0:
					return None
				#print self.matrix[pos[0]][pos[1]]
				return self.tmatrix[pos[0]][pos[1]]
		except:
			print '!!!'
			pass
		return None

	def _selname(self, val):
		self.selname = val

	##
	# memberOf BlitMatrix
	# called by \ref BlitMatrix.blit_coords
	def matrix_update(self, i, bc, _t=False):
		if self.size is None or self.min is None or self.max is None:
			return False
		#print i
		#try:
		pos = [int(i[0]-self.min[0]), int(i[1]-self.min[1])]
		#print pos
		#print self.size
		#print pos
		if pos[0] >= self.size[0] or pos[0] < 0:
			print '!!!'
			return False
		if pos[1] >= self.size[1] or pos[1] < 0:
			print '!!!#'
			return False
		if _t is False:
			self.matrix[pos[0]][pos[1]] = bc
		else:
			self.tmatrix[pos[0]][pos[1]] = bc
		return True

	##
	# memberOf BlitMatrix
	def matrix_add_coord(self, i, bc):
		if self.size is None or self.min is None or self.max is None:
			return False
		pos = [int(i[0]-self.min[0]), int(i[1]-self.min[1])]
		if pos[0] >= self.size[0] or pos[0] < 0:
			print '!!!=-='
			return False
		if pos[1] >= self.size[1] or pos[1] < 0:
			print '!!!#=-='
			return False
		self.tmatrix[pos[0]][pos[1]].append(bc)
		return True

	## add \ref BlitCoord
	# calls \ref BlitMatrix::check_bounds
	# memberOf BlitMatrix
	def add_coord(self, pos, uvw, color, flip=False):
		pval = pos
		if flip:
			pval[1] = -pos[1]
		#val = self[pos[0],pos[1]]
		#for bc in self.coords:
		#	if(bc.pos[0]==pos[0] and bc.pos[1]==pos[1]):
		#		if(uvw[2]>bc.uvw[2]):
		#			bc.update_uvw_color(uvw,color)
		#		return
		if color[3] >= 255:
			pass
			#print color
		else:
			pass
			#print color
		#if(pval[0]==-309 and pval[1]==-428):
		#	print '=-=-=-'
		#	print uvw
		#	print pval
		#	print color
		self.check_bounds(pval)
		self.coords.append(BlitCoord(pval, uvw, color))
		#inp = [int(pos[0]),int(pos[1])]

	## builds bounds against coords on list
	# memberOf BlitMatrix
	def check_bounds(self, pos):
		#print pos
		#print 'self.min %s' % (self.min)
		#print 'self.max %s' % (self.max)
		if self.min is None or self.max is None:
			self.min = vec2add(pos, [-1, -1])
			self.max = vec2add(pos, [1, 1])
			#print '!!!'
			return
		#print pos
		#print self.min
		if pos[0] < self.min[0]:
			self.min[0] = pos[0]-1
		if pos[1] < self.min[1]:
			self.min[1] = pos[1]-1
		if pos[0] > self.max[0]:
			self.max[0] = pos[0]+1
		if pos[1] > self.max[1]:
			self.max[1] = pos[1]+1

	## primary blit -
	# bounds needs to exist first
	# calls \ref BlitMatrix::matrix_add_coord
	# calls \ref get_final_color
	# calls \ref adddot
	# calls \ref BlitCoord.blend_color
	# calls \ref SelectionObject.mark
	# memberOf BlitMatrix
	def blit_coords(self):
		#coordwatch = [-755, 25]
		#print self.max
		#print self.min
		#return
		if self.min is None or self.max is None:
			return
		self.size = [int(self.max[0]-self.min[0])+1, int(self.max[1]-self.min[1])+1]
		print self.size
		for i in range(0, self.size[0]):
			self.matrix.append([])
			col = list_getlast(self.matrix)
			for j in range(0, self.size[1]):
				col.append(None)
		for i in range(0, self.size[0]):
			self.tmatrix.append([])
			col = list_getlast(self.tmatrix)
			for j in range(0, self.size[1]):
				col.append([])
		#remlist = []
		i = 0
		print 'coords pre-blit: %d' % (len(self.coords))
		for bc in self.coords:
			#if(i==91):
			#	print 'coord: %d' % (i)
			#print bc.pos
			if bc.color[3] == 255:
				val = self[bc.pos[0], bc.pos[1], False]
				if val is None:
					if self.matrix_update([bc.pos[0], bc.pos[1]], bc):
						pass
				else:
					#existing uvw is actual depth val, not a line
					if val.uvw is not None and bc.uvw is not None:
						if bc.uvw[2] < val.uvw[2]:
							pass
							self[bc.pos[0], bc.pos[1]].update_uvw_color(bc.uvw, bc.color)
					elif val.uvw is not None and bc.uvw is None:
						pass
					elif val.uvw is None and bc.uvw is not None:
						self[bc.pos[0], bc.pos[1]].update_uvw_color(bc.uvw, bc.color)
					elif val.uvw is None and bc.uvw is None:
						#self[bc.pos[0],bc.pos[1]].update_uvw_color(bc.uvw,bc.color)
						self[bc.pos[0], bc.pos[1]].blend_color(bc.color)
						#self[bc.pos[0],bc.pos[1]].update_uvw_color(bc.uvw,[bc.color[0],bc.color[1],bc.color[2],255])
					else:
						pass
				#remlist.append(i)
			else:
				self.matrix_add_coord([bc.pos[0], bc.pos[1]], bc)
			i += 1
		#print 'length of remove list is: %d' % (len(remlist))
		#i = len(remlist)-1
		#while(i >= 0):
		#	val = remlist[i]
		#	del self.coords[val]
		#	i -= 1
		
		#print 'len of coords list, post blit: %d' % (len(self.coords))
		for col in self.tmatrix:
			for items in col:
				if len(items) == 0:
					pass
				elif len(items) >= 1:
					val = self[items[0].pos[0], items[0].pos[1], False]
					#if(val is not None):
						#print '[%d, %d, %f]' % (val.pos[0],val.pos[1],val.uvw[2])
						#print items[0].pos
					bcolor = [255.0, 255.0, 255.0, 255]
					depth = None
					if val is not None:
						bcolor = [float(val.color[0]), float(val.color[1]), float(val.color[2]), 255]
						#depth = val.pos[2]
					bc = get_final_color(items, bcolor, depth)
					
					if bc is not None:
						if val is None:
							if self.matrix_update([bc.pos[0], bc.pos[1], False], bc):
								pass
						else:
							#existing uvw is actual depth val, not a line
							if val.uvw is not None and bc.uvw is not None:
								if bc.uvw[2] < val.uvw[2]:
									self[bc.pos[0], bc.pos[1], False].update_uvw_color(bc.uvw, bc.color)
							elif val.uvw is not None and bc.uvw is None:
								pass
								self[bc.pos[0], bc.pos[1], False].update_uvw_color(bc.uvw, bc.color)
							elif val.uvw is None and bc.uvw is not None:
								self[bc.pos[0], bc.pos[1], False].update_uvw_color(bc.uvw, bc.color)
							elif val.uvw is None and bc.uvw is None:
								pass
								#self[bc.pos[0],bc.pos[1]].update_uvw_color(bc.uvw,bc.color)
								#self[bc.pos[0],bc.pos[1]].blend_color(bc.color)
								#self[bc.pos[0],bc.pos[1]].update_uvw_color(bc.uvw,[bc.color[0],bc.color[1],bc.color[2],255])
							else:
								pass

		for col in self.matrix:
			for bc in col:
				if bc is not None:
					self.sel.mark([bc.pos[0]+self.ofs[0], bc.pos[1]+self.ofs[1]], 0, bc.color)


## Used inside of RasterObject
class RasterTriangle:
	## RasterTriangle.__init__
	# calls \ref raster_getscreencoord
	# - Vector math usage -
	# essentially ignores the normals passed and does flat shading.  This is because it doesn't do Gouraud shading, yet.  Instead it calculates the normal based on the triangle coords and fills in a bright variable.
	def __init__(self, v0, v1, v2, vn0, vn1, vn2):
		self.vw = [VectorCopy(v0), VectorCopy(v1), VectorCopy(v2)]
		self.v = [raster_getscreencoord(v0), raster_getscreencoord(v1), raster_getscreencoord(v2)]
		self.vn = [VectorCopy(vn0), VectorCopy(vn1), VectorCopy(vn2)]
		self.vne = [None, None, None]
		#print 'vert normals: %s' % (self.vn)
		for i in range(0, 3):
			self.vne[i] = raster_getscreencoord(VectorMA(self.vw[i], 1.5, VectorNormalize(self.vn[i])))
		vnp = VectorAdd(vn0, vn1)
		vnp = VectorAdd(vnp, vn2)
		vnp = VectorNormalize(vnp)
		vall = VectorCopy(self.vw[0])
		for i in range(1, 3):
			vall = VectorAdd(vall, self.vw[i])
		vall[0] /= 3.0
		vall[1] /= 3.0
		vall[2] /= 3.0
		self.vall = vall

		#self.v[0][2] = 0.0
		#self.v[1][2] = 0.0
		#self.v[2][2] = 0.0
		#print self.vw
		#print self.v
		
		self.bis = [None, None, None]
		self.normal = None
		#self.bisw = [tri_getbisectvert(self.vw[1],self.vw[2],self.vw[0]),tri_getbisectvert(self.vw[0],self.vw[2],self.vw[1]),tri_getbisectvert(self.vw[0],self.vw[1],self.vw[2])]
		#self.bis = [raster_getscreencoord(self.bisw[0]),raster_getscreencoord(self.bisw[1]),raster_getscreencoord(self.bisw[2])]
		#print self.bisw
		#print self.bis
		self.edge1 = vec2sub(self.v[1], self.v[0])
		self.edge2 = vec2sub(self.v[2], self.v[0])
		self.deep1 = self.v[1][2] - self.v[0][2]
		self.deep2 = self.v[2][2] - self.v[0][2]
		self.normal = CrossProduct(VectorNormalize(VectorSubtract(self.vw[1], self.vw[0])), VectorNormalize(VectorSubtract(self.vw[2], self.vw[0])))
		self.normal = VectorNormalize(self.normal)
		#print self.vn
		#print '%f\t%f\t%f' % (vnp[0],vnp[1],vnp[2])
		#print '%f\t%f\t%f' % (self.normal[0],self.normal[1],self.normal[2])
		dotp = DotProduct(vnp, self.normal)
		if dotp < 0.0:
			self.normal = VectorInverse(self.normal)
		self.nend = VectorMA(self.vall, 1.5, self.normal)
		self.vall = raster_getscreencoord(self.vall)
		self.nend = raster_getscreencoord(self.nend)
		#print '%f\t%f\t%f' % (self.normal[0],self.normal[1],self.normal[2])
		self.bright = DotProduct([0.0, 0.0, -1.0], self.normal)
		if self.bright < 0.0:
			self.bright = -self.bright
		#print self.bright

		#print VectorLength(VectorSubtract(self.bis[0],self.v[0]))
		#print VectorLength(VectorSubtract(self.bis[1],self.v[1]))
		#print VectorLength(VectorSubtract(self.bis[2],self.v[2]))
		self.blits = []

	## RasterTriangle.blit_bisects
	# not actually used, but could add dots at triangle bisects
	# \ref adddot
	def blit_bisects(self, selname):
		adddot(selname, self.bis[0], [255, 0, 0, 255], 1)
		adddot(selname, self.bis[1], [255, 0, 0, 255], 1)
		adddot(selname, self.bis[2], [255, 0, 0, 255], 1)

	## RasterTriangle.go_coord
	# called by \ref RasterObject.blit_triangle
	# research use
	def go_coord(self, coord):
		v0 = VectorCopy(self.v[0])
		v1 = VectorCopy(self.v[1])
		v2 = VectorCopy(self.v[2])
		v0[2] = 0.0
		v1[2] = 0.0
		v2[2] = 0.0
		#print 'go_coord'
		#print coord
		#b0 = VectorSubtract(self.bis[0],v0)
		bis = [None, None, None]
		if self.bis[1] is None:
			self.bis[1] = tri_getbisectvert(v0, v2, v1)
		bis[1] = self.bis[1]
		if self.bis[2] is None:
			self.bis[2] = tri_getbisectvert(v0, v1, v2)
		bis[2] = self.bis[2]
		#tri_getbisectvert(self.vw[1],self.vw[2],self.vw[0])
		#bis[1] = tri_getbisectvert(v0,v2,v1)
		#bis[2] = tri_getbisectvert(v0,v1,v2)
		#b1 = VectorSubtract(self.v[1],bis[1])
		#b2 = VectorSubtract(self.v[2],bis[2])
		b1 = VectorSubtract(v1, bis[1])
		b2 = VectorSubtract(v2, bis[2])
		#b0[2] = 0.0
		#b1[2] = 0.0
		#b2[2] = 0.0
		edge0 = vec2sub(coord, v0)
		#if(is_tinyfloat(self.edge1[0])):
		#	if(is_tinyfloat(self.edge2[0])):
		#		#to small to be seen!
		#		return False
		#	u = edge0[0]/self.edge2[0]
		#	if(u>1.0 or u<0.0):
		#		return False
		#	if(is_tinyfloat(self.edge1[1])):
		#		return False
		#	v = (edge0[1]-self.edge1[1]*u)/self.edge2[1]
		#	if(v<0.0):
		#		return False
		#	if(u+v>1.0):
		#		return False
		#	return True
		vlen = vec2len(b1)
		ulen = vec2len(b2)
		if is_tinyfloat(ulen):
			return None
		if is_tinyfloat(vlen):
			return None
		#print vlen
		#print ulen
		b1 = vec2normalize(b1)
		b2 = vec2normalize(b2)
		sub1 = vec2sub(v1, coord)
		sub2 = vec2sub(v2, coord)
		u = (ulen - vec2dot(b2, sub2)) / ulen
		v = (vlen - vec2dot(b1, sub1)) / vlen
		w = (u*self.deep2 + v*self.deep1) + self.v[0][2]
		#w = w - 1000.0
		#print 'u: %f' % (u)
		#print 'v: %f' % (v)
		#print 'w: %f' % (w)
		#u = (ulen - vec2dot(b2,sub2)) / ulen
		#v = (vlen - vec2dot(b1,sub1)) / vlen
		if u > 1.0 or u < 0.0:
			return None
		#print coord
		#return False
		if v > 1.0 or v < 0.0:
			return None
		if u+v > 1.0:
			return None
		#adddot('cap_mdl',coord,[int(u * 255.0),0,int(v * 255.0),255])
		#return False
		return [u, v, w]

	## RasterTriangle.__getitem__
	# returns value num from \ref RasterTriangle.v
	def __getitem__(self, num):
		return self.v[num]
	

## research use
def get2dcoord(coords, x, y):
	for cor in coords:
		if cor[0] == x and cor[1] == y:
			return cor
	coords.append([x, y, 0])
	return coords[len(coords)-1]


## research use
def tic2dcoord(coords, x, y):
	for cor in coords:
		if cor[0] == x and cor[1] == y:
			cor[2] += 1
			return cor
	coords.append([x, y, 1])
	return coords[len(coords)-1]


## primary Raster
# lots of goodies in this class
# \ref RasterTriangle
class RasterObject:

	## initialize values tris, bnds_min, bnds_max, locked, zbuffer, hm, coords
	def __init__(self, bm):
		self.tris = []
		self.bnds_min = None
		self.bnds_max = None
		self.locked = False
		self.zbuffer = None
		self.bm = bm
		self.coords = []

	## builds raster object boundaries
	# populates bnds_min bnds_max
	def bounds_compare(self, v):
		if self.bnds_min is None:
			self.bnds_min = VectorCopy(v)
		if self.bnds_max is None:
			self.bnds_max = VectorCopy(v)
		for i in range(0, 3):
			if v[i] < self.bnds_min[i]:
				self.bnds_min[i] = v[i]
			if v[i] > self.bnds_max[i]:
				self.bnds_max[i] = v[i]

	## not called?
	#def z_buffer_init(self):
	#	scr_min = None
	#	scr_max = None

	## \ref RasterTriangle \ref RasterObject::bounds_compare
	# populates RasterObject.tris with supplied values v1 v2 v3 vn1 vn2 vn3
	def add_triangle(self, v1, v2, v3, vn1, vn2, vn3):
		#print 'addtri: %f %f %f' % (v1[0],v1[1],v1[2])
		self.tris.append(RasterTriangle(v1, v2, v3, vn1, vn2, vn3))
		self.bounds_compare(v1)
		self.bounds_compare(v2)
		self.bounds_compare(v3)

	## \ref tic2dcoord
	# \ref BlitMatrix.add_coord
	def blit_line(self, v1, v2, color=None, flip=False):
		if color is None:
			color = [64, 64, 64, 128]
		coords = []
		v3 = VectorSubtract(v2, v1)
		v3nor = VectorNormalize(v3)
		v3len = VectorLength(v3)
		seglen = 0.125
		trac = 0.0
		while trac < (v3len+seglen):
			pt = VectorAdd(VectorScale(v3nor, trac), v1)
			pt2d = [int(pt[0]), int(pt[1])]
			cor = tic2dcoord(coords, pt2d[0], pt2d[1])
			#print trac
			trac += seglen
		for cor in coords:
			#print cor
			col = [color[0], color[1], color[2], 16*cor[2]]
			if col[3] > 255:
				col[3] = 255
			self.bm.add_coord(cor, None, col, flip)
		if 0:
			global xc, yc, zc
			v3 = VectorSubtract(v2, v1)
			v3[zc] = 0.0
			vlen2d = VectorLength(v3)
			segs = int(vlen2d)
			if segs == 0:
				return
			v4 = VectorScale(v3, 1.0/float(segs))
			origin = VectorCopy(v1)
			self.bm.add_coord(origin, None, color, flip)
			v3 = VectorCopy(v1)
			for i in range(0, segs):
				v3 = VectorAdd(v3, v4)
				origin = VectorCopy(v3)
				self.bm.add_coord(origin, None, color, flip)

	## RasterObject.get_uv
	# given some screen coords returns dist relative to 'edge0'
	# supplied v0 v1 v2 and edge0
	# \ref is_tinyfloat
	#
	def get_uv(self, v0, v1, v2, edge0):
		edge1 = vec2sub(v1, v0)
		edge2 = vec2sub(v2, v0)
		if is_tinyfloat(edge1[0]):
			return -1.0
		else:
			d = vec2dot(edge2, edge1)
			if is_tinyfloat(d):
				return -1.0
			u = vec2dot(edge1, edge0)
			u /= d
			if u < 0.0 or u > 1.0:
				return -1.0
			return u

	## RasterObject.blit_triangle
	# \ref RasterTriangle.go_coord
	def blit_triangle(self, tri):
		bnds_min = VectorCopy(tri[0])
		bnds_max = VectorCopy(tri[0])
		
		#v0 = VectorCopy(tri[0])
		#v1 = VectorCopy(tri[1])
		#v2 = VectorCopy(tri[2])
		#print 'v0: %s' % (v0)
		#print 'v1: %s' % (v1)
		#print 'v2: %s' % (v2)
		for i in range(1, 3):
			for j in range(0, 3):
				if tri[i][j] < bnds_min[j]:
					bnds_min[j] = tri[i][j]
				if tri[i][j] > bnds_max[j]:
					bnds_max[j] = tri[i][j]
					
		#bnds_min[0] -= 50.0
		#bnds_min[1] -= 50.0
		#bnds_max[0] += 50.0
		#bnds_max[1] += 50.0
		bnds_min = VectorInt(bnds_min)
		bnds_max = VectorInt(bnds_max)
		bnds_size = [int(bnds_max[0]-bnds_min[0])+1, int(bnds_max[1]-bnds_min[1])+1]
		#for i in range(int(bnds_min[0]),int(bnds_max[0])+1):
		#	for j in range(int(bnds_min[1]),int(bnds_max[1])+1):
		for i in range(0, bnds_size[1]):
			for j in range(0, bnds_size[0]):
				coord = [float(j+bnds_min[0]), float(i+bnds_min[1]), 0.0]
				#print 'coord: %s' % (coord)
				uv = tri.go_coord(coord)
				if uv is not None:
					#print uv
					#adddot('cap_mdl',coord,[int(uv[0]*255.0),int(uv[1]*255.0),255,255])
					if tri.bright >= 0.0:
						#color = [160,128,128,128]
						color = [32, 48, 64, 255]
						for k in range(0, 3):
							color[k] += int(160.0 * tri.bright)
							if color[k] > 255:
								color[k] = 255
							elif color[k] < 0:
								color[k] = 0
						coord[2] = uv[2]
						self.bm.add_coord(coord, uv, color, True)

	def blit_polygon(self, numsides, pos, radius, color=None, angle=0.0):
		if color is None:
			color = [64, 64, 64, 128]
		startpos = [0.0, radius, 0.0]
		if is_tinyfloat(angle) is False:
			pos2 = MatrixTransformPoint(MatrixFromAngles(0.0, 0.0, angle), startpos)
			startpos = VectorCopy(pos2)
		m = MatrixFromAngles(0.0, 0.0, 360.0/float(numsides))
		i = 0
		poskeep = VectorCopy(startpos)
		while i < numsides:
			oldpos = poskeep
			poskeep = MatrixTransformPoint(m, oldpos)
			v1 = VectorAdd(oldpos, pos)
			v2 = VectorAdd(poskeep, pos)
			self.blit_line(v1, v2, color)
			i += 1
		self.blit_line(poskeep, startpos, color)

	def blit_grunt_work(self):
		#go_raster_triangles = _solid
		#go_wireframe_triangles = _wires
		go_raster_triangles = True
		go_wireframe_triangles = False
		go_wireframe_normals = False
		go_wireframe_twosided = False
		use_minmax = False
		min_tri = 0
		max_tri = 256
		triangles_ct = len(self.tris)
		if go_raster_triangles:
			print 'adding raster triangles'
			i = 0
			for tri in self.tris:
				if i % 256 == 0:
					print '%d / %d' % (i, triangles_ct)
				#if(i>=0 and i<64):
					#if(i%2==0):
				#	if(i%32==0):
				#print 'tri %d' % (i)
				if use_minmax:
					if (i >= min_tri) and (i < max_tri):
						self.blit_triangle(tri)
				else:
					self.blit_triangle(tri)
				i += 1
		
		if go_wireframe_triangles:
			print 'adding wireframe triangles'
			#sys.stdout.write('tri ')
			i = 0
			for tri in self.tris:
				if i % 256 == 0:
					print '%d / %d' % (i, triangles_ct)

				if use_minmax:
					if (i >= min_tri) and (i < max_tri):
						#print 'wires - tri:%d / %d' % (i,triangles_ct)
						#sys.stdout.write('.')
						
						if tri.bright > 0.0:
							#print('tri[0] %f %f' % (tri[0][0],tri[0][1]))
							self.blit_line(tri[0], tri[1], [64, 64, 64, 128], True)
							self.blit_line(tri[1], tri[2], [64, 64, 64, 128], True)
							self.blit_line(tri[2], tri[0], [64, 64, 64, 128], True)
							if go_wireframe_normals:
								#self.blit_line(tri[0],tri.vne[0],[255,0,0,255])
								#self.blit_line(tri[1],tri.vne[1],[255,0,0,255])
								#self.blit_line(tri[2],tri.vne[2],[255,0,0,255])
								self.blit_line(tri.vall, tri.nend, [255, 0, 0, 255], True)
						else:
							if go_wireframe_twosided:
								self.blit_line(tri[0], tri[1], [64, 64, 64, 128], True)
								self.blit_line(tri[1], tri[2], [64, 64, 64, 128], True)
								self.blit_line(tri[2], tri[0], [64, 64, 64, 128], True)
								if go_wireframe_normals:
									#self.blit_line(tri[0],tri.vne[0],[0,0,255,255])
									#self.blit_line(tri[1],tri.vne[1],[0,0,255,255])
									#self.blit_line(tri[2],tri.vne[2],[0,0,255,255])
									self.blit_line(tri.vall, tri.nend, [0, 0, 255, 255], True)
				else:
					if tri.bright > 0.0:
						pass
						self.blit_line(tri[0], tri[1], [64, 64, 64, 128], True)
						self.blit_line(tri[1], tri[2], [64, 64, 64, 128], True)
						self.blit_line(tri[2], tri[0], [64, 64, 64, 128], True)
						if go_wireframe_normals:
							self.blit_line(tri.vall, tri.nend, [255, 0, 0, 255], True)
					else:
						pass
						if go_wireframe_twosided:
							self.blit_line(tri[0], tri[1], [32, 32, 32, 128], True)
							self.blit_line(tri[1], tri[2], [32, 32, 32, 128], True)
							self.blit_line(tri[2], tri[0], [32, 32, 32, 128], True)
							if go_wireframe_normals:
								self.blit_line(tri.vall, tri.nend, [0, 0, 255, 255], True)
				i += 1
		
		print 'blitting coordinates'
		self.bm.blit_coords()


## blits a dot ... is it the same as the adddot() in wudanicon.py ?
def adddot(selection, coord, color=None, mark=0):
	if color is None:
		color = [64, 64, 64, 128]
	image_operation('seladdmark %s %d %d %d %d %d %d %d' % (selection, coord[0], coord[1], color[0], color[1], color[2], color[3], mark))


## \ref raster_getscreencoord \ref adddot
def plot_coord(selection, coord):
	plot = raster_getscreencoord(coord)
	adddot(selection, plot)


def plot_line(selection, v1, v2):
	global fScale
	scale = fScale / 2.0
	global xc, yc, zc
	v3 = VectorSubtract(v2, v1)
	v3[zc] = 0.0
	vlen = VectorLength(v3)
	segs = int(vlen*scale)
	#if(segs<5):
	#	segs = 5
	if segs == 0:
		return
	v4 = VectorScale(v3, 1.0/float(segs))
	plot_coord(selection, v1)
	v3 = VectorCopy(v1)
	for i in range(0, segs):
		v3 = VectorAdd(v3, v4)
		plot_coord(selection, v3)


## addline
# blits a line ... is it the same as the addline() in wudanicon.py ?
# \ref plot_coord
# \ref fScale
# \ref xc \ref
def addline(selection, v1, v2):
	global fScale
	scale = fScale / 2.0
	global xc, yc, zc
	v3 = VectorSubtract(v2, v1)
	v3[zc] = 0.0
	vlen = VectorLength(v3)
	segs = int(vlen*scale)
	#if(segs<5):
	#	segs = 5
	if segs == 0:
		return
	v4 = VectorScale(v3, 1.0/float(segs))
	plot_coord(selection, v1)
	v3 = VectorCopy(v1)
	for i in range(0, segs):
		v3 = VectorAdd(v3, v4)
		plot_coord(selection, v3)


## returns a coordinate in 3d space
# todo: apply actual matrix
# uses global variable \ref isometric
def raster_getscreencoord(coord):
	global fScale
	global isometric
	global xc, yc, zc
	scale = fScale
	#center = [int(0.0*scale),int(0.0*scale)]
	#xcor = coord
	if isometric:
		return [float(int(coord[xc]*scale)), float(int(coord[yc]*scale)), float(int(coord[zc]*scale))]


## transform supplied matrix bmat around the x axis by supplied angle
def wv_global_rotation_x(bmat, angle):
	dmat = MatrixFromAngles(angle, 0.0, 0.0)
	return MatrixMultiply(dmat, bmat)


## transform supplied matrix bmat around the y axis by supplied angle
def wv_global_rotation_y(bmat, angle):
	dmat = MatrixFromAngles(0.0, angle, 0.0)
	return MatrixMultiply(dmat, bmat)


## transform supplied matrix bmat around the z axis by supplied angle
def wv_global_rotation_z(bmat, angle):
	dmat = MatrixFromAngles(0.0, 0.0, angle)
	return MatrixMultiply(dmat, bmat)
