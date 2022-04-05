#!/usr/bin/env bash

set -e

hash tar uname grep curl head

#配置插件安装目录
install_path=/www/server/panel/plugin/alidrive
panel_path=/www/server/panel

OS="$(uname)"
case $OS in
  Linux)
    OS='linux'
    ;;
  Darwin)
    OS='darwin'
    ;;
  *)
    echo 'OS not supported'
    exit 2
    ;;
esac

ARCH="$(uname -m)"
case $ARCH in
  x86_64|amd64)
    ARCH='amd64'
    ;;
  aarch64)
    ARCH='arm64'
    ;;
  i?86|x86)
    ARCH='386'
    ;;
  arm*)
    ARCH='arm'
    ;;
  *)
    echo 'OS type not supported'
    exit 2
    ;;
esac
#安装
Install()
{
	Uninstall
	rm -rf $panel_path/BTPanel/static/img/soft_ico/ico-alidrive.png
	rm -rf $install_path
	echo '正在安装阿里云盘上传工具...'
	#==================================================================
	#依赖安装开始
	echo '下载插件中'
  DOWNLOAD_URL=$(curl -fsSL https://api.github.com/repos/aoaostar/alidrive-uploader-for-baota/releases/latest | grep "tarball_url.*" | cut -d '"' -f 4)
  curl -L "$DOWNLOAD_URL" | tar -xz
  mv `ls | grep "alidrive-uploader-for-baota"` $install_path
	echo '下载上传驱动中'
  CORE_DOWNLOAD_URL=$(curl -fsSL https://api.github.com/repos/aoaostar/alidrive-uploader/releases/latest | grep "browser_download_url.*$OS.*$ARCH" | cut -d '"' -f 4)
  curl -L "$CORE_DOWNLOAD_URL" | tar -xz
  mv `ls | grep "alidrive_uploader"` $install_path/core
	cp $install_path/icon.png $panel_path/BTPanel/static/img/soft_ico/ico-alidrive.png
	cp $install_path/core/example.config.yaml $install_path/core/config.yaml
	#依赖安装结束
	#==================================================================
	echo '================================================'
	echo '阿里云盘上传工具安装完成'
}
# 更新
Update()
{
	rm -rf $install_path\_temp
	mkdir -p $install_path\_temp/core
	cp $install_path/core/config.yaml $install_path\_temp/core/config.yaml
	Uninstall
	echo '正在更新阿里云盘上传工具...'
	#==================================================================
	#依赖安装开始
	echo '更新插件中'
  DOWNLOAD_URL=$(curl -fsSL https://api.github.com/repos/aoaostar/alidrive-uploader-for-baota/releases/latest | grep "tarball_url.*" | cut -d '"' -f 4)
  curl -L "$DOWNLOAD_URL" | tar -xz
  mv `ls | grep "alidrive-uploader-for-baota"` $install_path
	echo '更新插件上传驱动中'
  CORE_DOWNLOAD_URL=$(curl -fsSL https://api.github.com/repos/aoaostar/alidrive-uploader/releases/latest | grep "browser_download_url.*$OS.*$ARCH" | cut -d '"' -f 4)
  curl -L "$CORE_DOWNLOAD_URL" | tar -xz
  mv `ls | grep "alidrive_uploader"` $install_path/core
  chmod 755 $install_path/core/alidrive
	cp $install_path/icon.png $panel_path/BTPanel/static/img/soft_ico/ico-alidrive.png
	mv $install_path\_temp/core/config.yaml $install_path/core/config.yaml
	rm -rf $install_path\_temp
	#依赖安装结束
	#==================================================================
	echo '================================================'
	echo '阿里云盘上传工具更新完成！请重启插件！'
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
