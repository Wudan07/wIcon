# -*- coding: utf-8 -*-
"""wIcon library:
	q_math.py: Vector Functions and other Math Goodies.
	Many functions here are ported, or strongly based on versions found in Quake3 source release, which is GPL, but are
	heavily modified for use here (given that Python != C), but I beleive the 'credit where credit is due' rule applies
	here.
	This pythonic version originated from a copy given to me by Tr3Bor, the author of XreaL, a Quake3 game engine.
	A version of this was given to the author from Tr3Bor himself, without a specific license, and the version you find
	at https://github.com/fucknohtml/xreal/blob/master/blender/blender-2.49/q_math.py still is without license in the
	header of the file.  Hence the author is not aware of any restriction on sharing this file.
	Some additions are made by me, Brad Newbold, as follows:
		Vec3 functions:
		- VectorScale function
		- VectorNormalize function
		- VectorMA function
		- VectorInt function
		- is_tinyfloat function
		Vec2 functions
		- vec2copy
		- vec2dot
		- vec2dot_sr
		- vec2sub
		- vec2add
		- vec2scale
		- vec2len
		- vec2normalize
		- tri_getbisectvert
		- vec2distfromline
		- vec2distfromtri_vec
		Matrix functions
		- MatrixCopy
		- MatrixPrint
		- MatrixScaleAxis (nearly identical to MatrixIdentity)
		- MatrixTransformNormal (heavily based on MatrixTransformPoint)

"""

import math

epsilon = 0.000000001


def ANGLE2SHORT(x):
	return int((x * 65536 / 360) & 65535)


def SHORT2ANGLE(x):
	return x * (360.0 / 65536.0)


def DEG2RAD(a):
	return (a * math.pi) / 180.0


def RAD2DEG(a):
	return (a * 180.0) / math.pi


def DotProduct(x, y):
	return x[0] * y[0] + x[1] * y[1] + x[2] * y[2]


def CrossProduct(a, b):
	return [a[1]*b[2] - a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0]]


def VectorLength(v):
	return math.sqrt(v[0]*v[0] + v[1]*v[1] + v[2]*v[2])


def VectorSubtract(a, b):
	return [a[0] - b[0], a[1] - b[1], a[2] - b[2]]


def VectorAdd(a, b):
	return [a[0] + b[0], a[1] + b[1], a[2] + b[2]]


def VectorCopy(v):
	return [v[0], v[1], v[2]]


def VectorInverse(v):
	return [-v[0], -v[1], -v[2]]


def VectorScale(v, scale):
	return [v[0]*scale, v[1]*scale, v[2]*scale]


def VectorNormalize(v):
	vlen = VectorLength(v)
	ilen = 0.0
	if vlen != 0.0:
		ilen = 1.0/vlen
	return [v[0]*ilen, v[1]*ilen, v[2]*ilen]


def VectorMA(a, scale, b):
	return [a[0]+b[0]*scale, a[1]+b[1]*scale, a[2]+b[2]*scale]


def VectorInt(a):
	return [int(a[0]), int(a[1]), int(a[2])]


def is_tinyfloat(val):
	if math.fabs(val) < epsilon:
		return True
	return False


def vec2copy(v):
	return [v[0], v[1]]


def vec2dot(x, y):
	return x[0]*y[0] + x[1]*y[1]


def vec2dot_sr(x, y):
	return x[0]*y[0] - x[1]*y[1]


def vec2sub(a, b):
	return [a[0] - b[0], a[1] - b[1]]


def vec2add(a, b):
	return [a[0] + b[0], a[1] + b[1]]


def vec2scale(v, scale):
	return [v[0]*scale, v[1]*scale]


def vec2len(v):
	return math.sqrt(v[0]*v[0] + v[1]*v[1])


def vec2normalize(v):
	_len = vec2len(v)
	ilen = 0.0
	if _len != 0.0:
		ilen = 1.0 / _len
	return [v[0]*ilen, v[1]*ilen]


def tri_getbisectvert(v0, v1, v2):
	edge1 = VectorNormalize(VectorSubtract(v1, v0))
	edge0 = VectorSubtract(v2, v0)
	len1 = DotProduct(edge1, edge0)
	return VectorMA(v0, len1, edge1)


def vec2distfromline(coord, v0, v1, v2):
	edge1 = vec2sub(v1, v0)
	edge0 = vec2sub(coord, v0)
	edge1 = vec2normalize(edge1)
	lenalong1 = vec2dot(edge1, edge0)
	#set v3 to point on edge1 closest to coord
	v3 = vec2add(vec2scale(edge1, lenalong1), v0)

	#sub2 is difference between v2 and v3, or 1.0
	sub2 = vec2len(vec2sub(v2, v3))
	#sub3 = vec2len(vec2sub(coord,v3))
	#if(sub3 > sub2):
	#    return -1.0#(sub3/sub2)
	return (sub2 - vec2len(vec2sub(coord, v2))) / sub2
	#this returns almost sane coords
	#return ((sub2 - vec2len(vec2sub(coord,v2)))/sub2)


def vec2distfromtri_vec(coord, v0, v1, v2):
	edge1 = vec2sub(v1, v0)
	edge0 = vec2sub(coord, v0)
	edge1 = vec2normalize(edge1)
	lenalong1 = vec2dot(edge1, edge0)
	v3 = vec2add(vec2scale(edge1, lenalong1), v0)
	return vec2len(vec2sub(coord, v3))
	

