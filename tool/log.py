import logging

class Log(object):
    @staticmethod
    def getLog(name):
        logger = logging.getLogger(name)
        logAddress = "%s.log"%"service"
        handler = logging.FileHandler(logAddress)
        formatter = logging.Formatter("[%(levelname)s][%(funcName)s][%(asctime)s]%(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.DEBUG)
        return logger