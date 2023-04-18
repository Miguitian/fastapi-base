#!usr/bin/env python
# -*- coding:utf-8 _*-
"""
author: Miguitian
@time: 2022/10/28
@file: schemas.py
@description: 数据结构
"""
# pylint: disable=R0903, C0115
from pydantic import BaseModel  # pylint: disable=E0611


class TaskStatus:
    """
    【任务处理状态】
    """
    CREATE = "CREATE"
    SUCCESS = "SUCCESS"
    RUNNING = "RUNNING"
    FAILURE = "FAILURE"
    UNKNOWN = "UNKNOWN"


class CreateTaskReturn(BaseModel):
    """
    [异步创建任务的返回信息]
    """
    taskUuid: str
    taskStatus: str = TaskStatus.CREATE
    code: int = 200
    success: bool = True
    message: str


class TaskInfo(BaseModel):
    """
    电子指令分类需要提交的信息
    """
    taskUuid: str
    taskInfo: str  # 实际项目中，该位置需要更改为项目定义的接口信息


class TaskReturnInfo(BaseModel):
    """
    电子指令分类返回的信息
    """
    taskUuid: str
    taskStatus: str = "SUCCESS"
    code: int = 200
    success: bool = True
    message: str = "成功"
    internalSeconds: float = 0.0
    result: str = ""
