## 武汉理工大学健康填报自动化脚本（研究生版本）

该脚本是基于[此项目](https://github.com/xiaozhangtongx/WHUT-JKRBTB
)进行的修改，由于研究生版本的健康填报请求的地址不同，因此使用fiddler进行抓包，然后对着代码进行修改即可。

微信小程序中填报的相关链接有四个：`checkBind`，`bindUserInfo`，`monitorRegister`和`cancelBind`，查看fiddler修改请求头和体温记录，位置信息即可。

### 使用教程

**注意使用前请先取消小程序的关联**

首先上代码：`main.py`

```python
import json
import random

import mail
import requests

temperature = ["36\"C~36.5°C", "36.5°C~36.9°C"]

useragentlist = [
    "Mozilla/5.0 (Linux; U; Android 7.1.2; zh-cn; MI 6 Build/NXTHUAWEI) AppleWebKit/537.36 (KHTML, like Gecko)Version/4.0 MQQBrowser/9.9 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 9_3_5 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Mobile/13G36 baiduboxapp/0_01.5.2.8_enohpi_6311_046/5.3.9_1C2%8enohPi/1099a/7D4BD508A31C4692ACC31489A6AA6FAA3D5694CC7OCARCEMSHG/1",
    "Mozilla/5.0 (Linux; U; Android 4.4.4; en-us; vivo X5Max Build/KTU84P) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 UCBrowser/1.0.0.100 U3/0.8.0 Mobile Safari/534.30 AliApp(TB/6.5.0) WindVane/8.0.0 1080X1920 GCanvas/1.4.2.21",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 10_2 like Mac OS X) AppleWebKit/602.3.12 (KHTML, like Gecko) Mobile/14C92 baiduboxapp/0_01.5.2.8_enohpi_8022_2421/2.01_2C2%8enohPi/1099a/05D5623EBB692D46C9C9659B23D68FBD5C7FEB228ORMNJBQOHM/1",
    "Mozilla/5.0 (Linux; Android 8.0.0; BKL-AL00 Build/HUAWEIBKL-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/76.0.3809.89 Mobile Safari/537.36 T7/11.19 SP-engine/2.15.0 baiduboxapp/11.19.5.10 (Baidu; P1 8.0.0)",
    "Mozilla/5.0 (Linux; Android 8.1.0; vivo X20 Build/OPM1.171019.011; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/76.0.3809.89 Mobile Safari/537.36 T7/11.19 SP-engine/2.15.0 baiduboxapp/11.19.5.10 (Baidu; P1 8.1.0)",
    "Mozilla/5.0 (Linux; Android 9; DUK-AL20 Build/HUAWEIDUK-AL20; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/76.0.3809.89 Mobile Safari/537.36 T7/11.19 SP-engine/2.15.0 baiduboxapp/11.19.5.10 (Baidu; P1 9)"
]


def request_sessionId(json_data):
    url = "https://yjsxx.whut.edu.cn/wx/api/login/checkBind"
    headers = {
        "Accept-Encoding": "gzip, deflate, br",
        "content-type": "application/json",

        "Referer": "https://servicewechat.com/wx225eb50c34f6f98e/13/page-frame.html",
        "X-Tag": "flyio",
        "Content-Length": "136",
        # "Accept-Language": "zh-cn",
        "Connection": "keep - alive",
        "Host": "yjsxx.whut.edu.cn"
    }
    headers['User-Agent'] = random.choice(useragentlist)
    r = requests.post(url=url, headers=headers, json=json_data)
    # print(r)
    result = json.loads(r.text)
    # print("request_sessionId", result)
    sessionId = result['data']['sessionId']
    return str(sessionId)


def request_bindUserInfo(sessionId, json_data):
    url = "https://yjsxx.whut.edu.cn/wx/api/login/bindUserInfo"
    headers = {
        "Accept-Encoding": "gzip, deflate, br",
        "content-type": "application/json",
        "Referer": "https://servicewechat.com/wx225eb50c34f6f98e/13/page-frame.html",
        "Cookie": "JSESSIONID=%s" % (sessionId),
        # "Accept": "*/*",
        "X-Tag": "flyio",
        "Content-Length": "296",
        # "Accept-Language": "zh-cn",
        "Connection": "keep - alive",
        "Host": "yjsxx.whut.edu.cn"
    }
    headers['User-Agent'] = random.choice(useragentlist)
    print(json_data)
    r = requests.post(url=url, headers=headers, json=json_data)
    result = json.loads(r.text)
    # print("request_bindUserInfo", result)


def request_monitorRegister(sessionId, province, city, county, street):
    currentAddress = str(province) + str(city) + str(county) + str(street)
    url = "https://yjsxx.whut.edu.cn/wx/monitorRegister"
    headers = {
        "Accept-Encoding": "gzip, deflate, br",
        "content-type": "application/json",
        "Referer": "https://servicewechat.com/wx225eb50c34f6f98e/13/page-frame.html",
        "Cookie": "JSESSIONID=%s" % (sessionId),
        # "Accept": "*/*",
        "X-Tag": "flyio",
        "Content-Length": "552",
        # "Accept-Language": "zh-cn",
        "Connection": "keep - alive",
        "Host": "yjsxx.whut.edu.cn"
    }
    headers['User-Agent'] = random.choice(useragentlist)
    # json数据根据是否在校修改
    json_data = {
        "diagnosisName": "",
        "relationWithOwn": "",
        "currentAddress": currentAddress,
        "remark": "",
        "healthInfo": "正常",
        "isDiagnosis": "0",
        "isFever": "0",
        "isInSchool": "0",
        "isLeaveChengdu": "1",
        "isSymptom": "0",
        "temperature": random.choice(temperature),
        "noonTemperature": random.choice(temperature),
        "eveningTemperature": random.choice(temperature),
        "province": province,
        "city": city,
        "county": county
    }
    r = requests.post(url=url, headers=headers, json=json_data)
    result = json.loads(r.text)
    # print("request_monitorRegister", result)
    return result


def cancelBind(sessionId):
    url = "https://yjsxx.whut.edu.cn/wx/api/login/cancelBind"
    headers = {
        "Accept-Encoding": "gzip, deflate, br",
        "content-type": "application/json",
        "Referer": "https://servicewechat.com/wx225eb50c34f6f98e/13/page-frame.html",
        "Cookie": "JSESSIONID=%s" % (sessionId),
        "Connection": "keep - alive",
        "Host": "yjsxx.whut.edu.cn"
    }
    headers['User-Agent'] = random.choice(useragentlist)
    r = requests.post(url=url, headers=headers)
    result = json.loads(r.text)
    # print("cancelBind", result)


if __name__ == '__main__':
    data = {'sn': '这里填账号(身份证)', 'idCard': '这里填密码(默认身份证后6位)'}
    sessionId = request_sessionId(data)
    request_bindUserInfo(sessionId, data)
    # 地址格式为：province+city+county+street
    res = request_monitorRegister(sessionId, "湖北省", "仙桃市", "仙桃市", "永乐路6号")
    if res['code'] == 0:
        mail.sendmail(["success", res['message']])
    else:
        mail.sendmail(["error", res['message']])
    cancelBind(sessionId)
```

需要修改为自己的账号和密码，地址和是否在校需要对应修改。与参考项目不同的是`Header`中`Host`，`Referer`和`Content-Length`有所区别，这里已经修改好了。

使用邮件提醒打卡结果：`mail.py`

```python
import yagmail


def sendmail(data):
    try:
        yag = yagmail.SMTP(user='xxx@qq.com', password='SMTP生成的临时密码', host='smtp.qq.com')
        yag.send(to='你接收信息的邮箱', subject='健康打卡', contents=data)
        print('Email send success')
    except:
        print('Email send fail')
```

这里需要开通邮箱的SMTP服务，会生成一个授权码，填上以后就可以接收提醒了。当然也可以不要`mail.py`，注释掉main中的代码，自己手动去看也可以。

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