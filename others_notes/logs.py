# -*- coding: utf-8 -*-
import os
import logging
from concurrent_log_handler import ConcurrentRotatingFileHandler

# 日志文件的路径
LOG_DIRECTORY = "logs/"


def log_handler(name, log_level=logging.INFO, console_out=False):
    if not os.path.exists(LOG_DIRECTORY):
        os.makedirs(LOG_DIRECTORY)

    error_logfile = LOG_DIRECTORY + 'error_%s.log' % name
    info_logfile = LOG_DIRECTORY + 'info_%s.log' % name
    fmt = '%(asctime)s - [pid:%(process)d] %(processName)s - %(filename)s[line:%(lineno)d] %(levelname)s - %(message)s'
    formatter = logging.Formatter(fmt)
    # handler = TimedRotatingFileHandler(log_file, when='MIDNIGHT', interval=1, backupCount=5)
    error_handler = ConcurrentRotatingFileHandler(error_logfile, "a", 1024 * 1024 * 40, 5, encoding='utf-8')
    error_handler.setFormatter(formatter)
    error_handler.setLevel(logging.ERROR)

    info_handler = ConcurrentRotatingFileHandler(info_logfile, "a", 1024 * 1024 * 40, 5, encoding='utf-8')
    info_handler.setFormatter(formatter)
    info_handler.setLevel(log_level)
    logger = logging.getLogger(name)

    logger.addHandler(error_handler)
    logger.addHandler(info_handler)

    if console_out is True:
        console_handler = logging.StreamHandler()
        formatter = logging.Formatter(fmt)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    logger.setLevel(log_level)
    return logger


class LogHolder(object):
    def __init__(self):
        self.log = None

    def init_log(self, level=logging.DEBUG, console_out=False, name=None):
        if isinstance(level, str):
            level = level.lower()
        if level == 'debug':
            level = logging.DEBUG
        elif level == 'info':
            level = logging.INFO
        elif level == 'warning':
            level = logging.WARNING
        elif level == 'error':
            level = logging.ERROR
        else:
            level = logging.DEBUG

        self.log = log_handler(name, log_level=level, console_out=console_out)

    def __getattr__(self, item):
        if item == 'init_log':
            return self.init_log
        else:
            if self.log is None:
                raise Exception('logging is not initialized')
            return getattr(self.log, item)


def init_log(folder, filename):
    if not os.path.exists(folder):
        os.makedirs(folder)
    logger = logging.getLogger('videos')
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(filename)s - [line:%(lineno)d] - %(message)s')

    # info级别
    handler_info = logging.FileHandler(f'{folder}/{filename}_info.log', 'a', encoding='utf8')
    handler_info.setLevel(logging.INFO)
    handler_info.setFormatter(formatter)
    logger.addHandler(handler_info)

    # waring级别
    handler_warning = logging.FileHandler(f'{folder}/{filename}_warning.log', 'a', encoding='utf8')
    handler_warning.setLevel(logging.WARNING)
    handler_warning.setFormatter(formatter)
    logger.addHandler(handler_warning)

    # error 级别
    handler_error = logging.FileHandler(f'{folder}/{filename}_error.log', 'a', encoding='utf8')
    handler_error.setLevel(logging.WARNING)
    handler_error.setFormatter(formatter)
    logger.addHandler(handler_error)

    # 控制台打印
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    return logger


if __name__ == "__main__":
    logger = LogHolder()
    pass
