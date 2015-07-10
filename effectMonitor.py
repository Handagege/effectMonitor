#!/usr/bin/python
# -*- coding: utf-8 -*-

import statsItem
import urllib
import urllib2
import copy
import time
import logging
import logging.config
from chartConfProducer import *
from statsItem import *

class effectMonitor():
	def __init__(self,configData,timeManager):
		#时间管理器，用于储存更新时间数据
		self.timeManager = timeManager
		#配置信息
		self.configData = configData
		#配置logger
		logging.config.fileConfig(self.configData.loggerConfPath)
		self.logger = logging.getLogger(self.configData.loggerName)
		#最近一段时间的数据窗口长度
		self.windowLength = int(configData.windowLength)
		#最大可延迟处理的数据条数，用于解决数据发送时间的混淆
		self.delayPostNum = int(configData.delayPostNum)
		#暂时存储延迟数据
		self.delayDataList = []
		#用于解析key值以便发送数据
		self.parseKeysDic = {}
		#所有的统计状态
		self.allInOneDic = {}
		#用于标记新的key值
		self.newKeyFlag = False
		#用于标记特征、算法、候选
		self.indexList = ["-",":",","]
		#标准标记符
		self.stdIndex = ":"
		#不同数据类型key尾缀
		self.keySuffixList = [":tpoint:ctr",":tpoint:rpm",":tperiod:ctr",":tperiod:rpm"]
		#self.timePeriodMark = ":tperiod"
		#self.timePointMark = ":tpoint"
		#前缀
		self.keyPrefix = "eros:"
		self.ccProducer = chartConfProducer(self.configData.keyTablePath,self.keyPrefix,self.keySuffixList)

	def deal(self,dataDic):
		dataIntegrityFlag = True
		dataCorrectFlag = True
		keyTime = dataDic.get(self.configData.createTime,None)
		businessID = dataDic.get(self.configData.businessID,None)
		candtypeID = dataDic.get(self.configData.candtypeID,None)
		primTemplateID = dataDic.get(self.configData.primTemplateID,None)
		secondTemplateID = dataDic.get(self.configData.secondTemplateID,None)
		click = dataDic.get(self.configData.click,None)
		achieve = dataDic.get(self.configData.achieve,None)
		#judge data integrity
		if (keyTime == None or businessID == None or candtypeID == None or\
			primTemplateID == None or secondTemplateID == None or \
			click == None or achieve == None) or (keyTime == "" or \
			businessID == "" or candtypeID == "" or primTemplateID == "" or\
			secondTemplateID == "" or click == "" or achieve == ""):
			dataIntegrityFlag = False
		#judge data correct
		try:
			click_int = int(click)
			achieve_int = int(achieve)
			keyTime = int(keyTime)
		except ValueError:
			self.logger.error("have some data error(click or achieve) can't tansfer to int")
			dataCorrectFlag = False
		
		if dataIntegrityFlag and dataCorrectFlag:	
			shortEndPoint = self.timeManager.shortEndPoint
			shortPeriod = self.timeManager.shortPeriod
			shortStartPoint = shortEndPoint-shortPeriod*self.windowLength
			longEndPoint = self.timeManager.longEndPoint
			#check the key exist
			self.addNewStatsItem(businessID,businessID)
			bToC_key = businessID + self.stdIndex + candtypeID
			bToC_parseKey = businessID + self.indexList[0] + candtypeID
			self.addNewStatsItem(bToC_key,bToC_parseKey)
			bToF_key = businessID + self.stdIndex + primTemplateID
			bToF_parseKey = businessID + self.indexList[1] + primTemplateID
			self.addNewStatsItem(bToF_key,bToF_parseKey)
			bToF_toA_key = businessID + self.stdIndex + primTemplateID + self.stdIndex + secondTemplateID
			bToF_toA_parseKey = businessID + self.indexList[2] + primTemplateID + self.indexList[2] + secondTemplateID
			self.addNewStatsItem(bToF_toA_key,bToF_toA_parseKey)
			#update key table
			if self.newKeyFlag:
				self.logger.debug("-----------|update key table|-----------")
				self.updateKeyTable()
			#deal time window stats	
			updateDayStatsFlag = True
			self.logger.debug("......................start.....................")
			self.logger.debug(dataDic)
			self.logger.debug("short post time point is %d"%(self.timeManager.shortEndPoint))
			self.logger.debug("long post time point is %d"%(self.timeManager.longEndPoint))
			if keyTime >= shortStartPoint and keyTime < shortEndPoint:
				pos = int((keyTime-shortStartPoint)/shortPeriod)
				##update four level data
				self.allInOneDic[businessID].updateWindowStats(click,achieve,pos)
				self.allInOneDic[bToC_key].updateWindowStats(click,achieve,pos)
				self.allInOneDic[bToF_key].updateWindowStats(click,achieve,pos)
				self.allInOneDic[bToF_toA_key].updateWindowStats(click,achieve,pos)
			elif keyTime >= shortEndPoint:
				self.logger.debug(".................post window stats................")
				self.delayDataList.append(copy.deepcopy(dataDic))
				updateDayStatsFlag = False
				l = len(self.delayDataList)
				self.logger.debug("delay list len : %d"%(l))
				if self.delayPostNum < l:
					self.postWindowStats()
					self.timeManager.updateShortPoint()
					self.logger.debug("after update short end time point is %d"%(self.timeManager.shortEndPoint))
					tempDelayDataList = copy.deepcopy(self.delayDataList)
					self.delayDataList = []
					for i in tempDelayDataList:
						self.logger.debug("*************deal delay data**************")
						self.deal(i)

			#deal day stats
			if updateDayStatsFlag:
				if keyTime > longEndPoint:
					self.logger.debug(".................post day stats.................")
					#print longEndPoint
					self.postDayStats()
					self.timeManager.updateLongPoint()
					self.addNewStatsItem(businessID,businessID)
					self.addNewStatsItem(bToC_key,bToC_parseKey)
					self.addNewStatsItem(bToF_key,bToF_parseKey)
					self.addNewStatsItem(bToF_toA_key,bToF_toA_parseKey)
				self.allInOneDic[businessID].updateDayStats(click,achieve)
				self.allInOneDic[bToC_key].updateDayStats(click,achieve)
				self.allInOneDic[bToF_key].updateDayStats(click,achieve)
				self.allInOneDic[bToF_toA_key].updateDayStats(click,achieve)

	def postWindowStats(self):
		keyTime = self.timeManager.shortEndPoint-self.timeManager.shortPeriod
		postFlag = True
		printFlag = True
		for key in self.allInOneDic:
			(ctr,rpm) = self.allInOneDic[key].proWindowStats()
			postCtrKey = self.keyPrefix + key + self.keySuffixList[2]
			postRpmKey = self.keyPrefix + key + self.keySuffixList[3]
			if postFlag:
				response = urllib.urlopen(self.configData.postUrlPath,self.constructUrlData(postCtrKey,int(ctr),keyTime))
				self.logger.debug("[%s] ctr post success or fail:%s"%(postCtrKey,response.read()))
				response = urllib.urlopen(self.configData.postUrlPath,self.constructUrlData(postRpmKey,int(rpm),keyTime))
				self.logger.debug("[%s] rpm post success or fail:%s"%(postRpmKey,response.read()))
			if printFlag:
				self.logger.debug("[%s] windowStats----time:%s ctr:%0.3f"%(postCtrKey,time.strftime('%Y%m%d%H%M%S',time.localtime(keyTime)),ctr))
				self.logger.debug("[%s] windowStats----time:%s rpm:%0.3f"%(postRpmKey,time.strftime('%Y%m%d%H%M%S',time.localtime(keyTime)),rpm))

	def postDayStats(self):
		keyTime = self.timeManager.longEndPoint-self.timeManager.longPeriod
		postFlag = True
		updateKeyTableFlag = False
		for key in self.parseKeysDic.keys():
			(ctr,rpm) = self.allInOneDic[self.parseKeysDic[key]].proDayStats()
			self.allInOneDic[self.parseKeysDic[key]].flushDayStats()
			postCtrKey = self.keyPrefix + self.parseKeysDic[key] + self.keySuffixList[0]
			self.logger.debug("[%s] dayStats----time:%d ctr:%0.3f"%(postCtrKey,keyTime,ctr))
			postRpmKey = self.keyPrefix + self.parseKeysDic[key] + self.keySuffixList[1]
			self.logger.debug("[%s] dayStats----time:%d rpm:%0.3f"%(postRpmKey,keyTime,rpm))
			#如果一天没有数据，则删除这条key，不显示这条数据
			if ctr == 0.0:
				del self.allInOneDic[self.parseKeysDic[key]]
				del self.parseKeysDic[key]
				updateKeyTableFlag = True
			if postFlag:
				response = urllib.urlopen(self.configData.postUrlPath,self.constructUrlData(postCtrKey,ctr,keyTime))
				response = urllib.urlopen(self.configData.postUrlPath,self.constructUrlData(postRpmKey,rpm,keyTime))
		if updateKeyTableFlag:
			self.updateKeyTable()

	
	def constructUrlData(self,key,rank,time):
		para_dic = {}
		para_dic["key"] = key
		para_dic["rank"] = rank
		para_dic["time"] = time
		return urllib.urlencode(para_dic)

	def addNewStatsItem(self,stdKey,parseKey):
		if parseKey not in self.parseKeysDic:
			self.allInOneDic[stdKey] = statsItem(self.windowLength)
			self.parseKeysDic[parseKey] = stdKey
			self.newKeyFlag = True

	def updateKeyTable(self):
		self.newKeyFlag = False
		#file = open(self.configData.keyTablePath,'w')
		candtypeList = []
		featureList = []
		feature_algorithmList = []
		businessList = []
		for key in self.parseKeysDic:
			if key.rfind(self.indexList[0]) != -1:
				candtypeList.append(self.parseKeysDic[key])
			elif key.rfind(self.indexList[1]) != -1:
				#key = key.replace(self.indexList[1],self.stdIndex)
				featureList.append(self.parseKeysDic[key])
			elif key.rfind(self.indexList[2]) != -1:
				feature_algorithmList.append(self.parseKeysDic[key])
			else:
				businessList.append(key)
		candtypeMap = self.parseKeyToMap(candtypeList)
		featureMap = self.parseKeyToMap(featureList)
		feature_algorithmMap = self.parseKeyToMap(feature_algorithmList)
		businessMap = {}
		businessMap["business"] = businessList
		self.ccProducer.deal(businessMap,candtypeMap,featureMap,feature_algorithmMap)
		#self.writeKeyMapToFile(file,candtypeMap,"-候选")
		#file.write('------------------------------\n')
		#self.writeKeyMapToFile(file,featureMap,"-特征")
		#file.write('------------------------------\n')
		#self.writeKeyMapToFile(file,feature_algorithmMap,"-特征-算法")
		#file.write('------------------------------\n')
		#self.writeKeyMapToFile(file,businessMap,"")
	
	def parseKeyToMap(self,dataList):
		keyMap = {}
		for i in dataList:
			pos = i.rfind(self.stdIndex)
			key = i[:pos]
			if key in keyMap.keys():
				keyMap[key].append(i)
			else:
				keyMap[key] = []
				keyMap[key].append(i)
		return keyMap

	def writeKeyMapToFile(self,file,data,suffix):
		for key in data:
			file.write(key+suffix+"\n")
			for d in data[key]:
				file.write(self.keyPrefix+d+self.keySuffixList[0]+"\n")
				file.write(self.keyPrefix+d+self.keySuffixList[1]+"\n")
				file.write(self.keyPrefix+d+self.keySuffixList[2]+"\n")
				file.write(self.keyPrefix+d+self.keySuffixList[3]+"\n")
		file.write("\n")

	def printStatsItemMsg(self):
		for key in self.allInOneDic:
			print "***...[%s] itemStatsMsg...***"%(key)
			self.allInOneDic[key].printMsg()
	
	def printStatsItemMsgToLog(self):
		for key in self.allInOneDic:
			self.logger.debug("***...[%s] itemStatsMsg...***"%(key))
			self.allInOneDic[key].printMsgToLog(self.logger)
		self.logger.debug("......................end.....................\n")
		