def RadiusFromBounds(mins, maxs):
	corner = [0, 0, 0]

	for i in range(0, 3):
		a = abs(mins[i])
		b = abs(maxs[i])
		if a > b:
			corner[i] = a
		else:
			corner[i] = b

	return VectorLength(corner)


## returns an identity matrix
def MatrixIdentity():
	return [[1.0, 0.0, 0.0, 0.0],
			[0.0, 1.0, 0.0, 0.0],
			[0.0, 0.0, 1.0, 0.0],
			[0.0, 0.0, 0.0, 1.0]]


## returns a matrix that performs a roll, pitch, yaw
def MatrixFromAngles(roll, pitch, yaw):
	sp = math.sin(DEG2RAD(pitch))
	cp = math.cos(DEG2RAD(pitch))

	sy = math.sin(DEG2RAD(yaw))
	cy = math.cos(DEG2RAD(yaw))

	sr = math.sin(DEG2RAD(roll))
	cr = math.cos(DEG2RAD(roll))
	
	return [[cp * cy,                     cp * sy,                 -sp,       0.0],
			[(sr * sp * cy + cr * -sy),  (sr * sp * sy + cr * cy),  sr * cp,  0.0],
			[(cr * sp * cy + -sr * -sy), (cr * sp * sy + -sr * cy), cr * cp,  0.0],
			[0.0,                         0.0,                      0.0,      1.0]]


## returns a copy of matrix m.  matrix m can be any array of lists containing floats, doesn't validate size
def MatrixCopy(m):
	b = []
	for i in range(0, len(m)):
		b.append([])
		n = m[i]
		for j in range(0, len(n)):
			b[i].append(n[j])
	return b


## prints matrix values in someone decent format.  will print any array of lists containing floats,
## doesn't validate size
def MatrixPrint(m):
	b = []
	rowslen = len(m)
	colslen = 0
	vallen = 0
	for i in range(0, len(m)):
		b.append([])
		n = m[i]
		if len(n) > colslen:
			colslen = len(n)
		for j in range(0, len(n)):
			val = '%2.8f' % (n[j])
			if len(val) > vallen:
				vallen = len(val)
			b[i].append(val)
	for i in range(0, rowslen):
		n = b[i]
		line = '| '
		for j in range(0, len(n)):
			val = n[j]
			while len(val) < vallen:
				val = ' ' + val
			line += val + ' '
		line += '|'
		print line


## returns a matrix that has axis scale values of sx sy sz (3 floats)
def MatrixScaleAxis(sx, sy, sz):
	return [[sx,  0.0, 0.0, 0.0],
			[0.0, sy,  0.0, 0.0],
			[0.0, 0.0, sz,  0.0],
			[0.0, 0.0, 0.0, 1.0]]


## returns a vec3 that is vec3 p transformed by matrix m (m, p)
def MatrixTransformPoint(m, p):
	return [m[0][0] * p[0] + m[1][0] * p[1] + m[2][0] * p[2] + m[3][0],
			m[0][1] * p[0] + m[1][1] * p[1] + m[2][1] * p[2] + m[3][1],
			m[0][2] * p[0] + m[1][2] * p[1] + m[2][2] * p[2] + m[3][2]]


## returns a vec3 that is p transformed by matrix m (m, p)
def MatrixTransformNormal(m, p):
	return [m[0][0] * p[0] + m[1][0] * p[1] + m[2][0] * p[2],
			m[0][1] * p[0] + m[1][1] * p[1] + m[2][1] * p[2],
			m[0][2] * p[0] + m[1][2] * p[1] + m[2][2] * p[2]]


## returns a 4x4 matrix that is the multiplied result of a * b
def MatrixMultiply(b, a):
	return [[
			a[0][0] * b[0][0] + a[0][1] * b[1][0] + a[0][2] * b[2][0],
			a[0][0] * b[0][1] + a[0][1] * b[1][1] + a[0][2] * b[2][1],
			a[0][0] * b[0][2] + a[0][1] * b[1][2] + a[0][2] * b[2][2],
			0.0,
			],[
			a[1][0] * b[0][0] + a[1][1] * b[1][0] + a[1][2] * b[2][0],
			a[1][0] * b[0][1] + a[1][1] * b[1][1] + a[1][2] * b[2][1],
			a[1][0] * b[0][2] + a[1][1] * b[1][2] + a[1][2] * b[2][2],
			0.0,
			],[
			a[2][0] * b[0][0] + a[2][1] * b[1][0] + a[2][2] * b[2][0],
			a[2][0] * b[0][1] + a[2][1] * b[1][1] + a[2][2] * b[2][1],
			a[2][0] * b[0][2] + a[2][1] * b[1][2] + a[2][2] * b[2][2],
			0.0,
			],[
			a[3][0] * b[0][0] + a[3][1] * b[1][0] + a[3][2] * b[2][0] + b[3][0],
			a[3][0] * b[0][1] + a[3][1] * b[1][1] + a[3][2] * b[2][1] + b[3][1],
			a[3][0] * b[0][2] + a[3][1] * b[1][2] + a[3][2] * b[2][2] + b[3][2],
			1.0,
			]]


def MatrixSetupTransform(forward, left, up, origin):
	return [[forward[0], forward[1], forward[2], origin[0]],
			[left[0],    left[1],   left[2],     origin[1]],
			[up[0],      up[1],     up[2],       origin[2]],
			[0.0,        0.0,       0.0,         1.0]]
