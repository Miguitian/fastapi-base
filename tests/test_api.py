#!usr/bin/env python
# -*- coding:utf-8 _*-
"""
author: Miguitian
@time: 2022/10/31
@file: test_api.py
@description:
"""
import json
from multiprocessing.pool import ApplyResult
from unittest import mock
import pytest
from fastapi.testclient import TestClient
from app.api import APP
from app.schemas import TaskInfo

client = TestClient(APP)  # 先pip install pytest
TASK_UUID = "1234"


@pytest.fixture
def task_info() -> TaskInfo:
    task_info = {
        "taskUuid": TASK_UUID,
        "taskInfo": "测试数据"
    }
    task = TaskInfo(**task_info)
    return task


def test_ping():
    response = client.get(url='/version')
    assert response.status_code == 200


class TestTaskSync:
    def test_success_create_task(self, task_info):
        response = client.post('/api/task_sync',
                               content=task_info.json())
        assert response.status_code == 200
        ret_info = json.loads(response.content)
        assert ret_info.get("code") == 200

    def test_error_create_task(self, task_info):
        pass


class TestAsyncTaskCreate:
    def test_success(self, task_info):
        mock_apply_result = mock.Mock(spec=ApplyResult)
        mock_apply_result.ready.side_effect = [True]
        with mock.patch.dict('app.api.TASK_INFO',
                             {TASK_UUID: mock_apply_result}):
            response = client.post('/api/task',
                                   content=task_info.json())
            assert response.status_code == 200
            ret_info = json.loads(response.content)
            assert ret_info.get("code") == 200
            assert ret_info.get("taskStatus") == "SUCCESS"

    def test_create(self, task_info):
        with mock.patch.dict('app.api.TASK_INFO', {}):
            response = client.post('/api/task',
                                   content=task_info.json())
            assert response.status_code == 200
            ret_info = json.loads(response.content)
            assert ret_info.get("code") == 200
            assert ret_info.get("taskStatus") == "CREATE"
