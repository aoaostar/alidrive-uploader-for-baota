var alidrive_message = {
    instance: 0,
    loading: function (message) {
        this.instance = layer.msg(message, {
            icon: 16,
            shade: 0.4,
            time: 0,
        });
        return this.instance
    },
    success: function (message) {
        this.instance = layer.msg(message, {
            icon: 1
        });
        return this.instance
    },
    error: function (message) {
        this.instance = layer.msg(message, {
            icon: 2
        });
        return this.instance
    },
    close: function (instance) {
        if (instance) {
            layer.close(instance)
        } else {
            layer.close(this.instance)
        }
    }
}

var alidrive_view_files = {
    page: 1,
    index: function () {
        show('p-files')
        this.get_dir()
    },
    get_dir: function (p, path) {

        if (p === undefined) p = 1;
        if (path === undefined) {
            path = getCookie('Path');
        }
        setCookie('Path', path);
        this.page = p
        request_post('/files?action=GetDir', {
            p: p,
            showRow: 100,
            path: path,
        }).then(res => {
            //href='p=2'
            $("#p-file-page").html(res.PAGE.replace(/href='p=(\d+)'/g, `onclick="view_files.get_dir($1,'${res.PATH}')"`))
            let path_split = res.PATH.split('/');
            let tmp_path = `<li><a title="/" onclick="alidrive_view_files.get_dir(1,'/')">根目录</a></li>`

            for (let i = 0; i < path_split.length; i++) {
                if (path_split[i] === "") {
                    continue
                }
                let full_path = path_split.slice(0, i + 1).join('/')
                tmp_path += `<li><a title="${path_split[i]}" onclick="alidrive_view_files.get_dir(1,'${full_path}')">${path_split[i]}</a></li>`
            }
            $('#p-files-path').html(tmp_path)

            let tmp = ''
            for (const d of res.DIR) {
                const fileinfo = d.split(';');
                const realpath = res.PATH + '/' + fileinfo[0];
                tmp += `<tr>
                            <td class="cursor" onclick="alidrive_view_files.get_dir(1,'${realpath}')">
                                <span class="ico ico-folder"></span><span>${fileinfo[0]}</span>
                            </td>
                            <td>${ToSize(fileinfo[1])}</td>
                            <td>${getLocalTime(fileinfo[2])}</td>
                            <td class="text-right">
                                <a class="btlink" onclick="alidrive.add_task('${realpath}')">上传</a>
                            </td>
                        </tr>`
            }
            for (const d of res.FILES) {
                const fileinfo = d.split(';');
                const realpath = res.PATH + '/' + fileinfo[0];
                tmp += `<tr>
                            <td class="cursor">
                                <span class="ico ico-file"></span><span>${fileinfo[0]}</span>
                            </td>
                            <td>${ToSize(fileinfo[1])}</td>
                            <td>${getLocalTime(fileinfo[2])}</td>
                            <td class="text-right">
                                <a class="btlink" onclick="alidrive.add_task('${realpath}')">上传</a>
                            </td>
                        </tr>`
            }
            $('#p-files-list').html(tmp)
        })
    },
    back: function () {
        let path = getCookie('Path');
        this.get_dir(1, path.slice(0, path.lastIndexOf('/') + 1))
    }
}
var alidrive = {
    update: function () {
        const loading = alidrive_message.loading('正在更新中');
        request_plugin("alidrive", 'update', {}, 0).then(res => {
            if (res.status) {
                alidrive_message.success("更新成功")
            } else {
                alidrive_message.error(res.msg)
            }
        }).finally(() => {
            alidrive_message.close(loading)
        })
    },
    check_update: function (type = "check_update") {
        const loading = alidrive_message.loading('正在检查更新中');
        request_plugin("alidrive", type).then(res => {
            let tmp = `<tr>
                            <th>插件版本</th>
                            <td>${res.version}</td>
                            <th>Core 版本</th>
                            <td>${res.core_version}</td>
                        </tr>
                        <tr>
                            <th>最新插件版本</th>
                            <td>${res.lastest_version}</td>
                            <th>最新 Core 版本</th>
                            <td>${res.lastest_core_version}</td>
                        </tr>
                        <tr>
                            <th>作者</th>
                            <td>Pluto</td>
                            <th>Github</th>
                            <td><a href="https://github.com/aoaostar" target="_blank">https://github.com/aoaostar</a></td>
                        </tr>`
            $('#p-index-content').html(tmp)
        }).finally(() => {
            alidrive_message.close(loading)
        })
    },
    get_index: function () {
        show("p-index")
        this.check_update("index")
        alidrive_server.status()
    },
    get_config: function () {
        show("p-config")
        request_plugin("alidrive", "get_config").then(res => {
            $('#p-config-content').text(res)
        })
    },
    save_config: function () {
        const loading = alidrive_message.loading('提交中');
        request_plugin("alidrive", "save_config", {
            data: $('#p-config-content').text()
        }).then(res => {
            layer.msg(res.msg, {icon: res.status ? 1 : 2});
        }).finally(() => {
            alidrive_message.close(loading)
        })
    },
    get_tasks: function () {
        show('p-task')
        request_plugin("alidrive", "get_tasks").then(res => {
            let tmp = ''
            for (const k in res) {
                tmp += `<tr>
                                <td><input data-id="${k}" type="checkbox"></td>
                                <td>
                                    <div class="titlename c3">${k}</div>
                                </td>
                                <td>
                                    <div class="titlename c3">${res[k]}</div>
                                </td>
                            </tr>`
            }
            $('#p-task-content').html(tmp)
            $('#p-task-count').text(`共${Object.keys(res).length}条`)
        })
    },
    add_task: function (filepath) {
        const loading = alidrive_message.loading('提交中');
        request_plugin("alidrive", "add_task", {
            filepath: filepath
        }).then(res => {
            layer.msg(res.msg, {icon: res.status ? 1 : 2});
        }).finally(() => {
            alidrive_message.close(loading)
        })
    },
    delete_task: function (id) {
        const loading = alidrive_message.loading('提交中');
        return request_plugin("alidrive", "delete_task", {
            id: id
        }).finally(() => {
            alidrive_message.close(loading)
        })
    },
    get_logs: function () {
        show("p-log")
        request_plugin("alidrive", "get_logs").then(res => {
            let $p = $('#p-log-content');
            $p.text(res)
            $p.scrollTop($p.prop("scrollHeight"))
        })
    },
    clear_logs: function () {
        request_plugin("alidrive", "clear_logs").then(res => {
            layer.msg(res.msg, {icon: res.status ? 1 : 2});
            this.get_logs()
        })
    },
}

