## 说明
本项目为阿里云盘上传工具的宝塔插件   
可以将服务器内的文件快速上传到阿里云盘

## 演示图
![WNwyU1.png](https://z3.ax1x.com/2021/07/20/WNwyU1.png)
![WN0pan.png](https://z3.ax1x.com/2021/07/20/WN0pan.png)
![WN0Wiq.png](https://z3.ax1x.com/2021/07/20/WN0Wiq.png)

## 安装
### Centos7
```shell script
yum install -y wget && wget -O install.sh https://raw.githubusercontent.com/aoaostar/aliyundrive_uploader_for_baota/master/install.sh && sh install.sh install
```
### Debian
```shell script
wget -O install.sh https://raw.githubusercontent.com/aoaostar/aliyundrive_uploader_for_baota/master/install.sh && sh install.sh install
```
## 配置账号信息
![](https://z3.ax1x.com/2021/03/27/6zB8JA.png)

* 控制台快速获取代码
```javascript
var data = JSON.parse(localStorage.getItem('token'));
console.log(`refresh_token  =>  ${data.refresh_token}
default_drive_id  =>  ${data.default_drive_id}
`);
```
## 注意
使用宝塔插件需要将上传工具`config.json`里的`RESIDENT`值改成`true`，即启用常驻运行，以常驻运行