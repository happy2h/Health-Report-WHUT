import yagmail


def sendmail(data):
    try:
        yag = yagmail.SMTP(user='3555232441@qq.com', password='jkhufenzzcccdcbd', host='smtp.qq.com')
        yag.send(to='你接收信息的邮箱', subject='健康打卡', contents=data)
        print('Email send success')
    except:
        print('Email send fail')
