#!/usr/bin/python

import processer

def add(p):
	p.data += 1
def addInt(a):
	a += 1
p = processer.processer()
print p.data
add(p)
print p.data

a = 1
print a
addInt(a)
print a

