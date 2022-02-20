import yagmail


def sendmail(data):
    try:
        yag = yagmail.SMTP(user='xxx@qq.com', password='SMTP生成的临时密码', host='smtp.qq.com')
        yag.send(to='你接收信息的邮箱', subject='健康打卡', contents=data)
        print('Email send success')
    except:
        print('Email send fail')
