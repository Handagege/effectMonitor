#!/usr/bin/python

from random import *

print randint(-10,1)
print randrange(0,10,2)
print uniform(1,10)
print choice("abcde")
print sample("abcde",3)

str = "hello"
data = "......%s......."%(str)
print data
i = [-1,1]
print choice(i)
