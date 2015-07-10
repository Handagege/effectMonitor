#!/usr/bin/python

import ConfigParser
import types

d = {"a":1,"b":2}
print d.get("a",None)
r = d.get("c",None)
if r == None:
	print "yyyy"
d = "111"
if r == "" or\
	 d == "asd":
	print "dddd"
print type(d)
try:
	d = int(d)
except ValueError:
	print "value error"
print type(d)

print d," 222"

l1 = ['111','123']
l2 = ['333','444']
l1.extend(l2)
print l1
