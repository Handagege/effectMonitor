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
data = "expo_id:1020304949|click:1|achieve:-1|business_id:123|candtype_id:234|prim_temp_id:345|sec_temp_id:456|expo_source:wep|create_time:1411111111|timestamp:1400013223|weight:1"
set_mc_data.setmc("test_3",data,10)
