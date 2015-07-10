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
#发送数据插件
import setmcdata
#内容落地插件
import writefile
#------------------------START-----------------------------------
#可以import自己的配置文件

#------------------------END-------------------------------------

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

    #------------------------START-----------------------------------
    #如果需要将队列中获取的内容落地，则需要加上这段代码
    #------------------------END-------------------------------------

    #循环从队列中获取数据
    get_null_count = 0
    while  True :
        #如果接收到kill信号，则会做如下退出处理
        #recv kill signal the break loop
        if break_flag :
            print "break while loop in " + name
            fastlog.info("break while loop in " + name)
            ##------------------------START-----------------------------------
            ##结束进程前的后续操作
            ##------------------------END-------------------------------------
            break
        try :
            #从连接上的队列集群中，随机一台服务器中获取一条数据
            (result_data, server_addr) = get_queue_data.randomgetonedata()
            if result_data == None or result_data == "" :
                get_null_count += 1
                if get_null_count >= 10 :
                    get_null_count = 0
                    time.sleep(0.05)
                continue
            #fastlog.info("server: " + server_addr + " data: " + result_data)
            get_null_count = 0

            ## parser action data
            #------------------------START-----------------------------------
            #二次开发者根据需求解析这一条数据
            print "server: " + server_addr + " data: " + result_data
            sys.stdout.flush()

            #------------------------END-------------------------------------

        except Exception, e:
            fastlog.error("parser data Exception: " + str(e) + " data: " + str(result_data))



##-----------------------------------------------------------
#能够单独运行，可以测试程序
if __name__ == '__main__':
    property_dict_str='{"mod":"test_action","process_num":2,"key":"test_3","out_path":"/data1/zhanghan/effectMonitor/server","servers":"10.75.29.31:21122","suffix":"txt"}'
    property_dict = json.loads(property_dict_str)
    print "property_dict: " + str(property_dict)
    fastlog.open_log(property_dict["mod"] + ".log")
    #调用run方法就可以进入死循环，测试程序
    run(property_dict)
    print "End"