def test1():
	import ConfigParser
	import timeManager
	import configData
	import stdSampleParser
	##my data prepare
	##------------------------START-----------------------------------
	#configure message
	cf = ConfigParser.ConfigParser()
	cf.readfp(open('./conf/rinMethod.ini','r'))
	c = configData.configData(cf)
	#data parser
	parser = stdSampleParser.stdSampleParser()
	#init timeManager data
	t = timeManager.timeManager(int(c.longTimePeriod),int(c.shortTimePeriod))
	t.setEndPoint(1435313248)

	print ".................first stats item data................"
	data = "expo_id:1234567|click:1|achieve:-1|business_id:userprofile|candtype_id:candtype1|prim_temp_id:pt1|sec_temp_id:st1|expo_source:web|create_time:1435313246|timestamp:1435313200|weight:1"
	#key processer
	data = parser.parse(data)
	effectMonitorInstance = effectMonitor(c,t)
	effectMonitorInstance.deal(data)
	print(data)
	parser.clear()
	effectMonitorInstance.printStatsItemMsg()

	print ".................second stats item data................"
	data = "expo_id:12345678|click:1|achieve:1|business_id:userprofile|candtype_id:candtype2|prim_temp_id:pt1|sec_temp_id:st2|expo_source:web|create_time:1435313230|timestamp:1435313200|weight:1"
	data = parser.parse(data)
	effectMonitorInstance.deal(data)
	print(data)
	effectMonitorInstance.printStatsItemMsg()
	parser.clear()

	print ".................third stats item data................"
	data = "expo_id:123456789|click:-1|achieve:-1|business_id:userprofile|candtype_id:candtype2|prim_temp_id:pt1|sec_temp_id:st2|expo_source:web|create_time:1435313480|timestamp:1435313200|weight:1"
	data = parser.parse(data)
	effectMonitorInstance.deal(data)
	print(data)
	effectMonitorInstance.printStatsItemMsg()
	parser.clear()

	print ".................forth stats item data................"
	data = "expo_id:123456789|click:-1|achieve:-1|business_id:userprofile|candtype_id:candtype2|prim_temp_id:pt1|sec_temp_id:st1|expo_source:web|create_time:1435313480|timestamp:1435313200|weight:1"
	data = parser.parse(data)
	effectMonitorInstance.deal(data)
	print(data)
	effectMonitorInstance.printStatsItemMsg()
	parser.clear()

	print ".................fifth stats item data................"
	data = "expo_id:123456789|click:1|achieve:-1|business_id:userprofile|candtype_id:candtype2|prim_temp_id:pt1|sec_temp_id:st1|expo_source:web|create_time:1435313000|timestamp:1435313200|weight:1"
	data = parser.parse(data)
	effectMonitorInstance.deal(data)
	print(data)
	effectMonitorInstance.printStatsItemMsg()
	parser.clear()

	print ".................sixth stats item data................"
	data = "expo_id:123456789|click:1|achieve:-1|business_id:userprofile|candtype_id:candtype3|prim_temp_id:pt3|sec_temp_id:st1|expo_source:web|create_time:1435312700|timestamp:1435313200|weight:1"
	data = parser.parse(data)
	effectMonitorInstance.deal(data)
	print(data)
	effectMonitorInstance.printStatsItemMsg()
	parser.clear()
	
	print effectMonitorInstance.parseKeysDic
	effectMonitorInstance.postDayStats()
	##------------------------END-----------------------------------

