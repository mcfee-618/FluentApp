# -*- coding: utf-8 -*-

##TODO 定时备份数据库脚本同时发邮件
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from dotenv import load_dotenv


def send_emali(msg,address):
    load_dotenv()
    sender= os.getenv("email_address")
    from_addr = os.getenv("email_address")
    password = os.getenv("password")
    receivers = [address]  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱
    #创建一个带附件的实例
    message = MIMEMultipart()
    message['From'] = Header(sender)
    message['To'] =  Header(address)
    subject = '北京天气预报'
    message['Subject'] = Header(subject, 'utf-8')
    #邮件正文内容
    message.attach(MIMEText(msg, 'plain', 'utf-8'))

    try:
        server = smtplib.SMTP_SSL(host="smtp.163.com")
        server.connect("smtp.163.com",465)
    # 登录发信邮箱
        server.login(from_addr, password)
        server.sendmail(sender, receivers, message.as_string())
        print ("邮件发送成功")
    except smtplib.SMTPException as e:
        print ("Error: 无法发送邮件")
        print(e)
