# 校园违规管理系统

## 1、相关支持

- flask（需安装）
- xlutils（需安装）
- os
- time

## 2、使用方法

使用cmd进入app.py所在的目录，输入：

	python app.py

即可在本机运行服务器，局域网内其他用户访问：

	(hostip):14250

（hostip为你的本机ip）便能进入网页。<br>

### 修改用户

打开users.xls，A列输入用户名，B列输入密码即可<br>
**在所有用户之后的下一行一定要在A列输入END，且用户名不可与END重复！**

## 3、数据保存

data.xls保存着上传的数据<br>
uesrs.xls保存着登录的用户数据<br>
static/picture保存着上传的图片