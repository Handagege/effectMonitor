#!/usr/bin/python

import json

class chartConfProducer():
	def __init__(self,outFilePath,keyPrefix = "eros:",keySuffixList = [":tpoint:ctr",":tpoint:rpm",":tperiod:ctr",":tperiod:rpm"]):
		self.sectionKey = "sections"
		self.chartKey = "charts"
		self.timeKey = "time"
		self.dayPeriodKey = "d"
		self.monthPeriodKey = "m"
		self.sixHourPeriodKey = "S"
		self.nameKey = "name"
		self.itemKey = "item"
		self.kKey = "key"
		self.chartNameList = ["day:ctr","day:rpm","range:ctr","range:rpm"]
		self.timePeriodList = [self.monthPeriodKey,self.monthPeriodKey,self.sixHourPeriodKey,self.sixHourPeriodKey]
		self.candtypeKey = "candidates"
		self.featureKey = "eigenvectors"
		self.algorithmsKey = "algorithms"
		self.outFilePath = outFilePath
		self.keyPrefix = keyPrefix
		self.keySuffixList = keySuffixList

		self.homepageDic = {}
	
	def proHomepageConfFrame(self):
		timeList = [self.monthPeriodKey,self.monthPeriodKey,self.sixHourPeriodKey,self.sixHourPeriodKey]
		chartNameList = self.chartNameList
		itemList = [{}]*4
		sectionDic = {}
		chartDic = {}
		chartDic[self.timeKey] = timeList
		chartDic[self.nameKey] = chartNameList
		chartDic[self.itemKey] = itemList
		sectionDic[self.chartKey] = chartDic
		self.homepageDic[self.sectionKey] = sectionDic

	def deal(self,businessDic,candtypeDic,featureDic,featureToAlgorithmDic):
		#print businessDic
		#print candtypeDic
		#print featureDic
		#print featureToAlgorithmDic
		self.proHomepageConfFrame()
		for i in range(0,4):
			itemDic = {}
			businessList = businessDic["business"]
			completeBusinessList = []
			for j in businessList:
				completeBusinessList.append(self.keyPrefix+j+self.keySuffixList[i])
			itemDic[self.kKey] = completeBusinessList
			itemDic[self.candtypeKey] = self.proCandtypeConfList(businessList,candtypeDic,i)
			itemDic[self.featureKey] = self.proFeatureConfList(businessList,featureDic,featureToAlgorithmDic,i)
			self.homepageDic[self.sectionKey][self.chartKey][self.itemKey][i] = itemDic
		self.writeConfToFile()
	
	def proCandtypeConfList(self,businessKeys,candtypeDic,index):
		resultList = []
		for i in businessKeys:
			minItemDic = self.proMinConfItem(candtypeDic[i],index)
			resultList.append(minItemDic)
		return resultList

	def proFeatureConfList(self,businessKeys,featureDic,featureToAlgorithmDic,index):
		resultList = []
		for i in businessKeys:
			featureKeyList = featureDic[i]
			subDic = self.proMinConfItem(featureKeyList,index)
			subDic[self.algorithmsKey] = []
			for j in featureKeyList:
				subDic[self.algorithmsKey].append(self.proMinConfItem(featureToAlgorithmDic[j],index))
			resultList.append(subDic)
		return resultList

	def proMinConfItem(self,keyList,index):
		itemDic = {}
		itemDic[self.timeKey] = self.timePeriodList[index]
		itemDic[self.nameKey] = self.chartNameList[index]
		stdKeyList = []
		for i in keyList:
			stdKey = self.keyPrefix + i + self.keySuffixList[index]
			stdKeyList.append(stdKey)
		itemDic[self.kKey] = stdKeyList
		#print itemDic
		return itemDic
	
	def writeConfToFile(self):
		f = open(self.outFilePath,"w")
		f.write(json.dumps(self.homepageDic))

