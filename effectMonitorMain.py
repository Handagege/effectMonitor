#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
import os
import sys
import signal
import json
import urllib2
##------------------TEST START-----------------------------------------
local_path=os.path.split(os.path.realpath(__file__))[0]
num=local_path.rfind('/')
local_path=local_path[0:num]
sys.path.append(local_path + "/package")
sys.path.append(local_path + "/lib")
##------------------TEST END ------------------------------------------

##使用相关插件
#日志处理插件
import fastlog
#接收数据插件
import getqueuedata

#my define module
import ConfigParser
import configData
import stdSampleParser
import timeManager
import effectMonitor

#框架固定代码
break_flag = False
def onsignal_term(a,b):
	global break_flag
	print str(__file__) + "  " + str(os.getpid()) + " process recv signal"
	fastlog.info(str(__file__) + "  " + str(os.getpid()) + " process recv signal")
	break_flag = True
#------------------------START-----------------------------------
#二次开发自定义处理逻辑与方法

#------------------------END-------------------------------------

#框架固定代码，传入的参数property_dict，为配置文件中json串，转化为dict
def run(property_dict) :
	pid = os.getpid()
	name = str(property_dict["key"])
	#设置log输出logid
	fastlog.set_logid(name + "_" + str(pid))
	#信号处理函数
	signal.signal(signal.SIGTERM, onsignal_term)
	#根据配置中定义的队列服务器地址和key，连接队列服务器
	get_queue_data = getqueuedata.GetQueuData(property_dict["servers"], str(property_dict["key"]))

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
	now = time.time()
	t.setEndPoint(int(now))
	effectMonitorInstance = effectMonitor.effectMonitor(c,t)
	##------------------------END-----------------------------------

	#循环从队列中获取数据
	get_null_count = 0
	while  True :
		#如果接收到kill信号，则会做如下退出处理
		if break_flag :
			print "break while loop in " + name
			fastlog.info("break while loop in " + name)
			##------------------------START-----------------------------------
			##结束进程前的后续操作
			##------------------------END-------------------------------------
			break
		try :
			#从连接上的队列集群中，随机一台服务器中获取一条数据
			#------------------------START-----------------------------------
			(data, server_addr) = get_queue_data.randomgetonedata()
			if data == None or data == "" :
				get_null_count += 1
				if get_null_count >= 10 :
					get_null_count = 0
					time.sleep(0.05)
				continue
			#fastlog.info("server: " + server_addr + " data: " + data)
			get_null_count = 0
			#------------------------END-------------------------------------

			#------------------------START-----------------------------------
			#print data
			effectMonitorInstance.deal(parser.parse(data))
			effectMonitorInstance.printStatsItemMsgToLog()
			parser.clear()
			#------------------------END-------------------------------------
		except Exception, e:
			fastlog.error("parser data Exception: " + str(e) + " data: " + str(data))



#能够单独运行，可以测试程序
if __name__ == '__main__':
	property_dict_str='{"mod":"test_action","process_num":1,"key":"eros_statistic_result1","out_path":"/data1/zhanghan/effectMonitor/server","servers":"mcq.recom.i.weibo.com:21122","suffix":"txt"}'
	property_dict = json.loads(property_dict_str)
	fastlog.open_log(property_dict["mod"] + ".log")
	#调用run方法就可以进入死循环，测试程序
	run(property_dict)
	print "End"


