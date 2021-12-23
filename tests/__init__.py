#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    desc: init文件,用于定位PROJECT_ROOT, 单元测试用例文件包
    author: miguitian
    date: 2021-12-23
"""
import os

_project_root = os.path.dirname(
    os.path.dirname(
        os.path.realpath(__file__)
    )
)