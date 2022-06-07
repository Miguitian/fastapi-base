#!usr/bin/env python
# -*- coding:utf-8 _*-
"""
author: Miguitian
@time: 2022/06/08
@file: CheckCodeStyle.py
@description:
"""
import os
import sys
import pathlib
from pylint.lint import Run

_project_root = str(pathlib.Path(__file__).resolve().parents[1])
sys.path.append(_project_root)

MIN_SCORE = 9.0
# 由于pylint在多进程下得分和单进程不一致，暂时强制单进程
_CPU_COUNT = 1
CHECK_DIR = os.path.join(_project_root, 'src')


def lint_files(files):
    files.sort()
    for i, file_ in enumerate(files):
        print(i, file_)
    options = [f'--jobs={_CPU_COUNT}']
    results = Run(files+options, exit=False)
    score = results.linter.stats.global_note
    return score

def get_files(check_dir: str):
    exclude_dir = ['__pycache__']
    file_list = []

    for root, _, files in os.walk(check_dir):
        dirs_list = root.split('/')
        first_sub_dir = dirs_list[1] if len(dirs_list) > 1 else ''
        if (first_sub_dir in exclude_dir) or first_sub_dir.startswith('.'):
            continue

        for file in files:
            full_path = os.path.join(root, file)
            extension = os.path.splitext(full_path)[1]
            if extension == '.py':
                file_list.append(full_path)

    return file_list


def main():
    file_list = get_files(CHECK_DIR)
    score = lint_files(file_list)
    print(f"项目的pylint得分为: {score:3.2f}")
    if score < MIN_SCORE:
        # raise Exception('pylint分数太低啦，需要高于%3.2f哦' % MIN_SCORE)
        print('pylint分数太低啦，需要高于%3.2f哦' % MIN_SCORE)
    else:
        print(f"代码风格检测通过 分数为: {score:3.2f}")


if __name__ == '__main__':
    main()