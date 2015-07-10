#!/usr/bin/python

class base():
	def __init__(self):
		self.a = 1
		self.b = 2
	def do(self):
		print self.a
	def process(self):
		self.do()

class aa(base):
	def __init__(self):
		base.__init__(self)
		self.c = 3
	def do(self):
		self.c += 1
		print self.c

if __name__ == "__main__":
	a = aa()
	a.process()
	a.process()