def test2():
	import random
	import time
	import ConfigParser
	import timeManager
	import configData
	import stdSampleParser
	##my data prepare
	##------------------------START-----------------------------------
	#configure message
	cf = ConfigParser.ConfigParser()
	cf.readfp(open('./conf/rinMethod.ini','r'))
	c = configData.configData(cf)
	#data parser
	parser = stdSampleParser.stdSampleParser()
	#init timeManager data
	t = timeManager.timeManager(int(c.longTimePeriod),int(c.shortTimePeriod))
	now = int(time.time())
	t.setEndPoint(now)
	#key processer
	effectMonitorInstance = effectMonitor(c,t)

	intList = [-1,1]
	#candtypeList = ["c001","c002"]
	candtypeList = ["c001"]
	#businessList = ["b001","b002"]
	businessList = ["b001"]
	for i in range(1,200):
		#print ".................%d stats item data................"%(i)
		#print "------------------------START------------------------------"
		msg = ".................%d stats item data................"%(i)
		effectMonitorInstance.logger.debug(msg)
		effectMonitorInstance.logger.debug("------------------------START------------------------------")
		achieve = random.choice(intList)
		click = 1
		if achieve == -1:
			click = random.choice(intList)
		createTime = random.randint(-4,10)+now
		now = createTime
		candtype = random.choice(candtypeList)
		business = random.choice(businessList)
		data = "expo_id:1234567|click:%d|achieve:%d|business_id:%s|candtype_id:%s|prim_temp_id:pt1|sec_temp_id:st1|expo_source:web|create_time:%d|timestamp:1435313246|weight:1"%(click,achieve,business,candtype,createTime)
		#print data
		effectMonitorInstance.logger.debug(data)
		data = parser.parse(data)
		effectMonitorInstance.deal(data)
		parser.clear()
		effectMonitorInstance.printStatsItemMsgToLog()
		effectMonitorInstance.logger.debug("------------------------END------------------------------\n")
		#time.sleep(1)

if __name__ == "__main__":
	test2()
