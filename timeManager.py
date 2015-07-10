#!/usr/bin/python

import time

class timeManager():
	def __init__(self):
		self.longPeriod = 24*60*60
		self.longEndPoint = 0
		self.shortPeriod = 5*60
		self.shortEndPoint = 0
	def __init__(self,longPeriod,shortPeriod):
		self.longPeriod = longPeriod
		now = time.time()
		self.longEndPoint = int(time.mktime(time.strptime(time.strftime('%Y%m%d',time.localtime(now)),'%Y%m%d')))+self.longPeriod
		self.shortPeriod = shortPeriod
		self.shortEndPoint = now-now%(self.shortPeriod)+self.shortPeriod
	def setEndPoint(self,tempTime):
		#self.longEndPoint = int(time.mktime(time.strptime(time.strftime('%Y%m%d',time.localtime(tempTime)),'%Y%m%d')))+self.longPeriod
		self.longEndPoint = tempTime-tempTime%(self.longPeriod)+self.longPeriod
		self.shortEndPoint = tempTime-tempTime%(self.shortPeriod)+self.shortPeriod
	def setPeriod(self,longPeriod,shortPeriod):
		self.longPeriod = longPeriod
		self.shortPeriod = shortPeriod
	def updateLongPoint(self):
		self.longEndPoint += self.longPeriod
	def updateShortPoint(self):
		self.shortEndPoint += self.shortPeriod
		

if __name__ == "__main__":
	t = timeManager(24*60*60,5*60)
	print t.longPeriod
	print t.shortPeriod
	print "time long end point:"
	print t.longEndPoint
	print time.localtime(t.longEndPoint)
	print "time short end point:"
	print t.shortEndPoint
	print time.localtime(t.shortEndPoint)
	t.updateLongPoint()
	t.updateShortPoint()
	print "after update time long end point:"
	print t.longEndPoint
	print time.localtime(t.longEndPoint)
	print "after update time short end point:"
	print t.shortEndPoint
	print time.localtime(t.shortEndPoint)

