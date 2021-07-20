# -*- coding: utf-8 -*-
# +-------------------------------------------------------------------
# | 公共函数类
# +-------------------------------------------------------------------
# | Author: Pluto <i@abcyun.cc>
# +-------------------------------------------------------------------

import os


# 处理路径
def qualify_path(path):
    if not path:
        return ''
    return path.replace('/', os.sep).replace('\\\\', os.sep).rstrip(os.sep) + os.sep

# 获取指定路径下的所有文件的相对路径
def get_all_file_relative(path):
    result = []
    if not os.path.exists(path):
        return result
    get_dir = os.listdir(path)
    for i in get_dir:
        sub_dir = os.path.join(path, i)
        if os.path.isdir(sub_dir):
            all_file = get_all_file_relative(sub_dir)
            all_file = map(lambda x: i + os.sep + x, all_file)
            result.extend(all_file)
        else:
            result.append(i)
    return result
