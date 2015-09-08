# -*- coding: utf-8 -*-
# Copyright (c) 2015 Brad Newbold (wudan07 [at] gmail.com)
# See LICENSE for details.
# handy.py
#
"""wIcon library:

"""

import sys
import os
import time
import struct
#from wicon.common import str_match_start, str_strip_newline, str_strip_whitespace
from common import *
#import string
#import getopt
#import os.path
#import socket
#import math
#from stat import *
#from const import *

outputDebugMSGs = False


def fabs(val):
	if val < 0.0:
		return -val
	return val


def redirect_stdout(filename):
	if filename:  # Replace stdout by file
		#print "os.close redirect_stdout"
		os.close(1)
		i = os.open(filename, os.O_CREAT | os.O_WRONLY | os.O_TRUNC, 0666)
		if i != 1:
			sys.stderr.write("stdout not opened on 1!\n")
		return i
	else:
		#LEAVE os.close(1) commented out here, it caused errors
		#os.close(1)
		sys.stdout = open('stdout.txt', 'w')
		#i=os.open(sys.stdout,os.O_CREAT|os.O_WRONLY|os.O_TRUNC,0666)
		#if i!=1:
		#	sys.stderr.write("stdout not opened on 1!\n")


def check_line(line):
	#val = str_strip_part(line,'\1')
	#val = str_strip_part(val,'\4')
	#return val
	#vals = line.split(1)
	val = ''
	#if(len(vals)==1):
	#		return line
	#for item in vals:
	#		val += item
	#return val

	for char in line:
		ic = ord(char)
		if ic < 32:
			if ic == 1:
				pass
			elif ic == 2:
				pass
			elif ic == 4:
				pass
			elif ic == 8:
				pass
			elif ic == 9:
				pass
			elif ic == 10:
				pass
			elif ic == 13:
				pass
			elif ic == 16:
				pass
			elif ic == 18:
				pass
			elif ic == 22:
				pass
			elif ic == 24:
				pass
			elif ic == 26:
				pass
			elif ic == 28:
				pass
			else:
				print ic
				print char
		if ic == 1:
			pass
		elif ic == 2:
			pass
		elif ic == 4:
			pass
		elif ic == 8:
			pass
		elif ic == 9:
			pass
		elif ic == 13:
			pass
		elif ic == 16:
			pass
		elif ic == 18:
			pass
		elif ic == 22:
			pass
		elif ic == 24:
			pass
		elif ic == 26:
			pass
		elif ic == 28:
			pass
		else:
			#print int(char)
			#val += '-%s(%s)' % (hex(ic),char)
			val += char
	return val


def file_open_out(path, append):
	try:
		if path != "":
			if append == 1:
				out = open(path, 'a')
			else:
				out = open(path, 'w')
		else:
			out = sys.stdout
	except EnvironmentError:
		return None
	return out


def file_open_out_b(path):
	try:
		if path != "":
			out = open(path, 'wb')
		else:
			out = sys.stdout
	except EnvironmentError:
		return None
	return out


def file_open_in(path):
	try:
		if path != "":
			infp = open(path, 'r')
		else:
			return None
	except EnvironmentError:
		return None
	return infp


def file_open_in_b(path):
	try:
		if path != "":
			infp = open(path, 'rb')
		else:
			return None
	except EnvironmentError:
		return None
	return infp


def bindata_unpack(binformat, fil):
	tmp = fil.read(struct.calcsize(binformat))
	return struct.unpack(binformat, tmp)


def _now():
	return time.time()


class CSVRow(dict):
	def __getattribute__(self, name):
		return self[name]
	
	def __missing__(self, name):
		return None


def loadvals(csvr, key, row):
	## maxlen = 0
	lenkey = len(key)
	lenrow = len(row)
	if lenkey < lenrow:
		maxlen = lenkey
	else:
		maxlen = lenrow
	for i in range(0, maxlen):
		csvr[key[i]] = row[i]


def guess_columns(path, delimiter=','):
	inf = file_open_in(path)
	if inf is None:
		return None
	lines = inf.readlines()
	inf.close()
	line = lines[0]
	out = file_open_out('csvguess', 0)
	out.write(line)
	out.close()
	rows = read_delimited_file('csvguess', delimiter, 1)
	os.remove('csvguess')
	if rows is None:
		return None
	return len(rows)


def unpack_delimited_file(path, delimiter=',', toprow=None):
	items = []
	rows = read_delimited_file(path, delimiter, guess_columns(path, delimiter))
	#inf = file_open_in(path)
	first_one = True
	keyrow = None
	if toprow is not None:
		keyrow = toprow
		first_one = False
	for row in rows:
		if first_one is True:
			keyrow = row
			first_one = False
		else:
			item = CSVRow()
			loadvals(item, keyrow, row)
			items.append(item)
	return items


def read_delimited_file(path, delimiter=',', perline=2):
	_debug = False
	avals = []
	rows = []
	inf = file_open_in(path)
	if inf is not None:
		if _debug:
			print('CSV: reading file \'%s\'' % path)
		lines = inf.readlines()
		inf.close()
		if _debug:
			print('CSV: lines in: %d' % len(lines))
		j = 0
		while j < len(lines):
			line = str_strip_newline(lines[j])
			vals = line.split(delimiter)
			lenvals = len(vals)
			## fvals = []
			i = 0
			if _debug:
				print i
				print lenvals
			while i < lenvals:
				if _debug:
					print i
					print vals[i]
				val = vals[i]
				if len(val) > 0:
					avals.append(val)
				else:
					avals.append(val)
				i += 1
			j += 1
	
	bvals = []
	i = 0
	lenvals = len(avals)
	while i < lenvals:
		val = avals[i]
		if len(val) > 0:
			if str_match_start(val[0], '"') is True:
				fixval = val[1:]
				i += 1
				done = False
				if _debug:
					print 'fixem ... (%s)' % val
				if str_match_end(fixval, '"') is True:
					fixval = fixval[0:-1]
					done = True
					i -= 1
				if i >= lenvals:
					done = True
					i -= 1
				while done is not True:
					if _debug:
						print i
						print val
						print fixval
					if len(avals[i]) > 0:
							if str_match_end(avals[i], '"') is True:
								fixval += '%s%s' % (delimiter, avals[i][0:-1])
								done = True
							else:
								fixval += '%s%s' % (delimiter, avals[i])
					else:
							fixval += '%s%s' % (delimiter, avals[i])
					i += 1
					if i == lenvals:
							done = True
					if done:
							i -= 1
					if done and _debug:
							print 'fixed: %s' % fixval
				bvals.append(fixval)
			else:
				bvals.append(val)
		else:
			bvals.append(val)
		i += 1
	
	i = 0
	while i < len(bvals):
		fvals = bvals[i:i + perline]
		if _debug:
			print fvals
		rows.append(fvals)
		i += perline
	return rows


def fseek(fil, target, size):
	if (target > 0) and (target < size):
		fil.seek(target)
	else:
		if outputDebugMSGs is True:
			print "fseek target 0x%08x exceeds 0x%08x" % (target, size)
