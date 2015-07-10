#!/usr/bin/python
import logging
import logging.config


class configData():
	def __init__(self,ConfigParser):
		self.expoID = ConfigParser.get("info","expo_ID_key")
		self.click = ConfigParser.get("info","click_key")
		self.achieve = ConfigParser.get("info","achieve_key")
		self.businessID = ConfigParser.get("info","business_ID_key")
		self.candtypeID = ConfigParser.get("info","candtype_ID_key")
		self.primTemplateID = ConfigParser.get("info","prim_temp_ID_key")
		self.secondTemplateID = ConfigParser.get("info","sec_temp_ID_key")
		self.expoSource = ConfigParser.get("info","expo_source_key")
		self.createTime = ConfigParser.get("info","create_time_key")
		self.timestamp = ConfigParser.get("info","timestamp_key")
		self.weight = ConfigParser.get("info","weight_key")

		self.delayPostNum = ConfigParser.get("info","delay_post_num")
		
		self.windowLength = ConfigParser.get("time","window_length")
		self.shortTimePeriod = ConfigParser.get("time","short_time_period")
		self.longTimePeriod = ConfigParser.get("time","long_time_period")

		self.keyTablePath = ConfigParser.get("path","key_table_path")
		self.postUrlPath = ConfigParser.get("path","post_url_path")
		self.delUrlPath = ConfigParser.get("path","del_url_path")

		self.loggerConfPath = ConfigParser.get("logger","file_path")
		self.loggerName = ConfigParser.get("logger","logger_name")

if __name__=="__main__":
	import ConfigParser
	cf = ConfigParser.ConfigParser()
	cf.readfp(open('./conf/rinMethod.ini','r'))
	c = configData(cf)
	print c.expoID
	print c.click
	print c.achieve
	print c.businessID
	print c.candtypeID
	print c.primTemplateID
	print c.secondTemplateID
	print c.expoSource
	print c.createTime
	print c.timestamp
	print c.weight
	
	print c.delayPostNum
	print c.windowLength
	print c.shortTimePeriod
	print c.longTimePeriod
	print c.postUrlPath
	print c.delUrlPath
	print c.loggerConfPath
	print c.loggerName
	logging.config.fileConfig(c.loggerConfPath)
	mylogger = logging.getLogger(c.loggerName)

	mylogger.info("This is info message")
	

