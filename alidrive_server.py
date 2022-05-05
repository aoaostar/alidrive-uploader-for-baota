#!/usr/bin/python
# -*- coding: utf-8 -*-
# +-------------------------------------------------------------------
# | Date: 2022/4/4
# +-------------------------------------------------------------------
# | Author: Pluto <i@aoaostar.com>
# +-------------------------------------------------------------------
import json
import os
import sys

os.chdir("/www/server/panel")

# 添加包引用位置并引用公共包
sys.path.append("class/")
import public
import time


class alidrive_server:
    __plugin_path = "/www/server/panel/plugin/alidrive/"
    __tasks_file = __plugin_path + "tasks.json"
    __core_file = __plugin_path + "core/alidrive"
    __logs_file = __plugin_path + "core/logs/alidrive.log"

    def __init__(self):
        pass

    def alidrive_status(self):
        exec_shell = public.ExecShell("ps -ef | grep alidrive | grep -v python | grep -v grep | wc -l")
        if exec_shell[1] == "" and int(exec_shell[0]) > 0:
            return True
        return False

    def server_status(self):
        exec_shell = public.ExecShell("ps -ef | grep alidrive_server.py | grep -v grep | wc -l")
        if exec_shell[1] == "" and int(exec_shell[0]) > 0:
            return True
        return False

    def server_start(self):

        while True:
            if self.server_status():
                if os.path.exists(self.__tasks_file):
                    task_file = public.readFile(self.__tasks_file)
                    tasks = json.loads(task_file)
                else:
                    tasks = {}
                now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                try:
                    task = tasks.pop(list(tasks.keys())[0])
                    command = f"chmod 755 {self.__core_file} && {self.__core_file} {task} /"
                    exec_shell = public.ExecShell(command)
                    log = f"[插件日志][{now}] {command}\n"
                    log += f"[插件日志][{now}] resp-length={len(exec_shell[0])},error={exec_shell[1]}\n"
                    public.writeFile(self.__tasks_file, json.dumps(tasks))
                    public.writeFile(self.__logs_file, log, "a")
                except Exception as e:
                    pass
            time.sleep(1)

    def server_stop(self):
        public.ExecShell("ps -ef | grep alidrive_server.py | grep -v 'grep' | cut -c 9-15 | xargs kill -9")
        public.ExecShell("ps -ef | grep alidrive | grep -v python | grep -v 'grep' | cut -c 9-15 | xargs kill -9")
        return True, ""


if __name__ == '__main__':
    server = alidrive_server()
    if len(sys.argv) > 2 and sys.argv[1] == "stop":
        server.server_stop()
    else:
        server.server_start()
