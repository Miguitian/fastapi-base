#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    desc: 日志打印相关
    author: miguitian
    date: 2021-02-01
"""

import os
import logging
import logging.handlers
from colorlog import ColoredFormatter
from conf import config

LOG_PATH = config.LogConfig.get_config_value("log_path")
LOG_LEVEL = config.LogConfig.get_config_value("log_level",
                                              default_value='info').lower()

LOG_LEVEL_MAPPINGS = {
    'notset': logging.NOTSET,
    'debug': logging.DEBUG,
    'info': logging.INFO,
    'warning': logging.WARNING,
    'error': logging.ERROR,
    'critical': logging.CRITICAL
}


def Logger(name):
    logger = logging.getLogger(name)
    logger.propagate = False  # 防止日志重复打印 logger.propagate 布尔标志, 用于指示消息是否传播给父记录器
    logger.setLevel(LOG_LEVEL_MAPPINGS[LOG_LEVEL])
    LOGFORMAT = '%(log_color)s%(asctime)s-%(name)s %(levelname)s:  %(message)s'
    format_str = ColoredFormatter(LOGFORMAT,
                                  log_colors={'DEBUG': 'white',
                                              'INFO': 'bold_white',
                                              'WARNING': 'bold_yellow',
                                              "ERROR": 'bold_red'})

    sh = logging.StreamHandler()
    sh.setFormatter(format_str)

    if LOG_PATH:
        if not os.path.exists(LOG_PATH):
            os.makedirs(LOG_PATH, exist_ok=True)
        # 按照文件大小进行存储
        # th = logging.handlers.RotatingFileHandler(os.path.join(LOG_PATH, '{}.log'.format(name)), mode='a',
        #                                           maxBytes=1024 * 1024 * 100,
        #                                           backupCount=10, encoding='utf-8')

        # 按照时间进行存储
        th = logging.handlers.TimedRotatingFileHandler(
            os.path.join(LOG_PATH, name),
            when="midnight",
            interval=1,
            backupCount=30,
            encoding='utf-8'
        )
        format_str = logging.Formatter(
            '%(asctime)s-%(name)s-%(levelname)s:  %(message)s')
        th.setFormatter(format_str)
        logger.addHandler(th)

    logger.addHandler(sh)
    return logger


logger = Logger("app")
