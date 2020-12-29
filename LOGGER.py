import logging as lg
from logging.handlers import RotatingFileHandler


class Logger:

    def __init__(self, log_id, path):
        self.log = lg.getLogger(log_id)
        self.log.setLevel(lg.DEBUG)
        # create file handler which logs even debug messages
        # f = lg.FileHandler(path, encoding="windows-1251")
        f = RotatingFileHandler(path, maxBytes=1000000,
                                backupCount=5, encoding="windows-1251")
        f.setLevel(lg.DEBUG)
        # create console handler with a higher log level
        c = lg.StreamHandler()
        c.setLevel(lg.DEBUG)
        # create formatter and add it to the handlers
        forma = lg.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', "%d.%m.%Y %H:%M:%S")
        f.setFormatter(forma)
        c.setFormatter(forma)
        # add the handlers to the logger
        self.log.addHandler(f)
        self.log.addHandler(c)

    def info(self, msg):
        self.log.info(msg)

    def error(self, msg):
        self.log.error(msg)


if __name__ == '__main__':
    logger = Logger("Main", 'Robot_log.log')
    logger.info('Test')
