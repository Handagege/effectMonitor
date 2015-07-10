#!/usr/bin/python

import logging
import logging.config

logging.config.fileConfig("effectiveMonitorLogger.conf")
logger = logging.getLogger("general")


logger.debug('This is debug message')
logger.info('This is info message')
logger.warning('This is warning message')

i = 1
logger.debug("this is %d"%(i))

dic = {"aaa":1,"bbb":2}
logger.debug(dic)
