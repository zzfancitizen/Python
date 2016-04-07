#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class Screen(object):
	"""docstring for Screen"""
	@property
	def width(self):
		return self._width

	@width.setter
	def width(self, value):
		self._width = value

	@property
	def height(self):
		return self._height

	@height.setter
	def height(self, value):
		self._height = value

	@property
	def resolution(self):
		return self._width * self._height

class Chain(object):
	"""docstring for Chain"""
	def __init__(self, path=''):
		self._path = path

	def users(self, path):
		self._path = '/users'
		return Chain('%s/%s' % (self._path, path))

	def __getattr__(self, path):
			return Chain('%s/%s' % (self._path, path))

	def __str__(self):
		return self._path

	__repr__ = __str__
		


		
		