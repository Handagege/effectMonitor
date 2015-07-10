#!/usr/bin/python

class stdSampleParser():
	def __init__(self):
		self.dic_data = {}
	def parse(self,data):
		dataList = data.split("|")
		temp_dic_data = {}
		for i in range(len(dataList)):
			dataNodeList = dataList[i].split(":")
			temp_dic_data[dataNodeList[0]] = dataNodeList[-1]
		self.dic_data = temp_dic_data
		return self.dic_data
	def getExpoID(self,expoID="expo_id"):
		return self.dic_data.get(expoID,None)
	def getClick(self,click="click"):
		return self.dic_data.get(click,None)
	def getAchieve(self,achieve="achieve"):
		return self.dic_data.get(achieve,None)
	def getBusinessID(self,businessID="business_id"):
		return self.dic_data.get(businessID,None)
	def getCandtypeID(self,candtypeID="candtype_id"):
		return self.dic_data.get(candtypeID,None)
	def getPrimTemplateID(self,primTemplateID="prim_temp_id"):
		return self.dic_data.get(primTemplateID,None)
	def getSecondTemplateID(self,secondTemplateID="sec_temp_id"):
		return self.dic_data.get(secondTemplateID,None)
	def getExpoSource(self,expoSource="expo_source"):
		return self.dic_data.get(expoSource,None)
	def getCreateTime(self,createTime="create_time"):
		return self.dic_data.get(createTime,None)
	def getTimeStamp(self,timestamp="timestamp"):
		return self.dic_data.get(timestamp,None)
	def getWeight(self,weight="weight"):
		return self.dic_data.get(weight,None)
	def getDicData(self):
		return self.dic_data
	def clear(self):
		self.dic_data.clear()

if __name__ == "__main__":
	#import ConfigParser
	#config = ConfigParser.ConfigParser()
	#config.readfp(open('./conf/rinMethod.ini','r'))
	stdSampleParser = stdSampleParser()
	data = "expo_id:1020304949|click:1|achieve:-1|business_id:123|candtype_id:234|prim_temp_id:345|sec_temp_id:456|expo_source:wep|create_time:1411111111|timestamp:1400013223|weight:1"
	stdSampleParser.parse(data)
	print "%s"%(stdSampleParser.getExpoID())
	print "%s"%(stdSampleParser.getClick())
	print "%s"%(stdSampleParser.getAchieve())
	print "%s"%(stdSampleParser.getBusinessID())
	print "%s"%(stdSampleParser.getCandtypeID())
	print "%s"%(stdSampleParser.getPrimTemplateID())
	print "%s"%(stdSampleParser.getSecondTemplateID())
	print "%s"%(stdSampleParser.getExpoSource())
	print "%s"%(stdSampleParser.getCreateTime())
	print "%s"%(stdSampleParser.getTimeStamp())
	print "%s"%(stdSampleParser.getWeight())
	print stdSampleParser.getDicData()
