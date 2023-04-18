#!usr/bin/env python
# -*- coding:utf-8 _*-
"""
author: Miguitian
@time: 2022/10/28
@file: run.py
@description: 负责系统的初始化等
"""
import uvicorn
from app import api
from config import ServerConfig
from logger import LOGGING_CONFIG

if __name__ == '__main__':
    PORT = ServerConfig.get_config_value("port", default_value=8000)
    uvicorn.run(api.APP, host="0.0.0.0", port=PORT, log_config=LOGGING_CONFIG)
