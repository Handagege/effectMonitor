#!/usr/bin/python

import time
import os
import sys
import signal

local_path=os.path.split(os.path.realpath(__file__))[0]
num=local_path.rfind('/')
local_path=local_path[0:num]
sys.path.append(local_path + "/package")
sys.path.append(local_path + "/lib")

import memcache
import setmcdata

mc_server_list = ["10.75.29.31:21122"]
set_mc_data = setmcdata.SetMC(mc_server_list)
print ".................first stats item data................"
data = "expo_id:1234567|click:1|achieve:-1|business_id:userprofile|candtype_id:candtype1|prim_temp_id:pt1|sec_temp_id:st1|expo_source:web|create_time:1435313246|timestamp:1435313200|weight:1"
set_mc_data.setmc("test_2",data,10)
print ".................second stats item data................"
data = "expo_id:12345678|click:1|achieve:1|business_id:userprofile|candtype_id:candtype2|prim_temp_id:pt1|sec_temp_id:st2|expo_source:web|create_time:1435313230|timestamp:1435313200|weight:1"
set_mc_data.setmc("test_2",data,10)
print ".................third stats item data................"
data = "expo_id:123456789|click:-1|achieve:-1|business_id:userprofile|candtype_id:candtype2|prim_temp_id:pt1|sec_temp_id:st2|expo_source:web|create_time:1435313480|timestamp:1435313200|weight:1"
set_mc_data.setmc("test_2",data,10)
print ".................forth stats item data................"
data = "expo_id:123456789|click:-1|achieve:-1|business_id:userprofile|candtype_id:candtype2|prim_temp_id:pt1|sec_temp_id:st1|expo_source:web|create_time:1435313480|timestamp:1435313200|weight:1"
set_mc_data.setmc("test_2",data,10)
