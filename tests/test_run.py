#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    desc: 单元测试用例写法
    author:
    date:
"""
import sys
import os
from fastapi.testclient import TestClient
import sys
_project_root = os.path.dirname(
            os.path.realpath(__file__)
)
sys.path.append(_project_root)
from src.run import app

client = TestClient(app)  # 先pip install pytest


def test_ping():  # 函数名用“test_”开头是 pytest 的规范。注意不是async def
    response = client.get(url='/healthy')
    assert response.status_code == 200
    assert response.text == '"API正常启动"'
