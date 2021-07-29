#!/bin/bash
PATH=/bin:/sbin:/usr/bin:/usr/sbin:/usr/local/bin:/usr/local/sbin:~/bin
export PATH

#配置插件安装目录
install_path=/www/server/panel/plugin/aliyundrive_uploader
panel_path=/www/server/panel
#安装
Install()
{
	Uninstall
	rm -rf $panel_path/BTPanel/static/img/soft_ico/ico-aliyundrive_uploader.png
	rm -rf $install_path/drive/config.json
	echo '正在安装阿里云盘上传工具...'
	#==================================================================
	#依赖安装开始
	echo '下载插件中'
	git clone https://github.com/aoaostar/aliyundrive_uploader_for_baota.git $install_path
	echo '下载上传驱动中'
	git clone https://github.com/Hidove/aliyundrive-uploader.git $install_path/drive
	$panel_path/pyenv/bin/pip install -r $install_path/drive/requirements.txt
	$panel_path/pyenv/bin/python $install_path/aliyundrive_uploader_migrate.py
	cp $install_path/icon.png $panel_path/BTPanel/static/img/soft_ico/ico-aliyundrive_uploader.png
	cp $install_path/drive/example.config.json $install_path/drive/config.json
	#依赖安装结束
	#==================================================================
	echo '================================================'
	echo '阿里云盘上传工具安装完成'
}
# 更新
Update()
{
	rm -rf $install_path\_temp
	mkdir -p $install_path\_temp/drive
	cp $install_path/drive/config.json $install_path\_temp/drive/config.json
	cp /www/server/panel/plugin/aliyundrive_uploader/drive/config.json /www/server/panel/plugin/aliyundrive_uploader\_temp/drive/config.json
	Uninstall
	echo '正在更新阿里云盘上传工具...'
	#==================================================================
	#依赖安装开始
	echo '更新插件中'
	git clone https://github.com/aoaostar/aliyundrive_uploader_for_baota.git $install_path
	echo '更新插件上传驱动中'
	git clone https://github.com/Hidove/aliyundrive-uploader.git $install_path/drive
	$panel_path/pyenv/bin/pip install -r $install_path/drive/requirements.txt
	$panel_path/pyenv/bin/python $install_path/aliyundrive_uploader_migrate.py
	cp $install_path/icon.png $panel_path/BTPanel/static/img/soft_ico/ico-aliyundrive_uploader.png
	mv $install_path\_temp/drive/config.json $install_path/drive/config.json
	rm -rf $install_path\_temp
	#依赖安装结束
	#==================================================================
	echo '================================================'
	echo '阿里云盘上传工具安装完成！请重启工具！'
}

#卸载
Uninstall()
{
	rm -rf $install_path
}

#操作判断
if [ "${1}" == 'install' ];then
	Install
elif [ "${1}" == 'uninstall' ];then
	Uninstall
elif [ "${1}" == 'update' ];then
	Update
else
	echo 'Error!';
fi
