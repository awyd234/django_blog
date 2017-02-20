# -*- coding: utf-8 -*-

import configparser
import os

current_dir = os.path.dirname(__file__)
parent_dir = os.path.dirname(current_dir)
config_path = os.path.join(parent_dir, 'etc/config.ini')

config = configparser.ConfigParser(allow_no_value=True)
config.read(config_path)


def get_value(section, option, default=None):
    '''
    得到etc/config.ini里的值
    :param section: 内容模块
    :param option: 模块的键值
    :param default: 查找失败返回值
    :return:
    '''
    try:
        return format(config.get(section, option))
    except:
        return default
