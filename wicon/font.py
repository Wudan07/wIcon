# -*- coding: utf-8 -*-
# Copyright (c) 2015 Brad Newbold (wudan07 [at] gmail.com)
# See LICENSE for details.
# font.py
#
from common import file_exists, str_match, str_match_end, str_strip_end, str_strip_newline
from handy import file_open_in, file_open_out
from selection import getselsize
from wudanicon import image_operation, line_to_vars


class FontGlyphObject:
	def __init__(self, index, imgnum, fontname=None):
		self.font = 'basic'
		if fontname is not None:
			self.font = fontname
		self.index = index
		self.imgnum = imgnum
		self.loaded = False
		self.ofs = None
		self.selname = None
		self.size = None
		
	def load(self):
		if self.imgnum is None:
			self.loaded = True
			return
		path = 'font/%s/glyph.%04d.png' % (self.font, self.imgnum)
		dat = 'font/%s/%04d.txt' % (self.font, self.imgnum)
		if file_exists(path):
			self.selname = 'glyph%04d' % self.imgnum
			#image_operation('selsquare %s %s cm 232 0 4' % (self.selname,path))
			image_operation('selsquare %s %s' % (self.selname, path))
			self.size = getselsize(self.selname)
			#print 'Load Glyph sel(%s) size %s' % (self.selname, str(self.size))
			self.ofs = [0, 0]
			if file_exists(dat):
				inf = file_open_in(dat)
				if inf is not None:
					lines = inf.readlines()
					for line in lines:
						line = str_strip_newline(line)
						vals = line_to_vars(line)
						if str_match(vals[0], 'ofs'):
							if len(vals) == 3:
								self.ofs[0] = int(vals[1])
								self.ofs[1] = int(vals[2])
					inf.close()
				pass
			else:
				self.ofs[1] = 8 - self.size[1]
				out = file_open_out(dat, 0)
				out.write('ofs %d %d\n' % (self.ofs[0], self.ofs[1]))
				out.close()
			self.loaded = True
		else:
			self.imgnum = False
			self.loaded = True
	
	def blit(self, sel, ofs):
		_debug = False
		#print self.index
		if self.selname is not None:
			#print self.size
			#print sel
			#print ofs
			image_operation('selappend %s %s of %d %d bounds' % (self.selname, sel, ofs[0]+self.ofs[0], ofs[1]+self.ofs[1]))
			#image_operation('selappend %s %s of %d %d bounds' (self.selname,sel,ofs[0]+self.ofs[0],ofs[1]+self.ofs[1]))
			if _debug:
				print 'BLIT INFO ---'
				print self.index
				print self.selname
				print ofs
				print self.ofs
				print self.size
				print 'Blit SEL %s to SEL %s' % (self.selname, sel)
				print getselsize(sel)
				print '          ---'
			return ofs[0] + self.ofs[0] + self.size[0] + 1
		#if(ofs is None):
		#	print 'OFS is None!'
		#else:
		#	print ofs
		if self.ofs is None:
			#print 'self.OFS is None!'
			return ofs[0] + 5
		#else:
		#	print self.ofs
		if self.size is None:
		#	print 'self.SIZE is None!'
			return ofs[0] + 5
		#else:
		#	print self.size
		return ofs[0] + self.ofs[0] + self.size[0] + 1


class FontObject:
	def __init__(self, fontname=None):
		self.name = 'basic'
		if fontname is not None:
			self.name = fontname
		self.glyphs = []
		self.read = False
		fkeep = 32
		ikeep = 0
		for i in range(0, 32):
			self.glyphs.append(FontGlyphObject(i, None, self.name))
		while fkeep < 127:
			self.glyphs.append(FontGlyphObject(fkeep, ikeep, self.name))
			fkeep += 1
			ikeep += 1
		for glyph in self.glyphs:
			glyph.load()
		#print len(self.glyphs)
	
	def blit_str(self, selname, keeps, string):
		ofs = [keeps[0], keeps[1]]
		extents = [keeps[0], keeps[1]]
		for val in string:
			#print val
			i = ord(val)
			#CHAR: NEWLINE
			if i == 10:
				ofs[0] = keeps[0]
				ofs[1] += 12
			#CHAR: CARRIAGE RETURN
			elif i == 13:
				ofs[0] = keeps[0]
				ofs[1] += 12
			#CHAR: TAB
			elif i == 9:
				ofs[0] += 20
			#EVERYTHING ELSE
			else:
				if i >= len(self.glyphs):
					ofs[0] = self.glyphs[32].blit(selname, ofs)
				else:
					ofs[0] = self.glyphs[i].blit(selname, ofs)
			for j in range(0, 2):
				if ofs[0] > extents[0]:
					extents[0] = ofs[0]
				if ofs[1] > extents[1]:
					extents[1] = ofs[1]
		return [extents[0]-keeps[0]-1, extents[1]-keeps[1]+10]
	
	def format_for_width(self, string, width):
		print 'FORMATFORWIDTH: (%s)' % string
		line = string.replace('\n', ' ')
		#print line
		data = ''
		vals = line.split(' ')
		ofs = [0, 0]
		#old_ofs = [None,None]
		i = 0
		while i in range(0, len(vals)):
			val = vals[i]
			print '---'
			print ofs
			#if(old_ofs[0] is None):
			#	old_ofs[0] = ofs[0]
			#	old_ofs[1] = ofs[1]
			print val
			newofs = self.blit_str(None, ofs, val)
			xpos = ofs[0] + newofs[0] + 1
			print '%d - %d xpos' % (ofs[0], xpos)
			#print newofs
			if xpos > width:
				if str_match_end(data, '\n'):
					#already did newline!
					data += val + ' '
					ofs = [ofs[0] + newofs[0] + 6, newofs[1]]
					print val
					i += 1
					pass
				else:
					data = str_strip_end(data, ' ')
					data += '\n'
					ofs = [0, 0]
					print 'NEWLINE'
			else:
				data += val + ' ' 
				ofs = [ofs[0] + newofs[0] + 6, newofs[1]]
				print val
				i += 1
		#print data
		return data
	
	def dump(self, selname):
		image_operation('selblock %s 0 0 800 20 0 0 0 255' % selname)
		ofs = [5, 5]
		for glyph in self.glyphs:
			ofs[0] = glyph.blit(selname, ofs)
		image_operation('selsave %s font_trial.png' % selname)