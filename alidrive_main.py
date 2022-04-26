#!/usr/bin/python
# -*- coding: utf-8 -*-
# +-------------------------------------------------------------------
# | Date: 2022/4/4
# +-------------------------------------------------------------------
# | Author: Pluto <i@aoaostar.com>
# +-------------------------------------------------------------------
import sys, os, json

# 设置运行目录

os.chdir("/www/server/panel")

# 添加包引用位置并引用公共包
sys.path.append("class/")
import public


class alidrive_main:
    __plugin_path = "/www/server/panel/plugin/alidrive/"
    __tasks_file = __plugin_path + "tasks.json"
    __config_file = __plugin_path + "core/config.yaml"
    __logs_file = __plugin_path + "core/logs/alidrive.log"
    __core_file = __plugin_path + "core/alidrive"
    __python = "/www/server/panel/pyenv/bin/python"
    __config = None
    __tasks = None

    # 构造方法
    def __init__(self):
        self.__tasks = self.__get_tasks()
        self.__config = self.__get_config()

    def index(self, args):
        from BTPanel import cache
        check_update = cache.get("check_update")
        if not check_update or len(check_update) < 4:
            check_update = self.check_update(args)
        cache.set("check_update", check_update, 3600)
        return check_update

    def check_update(self, args):
        from BTPanel import cache
        import requests
        cache.delete("check_update")
        file = public.readFile(self.__plugin_path + "info.json")
        loads = json.loads(file)
        exec_shell = public.ExecShell(f"chmod 755 {self.__core_file} && {self.__core_file} -v")
        get = requests.get("https://api.github.com/repos/aoaostar/alidrive-uploader-for-baota/releases/latest")
        plugin_json = get.json()
        get = requests.get("https://api.github.com/repos/aoaostar/alidrive-uploader/releases/latest")
        core_json = get.json()
        return {
            "version": loads["versions"],
            "core_version": exec_shell[0],
            "lastest_version": plugin_json["tag_name"],
            "lastest_core_version": core_json["tag_name"],
        }

    def update(self, args):
        shell = public.ExecShell(
            f"chmod 755 {self.__plugin_path}install.sh && bash {self.__plugin_path}install.sh update -y")

        if not shell[0] == "":
            return public.returnMsg(True, shell[0])
        return public.returnMsg(False, shell[1])

    def add_task(self, args):
        if "filepath" not in args:
            return public.returnMsg(False, "请传入文件路径")
        if not os.path.exists(args.filepath):
            return public.returnMsg(False, "文件不存在")
        import uuid
        self.__tasks[str(uuid.uuid1())] = args.filepath
        self.__save_tasks()
        return public.returnMsg(True, "添加成功")

    def get_tasks(self, args):
        return self.__tasks

    def delete_task(self, args):
        if "id" not in args:
            return public.returnMsg(False, "请传入任务id")
        if args.id in self.__tasks:
            del self.__tasks[args.id]
        self.__save_tasks()
        return public.returnMsg(True, "删除成功")

    def get_config(self, args):
        return self.__config

    def save_config(self, args):

        if "data" not in args:
            return public.returnMsg(False, "请传入配置文件内容")
        self.__config = args.data
        self.__save_config()
        return public.returnMsg(True, "保存成功")

    def get_logs(self, args):
        f_body = ""
        if os.path.exists(self.__logs_file):
            f_body = public.readFile(self.__logs_file)
        return f_body

    def clear_logs(self, args):
        public.writeFile(self.__logs_file, "")
        return public.returnMsg(True, "清除成功")

    def server_status(self, args):
        from alidrive_server import alidrive_server
        server = alidrive_server()
        return {
            "status": server.server_status(),
            "core_status": server.alidrive_status(),
        }

    def server_start(self, args):
        exec_shell = public.ExecShell(
            f"nohup {self.__python} {self.__plugin_path}alidrive_server.py >/dev/null 2>error.log  2>&1 &")
        if exec_shell[1] == "":
            return public.returnMsg(True, "启动成功")
        return public.returnMsg(False, exec_shell[1])

    def server_stop(self, args):
        from alidrive_server import alidrive_server
        server = alidrive_server()
        stop = server.server_stop()
        if stop[0]:
            return public.returnMsg(True, "停止成功")
        return public.returnMsg(stop[0], stop[1])

    def server_restart(self, args):
        from alidrive_server import alidrive_server
        server = alidrive_server()
        stop = server.server_stop()
        if stop[0]:
            start = public.ExecShell(
                f"nohup {self.__python} {self.__plugin_path}alidrive_server.py >/dev/null 2>error.log  2>&1 &")
            if start[1] == "":
                return public.returnMsg(True, "重启成功")
            else:
                return public.returnMsg(start[0], start[1])
        else:
            return public.returnMsg(stop[0], stop[1])

    def __get_config(self):
        # 判断是否从文件读取配置
        f_body = ""
        if os.path.exists(self.__config_file):
            f_body = public.ReadFile(self.__config_file)
        return f_body

    def __save_config(self):
        public.WriteFile(self.__config_file, self.__config)
        return True

    def __get_tasks(self):
        tasks = {}
        if os.path.exists(self.__tasks_file):
            file = public.readFile(self.__tasks_file)
            tasks = json.loads(file)
        if not isinstance(tasks, dict):
            tasks = {}

        return tasks

    def __save_tasks(self):
        public.writeFile(self.__tasks_file, json.dumps(self.__tasks))
