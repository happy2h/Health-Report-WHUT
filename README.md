## 武汉理工大学健康填报自动化脚本（研究生版本）

该脚本是基于[此项目](https://github.com/xiaozhangtongx/WHUT-JKRBTB
)进行的修改，由于研究生版本的健康填报请求的地址不同，因此使用fiddler进行抓包，然后对着代码进行修改即可。

微信小程序中填报的相关链接有四个：`checkBind`，`bindUserInfo`，`monitorRegister`和`cancelBind`，查看fiddler修改请求头和体温记录，位置信息即可。

### 使用教程

**注意使用前请先取消小程序的关联**

首先需要在`main.py`修改为自己的账号和密码，地址和是否在校需要对应修改。与参考项目不同的是`Header`中`Host`，`Referer`和`Content-Length`有所区别，这里已经修改好了。

使用邮件提醒打卡结果：`mail.py`。这里需要开通邮箱的SMTP服务，会生成一个授权码，填上以后就可以接收提醒了。当然也可以不要`mail.py`，注释掉main中的代码，自己手动去看也可以。

运行需要安装python3，然后终端中执行下面命令pip安装包：

```shell
pip install requests
pip install yagmaill
```

安装完成后直接运行main.py即可

## 服务器部署

把脚本部署到宝塔面板上，首先上传文件到宝塔目录里，记录路径。由于之前宝塔安装的是python2.7，需要升级python版本。

注意这里遇到的坑，直接下载python3以上的版本解压编译，然后运行脚本会提示`ssl no host`的错误，原因在编译python时没有编译ssl模块.

解决方法：在**编译python3前**指定openssl的安装目录。

这里需要查看你服务器安装openssl没有，使用`whereis openssl`找到openssl的安装目录，一般在`usr\local\openssl`，没有的话可以先安装open ssl1.0.2以上的版本。[仓库地址](https://github.com/openssl/openssl/releases)，上传到宝塔自定义目录，解压编译安装：

```shell
tar -xvf openssl-xxx.tar.gz
cd openssl-xxx
./config  no-shared -no-tests --prefix=/usr/local/openssl --openssldir=/usr/local
```

然后在解压的python3目录：`../Python-3.6.4/Modules`下修改`setup`文件，取消以下4行（6-9）的注释。`SSL=/usr/local/openssl`这里填上你自己的安装目录。

```
# Socket module helper for socket(2)
#_socket socketmodule.c

# Socket module helper for SSL support; you must comment out the other
# socket line above, and possibly edit the SSL variable:
SSL=/usr/local/openssl
_ssl _ssl.c \
	-DUSE_SSL -I$(SSL)/include -I$(SSL)/include/openssl \
	-L$(SSL)/lib -lssl -lcrypto

# The crypt module is now disabled by default because it breaks builds
# on many systems (where -lcrypt is needed), e.g. Linux (I believe).
#
# First, look at Setup.config; configure may have set this for you.

#_crypt _cryptmodule.c # -lcrypt	# crypt(3); needs -lcrypt on some systems
```

修改完成后编译安装python即可`make && make install`。

接着设置python3为默认版本，可以参考[这篇](https://blog.csdn.net/weixin_41798704/article/details/88238222)，修改完后，安装`requests`和`yagmail`包，然后在宝塔面板的定时任务上设置shell脚本如下，定时执行即可。

![image-20220220095747102](https://blogcdn.nickxie.top/img/image-20220220095747102.png)