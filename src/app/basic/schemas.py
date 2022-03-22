# -*- coding: utf-8 -*-
"""
    desc: fastapi涉及到的实体模型
    author: miguitian
    date: 2021-04-16
"""
from typing import Dict
from pydantic import BaseModel


class ABSBaseModel(BaseModel):
    """
    所有数据处理的基类.
    """
    code: int = 200
    info: str = "执行成功"
    runtime: str

    def jsonify(self) -> Dict:
        """
        [summary]

        Returns:
            Dict: [将对象序列化为词典]
        """

        pass


if __name__ == "__main__":
    pass
