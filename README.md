# fastapi-base
fastapi的基础脚手架，可以快速搭建起一个异步多进程工程性的api框架

## 开发时主要环境
`python：3.7.13` `FastApi: 0.87.0` `pytest: 6.2.5` `coverage: 7.2.3`
## 用法
### 前端swagger测试
```bash
http://127.0.0.1:8000/docs
```
## 部署方式
### 命令启动
##### 程序启动
```bash
python src/run.py
```
### docker启动
```bash
# 制作镜像
docker-compose build

# 启动
docker-compose up -d
```
## 注意
在首次开发时，需要用IDE软件将src目录设置为`Sources Root` 目录，否则在用IDE调试的时候会出现模型导入的错误