#!/usr/bin/python

import Queue

myqueue = Queue.Queue(maxsize = 10)
for i in range(1,3):
	myqueue.put(i)
for i in range(1,3):
	print(myqueue.get())

l = [Queue.Queue(maxsize = 10),Queue.Queue(maxsize = 10)]
for i in range(10):
	l[0].put(i)
	l[1].put(i+10)
	print(l[0].get())
	print(l[1].get())


