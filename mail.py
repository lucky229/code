#!/usr/bin/env python3
# -*- coding:UTF-8 -*-

import smtplib
from email.mime.text import MIMEText
from email.header import Header

import datetime

def email_send(messages):
    # message 邮件发送的信息
    
    # 发送邮箱服务器
    smtpserver = 'smtp.163.com'
    # 发送邮箱用户/密码
    user = 'ws229'
    password = 'TXTAQFDMZITHSINO'
    # 发送邮箱
    sender = 'ws229@163.com'
    # 接收邮箱
    receivers = ['8780037@qq.com',]
    # 发送邮件主题
    subject = '股票资讯更新-' + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 编写HTML类型的邮件正文
    msg = MIMEText(messages,'plain','utf-8')
    msg['Subject'] = Header(subject, 'utf-8')
    msg['From'] = 'ws229@163.com<ws229@163.com>'
    msg["To"] = ";".join(receivers)

    # 连接发送邮件
    try:
        smtp = smtplib.SMTP()
        smtp.connect(smtpserver, 25)
        smtp.login(user, password)
        smtp.sendmail(sender, receivers, msg.as_string())
        print("邮件发送成功！", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

        # 关闭连接
        smtp.quit()

    except smtplib.SMTPException:
        print("Error：无法发送邮件", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))     

if __name__ == '__main__':
	email_send("hello")