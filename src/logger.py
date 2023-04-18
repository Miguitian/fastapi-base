#!usr/bin/env python
# -*- coding:utf-8 _*-
"""
author: Miguitian
@time: 2022/10/28
@file: logger.py
@description:
"""
# pylint: disable=C0103, E0401, C0116, W0611, C0411
import os
import sys
from config import LogConfig  # pylint: disable=E0401
import logging.handlers
from logging.config import dictConfig
from cloghandler import ConcurrentRotatingFileHandler

LOG_PATH = LogConfig.get_config_value("log_path")
LOG_LEVEL = LogConfig.get_config_value("log_level",
                                       default_value='info').lower()

LOG_LEVEL_MAPPINGS = {
    'notset': logging.NOTSET,
    'debug': logging.DEBUG,
    'info': logging.INFO,
    'warning': logging.WARNING,
    'error': logging.ERROR,
    'critical': logging.CRITICAL
}

if LOG_PATH:

    if not os.path.exists(LOG_PATH):
        os.makedirs(LOG_PATH, exist_ok=True)

    LOGGING_CONFIG_FILE = {
        "version": 1,
        "formatters": {
            "default": {
                'format': '%(asctime)s %(levelname)s  %(message)s',
            },
            "plain": {
                "format": "%(message)s",
            },
            'colored': {
                '()': 'colorlog.ColoredFormatter',
                'format': "%(log_color)s %(asctime)s %(levelname)s %(reset)s %(blue)s%(message)s"}
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "level": LOG_LEVEL_MAPPINGS[LOG_LEVEL],
                "formatter": "colored",
                "stream": sys.stdout,
            },
            # "file": {
            #     "class": "logging.handlers.TimedRotatingFileHandler",  # 该方法为进程不安全，暂时没有解决方案
            #     "level": LOG_LEVEL_MAPPINGS[LOG_LEVEL],
            #     "filename": os.path.join(LOG_PATH, "app.log"),
            #     "encoding": "utf-8",
            #     "formatter": "default",
            #     "when": "M",
            #     "interval": 2,
            #     "backupCount": 30,
            # }
            "file": {
                "class": "logging.handlers.ConcurrentRotatingFileHandler",
                "level": LOG_LEVEL_MAPPINGS[LOG_LEVEL],
                "filename": os.path.join(LOG_PATH, "app.log"),
                "encoding": "utf-8",
                "formatter": "default",
                "mode": "a",
                "maxBytes": 1024 * 1024 * 100,
                "backupCount": 30,
            }
        },
        "loggers": {

            "file_logger": {
                "handlers": ["file", "console"],
                "level": "INFO",
                "propagate": False,
            },
            "uvicorn": {
                "handlers": ["file", "console"],
                "level": "INFO",
                "propagate": False,
            }

        },
        "disable_existing_loggers": True,
        "root": {
            "level": "INFO",  # # handler中的level会覆盖掉这里的level
            "handlers": ["console", "file"],
        }
    }

    LOGGING_CONFIG = LOGGING_CONFIG_FILE
    LOGGER_NAME = 'file_logger'

else:
    LOGGING_CONFIG_CONSOLE = {
        "version": 1,
        "formatters": {
            "default": {
                'format': '%(asctime)s %(levelname)s%(message)s',
            },
            "plain": {
                "format": "%(message)s",
            },
            'colored': {
                '()': 'colorlog.ColoredFormatter',
                'format': "%(log_color)s%(asctime)s %(levelname)s %(reset)s %(blue)s%(message)s"}
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "level": LOG_LEVEL_MAPPINGS[LOG_LEVEL],
                "formatter": "colored",
                "stream": sys.stdout,

            }
        },
        "loggers": {

            "console_logger": {
                "handlers": ["console"],
                "level": "INFO",
                "propagate": False,
            },
            "uvicorn": {
                "handlers": ["console"],
                "level": "INFO",
                "propagate": False,
            }
        },
        "disable_existing_loggers": True,
        "root": {
            "level": "INFO",  # handler中的level会覆盖掉这里的level
            "handlers": ["console"],
        }
    }
    LOGGING_CONFIG = LOGGING_CONFIG_CONSOLE
    LOGGER_NAME = 'console_logger'

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(LOGGER_NAME)  # 不写就是root
