#!usr/bin/env python
# -*- coding:utf-8 _*-
"""
author: Miguitian
@time: 2023/03/23
@file: run_task.py
@description: 任务处理主流程
"""
import time
import os
import traceback
from logger import logger
from .schemas import TaskReturnInfo, TaskStatus, TaskInfo


def run_task(task_info: TaskInfo) -> TaskReturnInfo:
    """
    系统主流程处理函数
    Args:
        task_info:

    Returns:

    """
    start_time = time.time()
    logger.info(f"{os.getpid()} is processing task: {task_info.taskUuid}")

    try:
        # 这里应该写上任务处理的主函数，并且更改schema格式进行返回，目前只是一个测试返回
        task_return = TaskReturnInfo(
            taskUuid=task_info.taskUuid,
            internalSeconds=f"{time.time() - start_time:.3f}",
            result=task_info.taskInfo
        )

        logger.info(
            f"{task_info.taskUuid} task finished in {round(time.time() - start_time, 3)} seconds.")

    except Exception as f:
        logger.error(traceback.format_exc())
        task_return = TaskReturnInfo(
            taskUuid=task_info.taskUuid,
            taskStatus=TaskStatus.FAILURE,
            message=str(repr(f)),
            code=400,
            success=False,
            internalSeconds=f"{time.time() - start_time:.3f}",
        )

        logger.error(f"{task_info.taskUuid}  {task_return.dict()}")
        logger.error(
            f"{task_info.taskUuid} Task terminated due to an error during execution.")

    return task_return


if __name__ == '__main__':
    pass
