#!/usr/bin/python

import Queue

class statsItem():
	def __init__(self,windowLength=12):
		self.totalWindowStats = [0,0,0]
		self.totalDayStats = [0,0,0]
		self.tempWindowStats = [0,0,0]
		self.windowLength = windowLength
		self.windowQueueStats = [[0]*windowLength,[0]*windowLength,[0]*windowLength]
		self.trueMark = "1"
		self.falseMark = "-1"
		self.ctrDim = 100.0
		self.rpmDim = 100.0

	def update(self,clickStatus,achieveStatus,pos=-1):
		self.totalDayStats[0] += 1
		self.windowQueueStats[0][pos] += 1
		if achieveStatus == self.trueMark:
			for i in range(1,3):
				self.totalDayStats[i] += 1
				self.windowQueueStats[i][pos] += 1
				self.tempWindowStats[i] += 1
		elif clickStatus == self.trueMark:
			self.totalDayStats[1] += 1
			self.windowQueueStats[1][pos] += 1
			self.tempWindowStats[1] += 1

	def updateWindowStats(self,clickStatus,achieveStatus,pos=-1):
		self.windowQueueStats[0][pos] += 1
		self.tempWindowStats[0] += 1
		if achieveStatus == self.trueMark:
			for i in range(1,3):
				self.windowQueueStats[i][pos] += 1
				self.tempWindowStats[i] += 1
		elif clickStatus == self.trueMark:
			self.windowQueueStats[1][pos] += 1 
			self.tempWindowStats[1] += 1

	def updateDayStats(self,clickStatus,achieveStatus):
		self.totalDayStats[0] += 1
		if achieveStatus == self.trueMark:
			for i in range(1,3):
				self.totalDayStats[i] += 1
		elif clickStatus == self.trueMark:
			self.totalDayStats[1] += 1
		
	def proDayStats(self):
		if self.totalDayStats[0] == 0:
			print "[warning] day expo stats data is empty"
			return 0,0
		ctr = float(self.totalDayStats[1])*1000.0*self.ctrDim/float(self.totalDayStats[0])
		rpm = float(self.totalDayStats[2])*1000.0*self.rpmDim/float(self.totalDayStats[0])
		return ctr,rpm

	def proWindowStats(self):
		for i in range(3):
			self.totalWindowStats[i] -= self.windowQueueStats[i][0]
			self.totalWindowStats[i] += self.tempWindowStats[i]
			del self.windowQueueStats[i][0]
			self.windowQueueStats[i].append(0)
		if self.totalWindowStats[0] == 0:
			print "[warning] temp window expo stats data is empty"
			return 0,0
		self.tempWindowStats = [0,0,0]
		ctr = float(self.totalWindowStats[1])*1000.0*self.ctrDim/float(self.totalWindowStats[0])
		rpm = float(self.totalWindowStats[2])*1000.0*self.rpmDim/float(self.totalWindowStats[0])
		return ctr,rpm

	def flushDayStats(self):
		self.totalDayStats = [0,0,0]
	
	def printMsg(self):
		#print "windowTempStats: expo=%d,click=%d,achieve=%d"%(self.tempWindowStats[0],self.tempWindowStats[1],self.tempWindowStats[2])
		print "totalWindowTempStats:",self.totalWindowStats[0],self.totalWindowStats[1],self.totalWindowStats[2]
		print "windowTempStats: ",self.tempWindowStats[0],self.tempWindowStats[1],self.tempWindowStats[2]
		print "windowQueueStats: ",self.windowQueueStats[0],self.windowQueueStats[1],self.windowQueueStats[2]
		print "dayStats: expo=%d,click=%d,achieve=%d"%(self.totalDayStats[0],self.totalDayStats[1],self.totalDayStats[2])
		
	def printMsgToLog(self,logger):
		#print "windowTempStats: expo=%d,click=%d,achieve=%d"%(self.tempWindowStats[0],self.tempWindowStats[1],self.tempWindowStats[2])
		msg = "totalWindowTempStats:",self.totalWindowStats[0],self.totalWindowStats[1],self.totalWindowStats[2]
		logger.debug(msg)
		msg = "windowTempStats: ",self.tempWindowStats[0],self.tempWindowStats[1],self.tempWindowStats[2]
		logger.debug(msg)
		msg = "windowQueueStats: ",self.windowQueueStats[0],self.windowQueueStats[1],self.windowQueueStats[2]
		logger.debug(msg)
		msg = "dayStats: expo=%d,click=%d,achieve=%d"%(self.totalDayStats[0],self.totalDayStats[1],self.totalDayStats[2])
		logger.debug(msg)
		
if __name__ == "__main__":
	myStatsItem = statsItem(2)
	for i in range(1000):
		if i%100 == 0:
			ctr,rpm = myStatsItem.proDayStats()
			myStatsItem.flushDayStats()
			print "PERDAY--- ctrValue: %.3f | rpmValue: %.3f"%(ctr,rpm)
		if i%20 == 0:
			print len(myStatsItem.windowQueueStats[0])
			ctr,rpm = myStatsItem.proWindowStats()
			print "PERWINDOW--- ctrValue: %.3f | rpmValue: %.3f"%(ctr,rpm)
		if i%5 == 0:
			myStatsItem.update("1","-1")
		elif i%10 == 0:
			myStatsItem.update("1","1")
		else:
			myStatsItem.update("-1","-1")


