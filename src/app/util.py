#!usr/bin/env python
# -*- coding:utf-8 _*-
"""
author: Miguitian
@time: 2022/11/02
@file: util.py
@description:
"""
import json
import os
import hashlib
from time import time
from functools import wraps
from logger import logger


def load_json_file(file_path: str) -> dict:
    with open(file_path, 'r', encoding='utf-8') as f:
        rule_model = json.load(f)

    return rule_model


def get_file_md5(file_path: str):
    if not os.path.exists(file_path):
        return ""

    with open(file_path, 'rb') as fp:
        data = fp.read()
    file_md5 = hashlib.md5(data).hexdigest()

    return file_md5


def _timer(action):
    def tmp_func(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            task_uuid = kwargs['task_uuid']
            logger.info(f"{task_uuid} {action} task started.")
            start_time = time()
            result = func(*args, **kwargs)
            end_time = time()
            run_time = end_time - start_time
            logger.info(
                f"{task_uuid} {action} task finished in {round(run_time, 3)} seconds.")
            return result

        return wrapper

    return tmp_func
