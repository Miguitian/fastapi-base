#!usr/bin/env python
# -*- coding:utf-8 _*-
"""
author: Miguitian
@time: 2022/10/28
@file: config.py
@description:
"""
# pylint: disable=C0103, E0401, C0116, W0611
import traceback
import os
import json
import yaml

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

_PROJECT_ROOT = os.path.dirname(
    os.path.dirname(
        os.path.realpath(__file__)
    )
)

CONFIG_PATH = os.path.join(_PROJECT_ROOT, f"conf{os.sep}config.yml")


def get_configer(config_abs_path):
    """
    [获得配置文件]

    Arguments:
        config_abs_path {[type]} -- [description]
    """
    yml_config = {}
    with open(config_abs_path, "rb") as config_yml_file:
        try:
            yml_config = yaml.safe_load(config_yml_file)
            print(yml_config)
        except yaml.YAMLError as exc:
            print(exc)
            traceback.print_exc()
    return yml_config


class ClientConfiger:
    """
    [配置项管理器]
    """
    config_abs_path: str

    def __init__(self, _config_type, _config_abs_path):
        """[summary]

        Args:
            _config_abs_path ([string]): [文件的路径]

        Raises:
            FileNotFoundError: [_config_abs_path 找不到文件]
            FileExistsError: [_config_abs_path 不是文件]
        """
        self.config_type = _config_type
        if not os.path.exists(_config_abs_path):
            raise FileNotFoundError(_config_abs_path)
        if not os.path.isfile(_config_abs_path):
            raise FileExistsError()
        self.config_abs_path = _config_abs_path
        self.yaml_config = {}
        self.refresh_config()

    def refresh_config(self):
        try:
            with open(self.config_abs_path, "rb") as config_yml_file:
                yml_config = yaml.safe_load(config_yml_file)
                self.yaml_config = yml_config
        except yaml.YAMLError as exc:
            print(exc)
            traceback.print_exc()
        return self

    def get_config_value(self, config_key_name, default_value=None):
        return self.yaml_config[self.config_type].get(config_key_name,
                                                      default_value)

    def get_model_path(self, config_key_name):
        model_name = self.yaml_config[self.config_type].get(config_key_name)
        model_path = os.path.join(_PROJECT_ROOT, "model", model_name)
        return model_path

    def __repr__(self):
        return json.dumps(self.yaml_config, ensure_ascii=False, indent=4)


ServerConfig = ClientConfiger("server", CONFIG_PATH)
LogConfig = ClientConfiger("log", CONFIG_PATH)

if __name__ == "__main__":
    LogConfig = ClientConfiger("log", CONFIG_PATH)
