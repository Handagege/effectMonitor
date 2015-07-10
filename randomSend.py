#!/usr/bin/python

import time
import os
import sys
import signal
import random

local_path=os.path.split(os.path.realpath(__file__))[0]
num=local_path.rfind('/')
local_path=local_path[0:num]
sys.path.append(local_path + "/package")
sys.path.append(local_path + "/lib")

import memcache
import setmcdata

mc_server_list = ["10.75.29.31:21122"]
set_mc_data = setmcdata.SetMC(mc_server_list)

#now = time.time()
now = 1435313246
intList = [-1,1]
candtypeList = ["c001","c002"]
businessList = ["b001","b002"]
for i in range(1,21):
	print ".................%d stats item data................"%(i)
	print "------------------------START------------------------------"
	achieve = random.choice(intList)
	click = 1
	if achieve == -1:
		click = random.choice(intList)
	createTime = random.randint(-2,10)+now
	now = createTime
	candtype = random.choice(candtypeList)
	business = random.choice(businessList)
	data = "expo_id:1234567|click:%d|achieve:%d|business_id:%s|candtype_id:%s|prim_temp_id:pt1|sec_temp_id:st1|expo_source:web|create_time:%d|timestamp:1435313246|weight:1"%(click,achieve,business,candtype,createTime)
	print data
	set_mc_data.setmc("test_2",data,10)
	print "------------------------END------------------------------\n"
	time.sleep(3)
