#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    desc: fastapi的启动文件 TODO：可以逐步设置路由相关
    author: miguitian
    date: 2021-12-23
"""

import uvicorn
import time
import os
import traceback
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import File, UploadFile
from app.log.logger import logger
from app.basic.schemas import ABSBaseModel

app = FastAPI()

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/ping")
def ping():
    return "API正常启动"


@app.post("/upload_file")
async def upload_file(file: UploadFile = File(...)):
    """
        上传一个文件，进行读取保存
        TODO：进行类型的判断，比如说zip、pdf、excel等，如有可能在上传时应该进行限制
        Args:
            file: 上传的文件，类型未知

    Returns:

    """
    try:
        start_time = time.time()
        logger.info(f"{file.filename} task start ...")
        file_content = await file.read()
        file_save_path = os.path.join('../../data', file.filename)
        with open(file_save_path, 'wb') as f:
            f.write(file_content)

        return ABSBaseModel(runtime=f'{time.time() - start_time}s')
    except Exception as f:
        traceback.print_exc()
        return ABSBaseModel(code=400, info=f'{repr(f)}',
                            runtime=f'{time.time() - start_time}')


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
