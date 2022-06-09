import logging
from datetime import datetime
from random import randint
import sys


def initLogger(logLevel):
    def getLoggerName(logLevel):
        logName=""
        if(logLevel==logging.INFO):logName="info" 
        if(logLevel==logging.ERROR):logName="error"
        if(logLevel==logging.DEBUG):logName="debug"
        return logName

    def initLogFilePath(logName):
        currentTime = datetime.now()
        currentTimeString= currentTime.strftime("%Y-%m-%d")
        LogFilePath = "./tmp/"+logName+"_"+currentTimeString+".log"
        return LogFilePath

    def setLogger(testLogger,logLevel):
        logFilePath = initLogFilePath(getLoggerName(logLevel))
        streamHandler = logging.StreamHandler(sys.stdout)
        fileHandler = logging.FileHandler(logFilePath, mode = 'a')
        streamFormatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%H:%M:%S')
        fileFormatter = logging.Formatter('%(asctime)s,%(levelname)s,%(message)s', datefmt='%H:%M:%S')
        streamHandler.setFormatter(streamFormatter)
        fileHandler.setFormatter(fileFormatter)
        testLogger.addHandler(streamHandler)
        testLogger.addHandler(fileHandler)
        return testLogger

    testLogger = logging.getLogger('logger_'+str(randint))
    testLogger.setLevel(logLevel)
    mylogger = setLogger(testLogger,logLevel)
    return mylogger

infoLogger = initLogger(logging.INFO)