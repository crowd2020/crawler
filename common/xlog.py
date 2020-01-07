#!/bin/env python
# -*-coding:utf-8-*-

import logging
import logging.config
import sys

import logging.handlers
from logging.handlers import DatagramHandler

class UdpHandler(DatagramHandler):
    """
    Send log which is already formatted to the recieve end in the string format.
    """
    def emit(self, record):
        try:
            log_line = "%s\n" % self.format(record)
            self.send(log_line)
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            self.handleError(record)
vars(logging)[UdpHandler.__name__] = UdpHandler


class Log:
    def __init__(self):
        home_path = sys.path[0]
        logging_conf = "%s/../conf/logging.conf" % home_path
        try:
            logging.config.fileConfig(logging_conf)
        except Exception, e:
            print ("ERROR: log conf failed to load %s" % logging_conf)
            logging.config.dictConfig({
                'version': 1,
                'disable_existing_loggers': False,
                'formatters': {
                    'standard': {
                        'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
                    },
                },
                'handlers': {
                    'default': {
                        'level': 'DEBUG',
                        'class': 'logging.StreamHandler',
                    },
                },
                'loggers': {
                    'root': {
                        'handlers': ['default'],
                        'level': 'DEBUG',
                        'propagate': True
                    },
                }
            })
        self.logger = logging.getLogger("root")

    def get_logger(self, name):
        return logging.getLogger(name)

    def wrap_msg(func):
        def _(self, format_str, *args):
            filename = sys._getframe().f_back.f_code.co_filename
            filename = filename.split('/')[-1]
            func_name = sys._getframe().f_back.f_code.co_name
            line_number = sys._getframe().f_back.f_lineno
            msg = (format_str % args) if len(args)>0 else format_str
            new_msg = "[%s:%d] [%s] %s" % (filename, line_number, func_name, msg)
            func(self, new_msg)
        return _

    @wrap_msg
    def DEBUG(self, format_str, *args):
        self.logger.debug(format_str)

    @wrap_msg
    def INFO(self, format_str, *args):
        self.logger.info(format_str)

    @wrap_msg
    def WARN(self, format_str, *args):
        self.logger.warn(format_str)

    @wrap_msg
    def ERROR(self, format_str, *args):
        self.logger.error(format_str)

    @wrap_msg
    def FATAL(self, format_str, *args):
        self.logger.fatal(format_str)

LOG = Log()
