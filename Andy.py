#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class Student(object):
		"""docstring for Student"""
		@property
		def score(self):
			return self._score

		@score.setter
		def score(self, value):
			if not isinstance(value, int):
				raise ValueError('score must be an integer')
			if value < 0 or value > 0:
				raise ValueError('score must between 0 and 100')
			self._score = value
		