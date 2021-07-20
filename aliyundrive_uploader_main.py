#!/usr/bin/python3
# -*- coding: utf-8 -*-
# +-------------------------------------------------------------------
# | 阿里云盘上传工具宝塔插件
# +-------------------------------------------------------------------
# | Author: Pluto <i@abcyun.cc>
# +-------------------------------------------------------------------
import sys, os, json

# 设置运行目录
import time
from sqlite import sqlite

os.chdir("/www/server/panel")

# 添加包引用位置并引用公共包
sys.path.append("class/")
import public

import aliyundrive_uploader_common as common

# 在非命令行模式下引用面板缓存和session对象
if __name__ != '__main__':
    pass

class aliyundrive_uploader_main:
    __plugin_path = "/www/server/panel/plugin/aliyundrive_uploader/"
    __config = None
    __data_path = __plugin_path + "/drive/db.db"
    __config_path = __plugin_path + "/drive/config.json"

    # 构造方法
    def __init__(self):
        if not os.path.exists(self.__data_path):
            public.ExecShell('python3 %sdrive/aliyundrive_uploader_migrate.py' % self.__plugin_path)

    def index(self, args):
        return self.get_logs(args)

    def file(self, args):
        return '11s'

    def get_logs(self, args):
        # 处理前端传过来的参数
        if not 'p' in args: args.p = 1
        if not 'rows' in args: args.rows = 100
        if not 'callback' in args: args.callback = ''
        args.p = int(args.p)
        args.rows = int(args.rows)

        # 取日志总行数
        db = self.__get_db()
        count = db.table('task_log').count()

        # 获取分页数据
        page_data = public.get_page(count, args.p, args.rows, args.callback)

        # 获取当前页的数据列表
        log_list = db.table('task_log').order('id desc').limit(page_data['shift'] + ',' + page_data['row']).select()

        # 返回数据到前端
        return {'data': log_list, 'page': page_data['page']}

    def get_task(self, args):

        # 处理前端传过来的参数
        if not 'p' in args: args.p = 1
        if not 'rows' in args: args.rows = 10
        if not 'callback' in args: args.callback = ''
        args.p = int(args.p)
        args.rows = int(args.rows)

        # 取日志总行数
        db = self.__get_db()
        count = db.table('task').where('status=? or status=?', (2, 0)).count()

        # 获取分页数据
        page_data = public.get_page(count, args.p, args.rows, args.callback)

        # 获取当前页的数据列表
        log_list = db.table('task') \
            .where('status=? or status=?', (2, 0)) \
            .order('create_time asc').limit(page_data['shift'] + ',' + page_data['row']).select()

        # 返回数据到前端
        return {'data': log_list, 'page': page_data['page']}

    def get_completed_tasks(self, args):

        # 处理前端传过来的参数
        if not 'p' in args: args.p = 1
        if not 'rows' in args: args.rows = 10
        if not 'callback' in args: args.callback = ''
        args.p = int(args.p)
        args.rows = int(args.rows)

        # 取日志总行数
        db = self.__get_db()
        count = db.table('task').where('status=? or status=?', (1, -1)).count()

        # 获取分页数据
        page_data = public.get_page(count, args.p, args.rows, args.callback)

        # 获取当前页的数据列表
        log_list = db.table('task') \
            .where('status=? or status=?', (1, -1)) \
            .order('finish_time desc').limit(page_data['shift'] + ',' + page_data['row']).select()

        # 返回数据到前端
        return {'data': log_list, 'page': page_data['page']}

    def get_task_log(self, args):
        # 验证前端输入
        if not hasattr(args, 'id') and args.id:
            return public.returnMsg(False, '必要信息不能为空，请核实!')

        db = self.__get_db()
        find = db.table('task_log').where('task_id=?', args.id).order('id asc').select()
        if find:
            return {
                'status': True,
                'msg': 'success',
                'data': find
            }
        return public.getJson(public.returnMsg(False, '没有该数据'))

    def get_config(self, args):
        return self.__get_config()

    def set_config(self, get):
        try:

            # 验证前端输入
            values = [
                get.REFRESH_TOKEN,
                get.DRIVE_ID,
                # get.ROOT_PATH,
                get.MULTITHREADING,
                get.MAX_WORKERS,
                get.CHUNK_SIZE,
                get.RESUME,
                get.OVERWRITE,
                get.RETRY,
                get.RESIDENT,
            ]

            for v in values:
                if not v:
                    return public.returnMsg(False, '必要信息不能为空，请核实!')

            if not get.ROOT_PATH:
                get.ROOT_PATH = "bt_upload"

            data = self.__get_config()
            for k in data.keys():
                if hasattr(get, k):
                    data[k] = getattr(get, k)
                    if k in ['MULTITHREADING', 'OVERWRITE', 'RESUME','RESIDENT']:
                        if data[k] in ['true', 1, True]:
                            data[k] = True
                        else:
                            data[k] = False

                        # 写入到配置文件
            public.WriteFile(self.__config_path, json.dumps(data))
            return public.returnMsg(True, '设置成功!')
        except Exception as e:
            pass
        return public.returnMsg(False, 'API资料校验失败，请核实!')

    def __get_db(self):
        db = sqlite()
        db.dbfile(self.__data_path)
        return db

    def create_upload_task(self, args):
        # 验证前端输入
        if not hasattr(args, 'realpath') and args.realpath:
            return public.returnMsg(False, '必要信息不能为空，请核实!')

        if os.path.isdir(args.realpath):
            # 获取所有文件的相对路径
            relative_path_list = common.get_all_file_relative(args.realpath)
            # 给所有文件添加当前目录路径
            relative_path_list = list(map(lambda x: os.path.basename(args.realpath) + os.sep + x, relative_path_list))
            # 去除父目录中的当前目录路径
            parent_path = common.qualify_path(os.path.dirname(args.realpath))
        else:
            relative_path_list = [
                os.path.basename(args.realpath)
            ]
            parent_path = common.qualify_path(os.path.dirname(args.realpath))

        for path in relative_path_list:
            data = {
                'filepath': path,
                'realpath': parent_path + path,
                'filesize': os.path.getsize(args.realpath),
                'status': 0,
                'create_time': int(time.time()),
                'finish_time': 0,
                'spend_time': 0,
            }
            db = self.__get_db()
            db.table('task').insert(data)
        return public.returnMsg(True, '提交成功')

    def get_sever_status(self, args):
        if self.__get_server_status():
            return public.getJson(public.returnMsg(True, "阿里云盘上传服务运行正常"))

        return public.getJson(public.returnMsg(False, "阿里云盘上传服务已停止"))

    def set_server_status(self, args):
        if args.type == 'start':
            public_exec_shell = self.__server_start()
            if self.__get_server_status():
                return public.getJson(public.returnMsg(True, '阿里云盘上传服务启动成功'))
            else:
                return public.getJson(public.returnMsg(False, public_exec_shell[1]))
        elif args.type == 'stop':
            self.__server_stop()
            return public.getJson(public.returnMsg(True, '阿里云盘上传服务停止成功'))
        elif args.type == 'restart':
            self.__server_stop()
            public_exec_shell = self.__server_start()
            if self.__get_server_status():
                return public.getJson(public.returnMsg(True, '阿里云盘上传服务重启成功'))
            else:
                return public.getJson(public.returnMsg(False, public_exec_shell[1]))
        else:
            return self.get_sever_status(args)

    def clear_task(self, args):
        db = self.__get_db()
        if args.type == 'all':
            delete = db.table('task').where('1=?', (1,)).delete()
            if type(delete) == int:
                return public.getJson(public.returnMsg(True, '阿里云盘任务队列全部清理成功'))
            else:
                return public.getJson(public.returnMsg(False, '阿里云盘任务队列清理失败：' + delete))
        elif args.type == 'completed':
            delete = db.table('task').where('status=?', (1,)).delete()
            if type(delete) == int:
                return public.getJson(public.returnMsg(True, '阿里云盘已上传任务队列清理成功'))
            else:
                return public.getJson(public.returnMsg(False, '阿里云盘已上传任务队列清理失败：' + delete))
        elif args.type == 'failure':
            delete = db.table('task').where('status=?', (-1,)).delete()
            if type(delete) == int:
                return public.getJson(public.returnMsg(True, '阿里云盘已上传任务队列清理成功'))
            else:
                return public.getJson(public.returnMsg(False, '阿里云盘已上传任务队列清理失败：' + delete))
        elif args.type == 'log':
            delete = db.table('task_log').where('1=?', (1,)).delete()
            if type(delete) == int:
                return public.getJson(public.returnMsg(True, '阿里云盘日志清理成功'))
            else:
                return public.getJson(public.returnMsg(False, '阿里云盘日志清理失败：' + delete))
        else:
            return public.getJson(public.returnMsg(False, '请传入正确的type'))

    def __get_server_status(self):
        if public.process_exists('python3', None, '%sdrive/main.py' % self.__plugin_path):
            return True
        else:
            return False

    def __get_server_pid(self, pname, exe=None, cmdline=None):
        try:
            import psutil
            pids = psutil.pids()
            for pid in pids:
                try:
                    p = psutil.Process(pid)
                    if p.name() == pname:
                        if not exe and not cmdline:
                            return pid
                        else:
                            if exe:
                                if p.exe() == exe: return pid
                            if cmdline:
                                if cmdline in p.cmdline(): return pid
                except:
                    pass
            return False
        except:
            return True

    def __server_start(self):
        if self.__get_server_status():
            return True
        return public.ExecShell('nohup python3 %sdrive/main.py >/dev/null 2>error.log  2>&1 &' % self.__plugin_path)

    def __server_stop(self):
        if not self.__get_server_status():
            return True
        while True:
            server_pid = self.__get_server_pid('python3', None, '%sdrive/main.py' % self.__plugin_path)
            if server_pid:
                public.ExecShell("kill -9 %d" % server_pid)
            else:
                break

        return True

    # 读取配置项(插件自身的配置文件)
    # @param key 取指定配置项，若不传则取所有配置[可选]
    # @param force 强制从文件重新读取配置项[可选]
    def __get_config(self, key=None, force=False):
        # 判断是否从文件读取配置
        if not self.__config or force:
            if not os.path.exists(self.__config_path): return None
            f_body = public.ReadFile(self.__config_path)
            if not f_body: return None
            self.__config = json.loads(f_body)

        # 取指定配置项
        if key:
            if key in self.__config: return self.__config[key]
            return None
        return self.__config

    # 设置配置项(插件自身的配置文件)
    # @param key 要被修改或添加的配置项[可选]
    # @param value 配置值[可选]
    def __set_config(self, key=None, value=None):
        # 是否需要初始化配置项
        if not self.__config: self.__config = {}

        # 是否需要设置配置值
        if key:
            self.__config[key] = value

        # 写入到配置文件
        public.WriteFile(self.__config_path, json.dumps(self.__config))
        return True