var alidrive_server = {
    status: function () {
        const loading = alidrive_message.loading('正在获取系统状态');
        request_plugin("alidrive", "server_status").then(res => {
            $('#p-index .status').hide()
            let status_change = $('#p-index .status-change');
            status_change.hide()
            if (res.status) {
                $(status_change[1]).show()
                $('#p-index .plugin-status .status.ok').show()
            } else {
                $(status_change[0]).show()
                $('#p-index .plugin-status .status.no').show()
            }
            if (res.core_status) {
                $('#p-index .core-status .status.ok').show()
            } else {
                $('#p-index .core-status .status.no').show()
            }
        }).finally(() => {
            alidrive_message.close(loading)
        })
    },
    start: function () {
        const loading = alidrive_message.loading('正在发送启动命令');
        request_plugin("alidrive", "server_start").then(res => {
            if (res.status) {
                alidrive_message.success("启动成功")
            } else {
                alidrive_message.error(res.message)
            }
        }).finally(() => {
            alidrive_message.close(loading)
            setTimeout(() => {
                this.status()
            }, 2000)
        })
    },
    stop: function () {
        const loading = alidrive_message.loading('正在发送停止命令');
        request_plugin("alidrive", "server_stop").then(res => {
            if (res.status) {
                alidrive_message.success("停止成功")
            } else {
                alidrive_message.error(res.message)
            }
        }).finally(() => {
            alidrive_message.close(loading)
            setTimeout(() => {
                this.status()
            }, 2000)
        })
    },
    restart: function () {
        const loading = alidrive_message.loading('正在发送重启命令');
        request_plugin("alidrive", "server_restart").then(res => {
            if (res.status) {
                alidrive_message.success("重启成功")
            } else {
                alidrive_message.error(res.message)
            }
        }).finally(() => {
            alidrive_message.close(loading)
            setTimeout(() => {
                this.status()
            }, 2000)
        })
    },
}

function request_plugin(plugin_name, function_name, args, timeout) {
    return new Promise((resolve, reject) => {
        $.ajax({
            type: 'POST',
            url: '/plugin?action=a&s=' + function_name + '&name=' + plugin_name,
            data: args,
            timeout: timeout,
            success: function (rdata) {
                resolve(rdata)
            },
            error: function (e) {
                alidrive_message.error("请求异常" + e)
                reject(e)
            }
        })
    })
}

function request_post(url, args, callback, timeout) {
    if (!timeout) timeout = 3600;
    return new Promise((resolve, reject) => {
        $.ajax({
            type: 'POST',
            url: url,
            data: args,
            timeout: timeout,
            dataType: 'json',
            success: function (rdata) {
                resolve(rdata)
            },
            error: function (e) {
                alidrive_message.error("请求异常" + e)
                reject(e)
            }
        })
    })
}