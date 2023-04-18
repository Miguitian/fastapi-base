#!usr/bin/env python
# -*- coding:utf-8 _*-
"""
author: Miguitian
@time: 2022/10/28
@file: api.py
@description:
"""
# pylint: disable=C0103, E0401, C0116
import os
import multiprocessing
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from logger import logger
from config import ServerConfig
from .run_task import run_task
from .schemas import TaskInfo, TaskReturnInfo, CreateTaskReturn, TaskStatus

TASK_NUM = ServerConfig.get_config_value("task_num", default_value=1)
if not os.getenv("WINDOWS"):  # 在windows环境下，多进程无法启动
    POOL = multiprocessing.Pool(processes=TASK_NUM, maxtasksperchild=30)
TASK_INFO = {}

APP = FastAPI()

origins = [
    "*",
]

APP.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@APP.get("/version")
def ping():
    system_version = "v1.0.0.20230420_Release"
    return system_version


@APP.post("/api/task_sync", response_model=TaskReturnInfo)
def create_task(task_info: TaskInfo):
    return run_task(task_info)


@APP.post("/api/task", response_model=CreateTaskReturn)
def async_task_create(task_info: TaskInfo):
    logger.info(f"Creating task: {task_info.taskUuid}")

    if TASK_INFO.get(task_info.taskUuid):
        if TASK_INFO[task_info.taskUuid].ready():
            logger.info(f"{task_info.taskUuid} Task has been completed.")
            result = CreateTaskReturn(
                taskUuid=task_info.taskUuid,
                taskStatus=TaskStatus.SUCCESS,
                message="任务已经执行完毕",
            )
        else:
            logger.info(
                f"{task_info.taskUuid} Task is already in progress.")
            result = CreateTaskReturn(
                taskUuid=task_info.taskUuid,
                taskStatus=TaskStatus.RUNNING,
                message="任务已经在处理中",
            )
    else:
        result = POOL.apply_async(run_task, args=(task_info,))
        TASK_INFO[task_info.taskUuid] = result
        logger.info(f"{task_info.taskUuid} Task created successfully.")

        result = CreateTaskReturn(
            taskUuid=task_info.taskUuid,
            taskStatus=TaskStatus.CREATE,
            message="任务创建成功",
        )

    return result


@APP.get("/api/task/{task_uuid}", response_model=TaskReturnInfo)
def async_get_task_results(task_uuid: str):
    logger.info(f"{task_uuid} Fetching task results.")

    if not TASK_INFO.get(task_uuid):
        logger.info(f"{task_uuid} Task creation did not occur.")
        result = TaskReturnInfo(
            taskUuid=task_uuid,
            taskStatus=TaskStatus.UNKNOWN,
            code=400,
            success=False,
            message="任务没有创建",
        )
        return result

    if TASK_INFO[task_uuid].ready():
        result = TASK_INFO.pop(task_uuid).get()
        logger.info(f'{task_uuid} Successfully fetched task results.')
    else:
        logger.info(f"{task_uuid} Task is currently being processed.")
        result = TaskReturnInfo(
            taskUuid=task_uuid,
            taskStatus=TaskStatus.RUNNING,
            code=200,
            success=False,
            message="任务正在执行中",
        )

    return result
