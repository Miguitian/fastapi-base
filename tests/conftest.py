#!usr/bin/env python
# -*- coding:utf-8 _*-
"""
author: Miguitian
@time: 2023/04/10
@file: conftest.py
@description:
"""
import os
import sys
import pathlib

_project_root = str(pathlib.Path(__file__).resolve().parents[1])
sys.path.append(os.path.join(_project_root, 'src'))
