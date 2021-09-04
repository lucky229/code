#!/usr/bin/env python3
# -*- coding:UTF-8 -*-

# 20210729更新，从name.txt中读取需要搜索股票的名称
# 20210901更新，更新直接通过 URL 获取信息，不用selenium
#

import time
import datetime
import os

import smtplib
from email.mime.text import MIMEText
from email.header import Header

import urllib.request
from urllib.parse import urlencode
import random
import re
import math

from io import BytesIO
import gzip


# 类操作
class app:

    def __init__(self):
        self.east_url = "https://www.eastmoney.com/"

    def checkupdate(self, stocks):
        
        # 接受信息的变量
        messages = ""

        # 对每一只股票的最新资讯和公告进行搜素
        for stock in stocks:

            try:

                # 获取单支股票的资讯和公告更新情况
                message = self.message_send(stock, self.get_message(stock))

                # 如果有更新，统计更新信息
                if message != "":
                    messages = messages + message
                else:
                    pass

                # 获取一支股票资料后等10秒
                time.sleep(2)
            except:

                continue
                
            finally:
                pass

        # 关闭webdriver 服务，关闭进程
        time.sleep(2)

        # 如果资讯和公告有更新，加上最后格式
        if messages != "":
            # messages 最后一行加上格式化*
            messages = messages + "★" * 19 + "\n" + "★" * 19 + "\n"
            #print(messages)
        else:
            pass

        # 将所有股票公告和资讯更新情况发送email
        self.email_send(messages)

    def get_message(self, stock):
        # 获取最新资讯和公告

        #stock = "大连圣亚"
        # 资讯板块查找是否有最新                
        print(stock, ", Searching now ......", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

        ######################################################################
        # 公告和资讯网址
        # 公告地址
        url_ann_base = "https://searchapi.eastmoney.com/bussiness/Web/GetSearchList?"

        # 资讯地址
        url_cms_base = "https://searchapi.eastmoney.com/bussiness/Web/GetCMSSearchList?"

        # 传入的参数
        # 页数，共用，都只查找第一页就可以
        page = 1
        # 传入的  cb 参数，公告和资讯可以共用
        cb_con = "jQuery" + str(random.randint(35101808371915740692, 35109802815209746756)) + "_" + str(int(time.time()*1000))
        # 公告的参数
        param_ann = {
            "cb" : cb_con,
            "keyword" : stock, 
            "type" : "401", 
            "pageindex" : page,
            "pagesize" : "10",
            "name" : "normal",
            "_" : int(time.time()*1000)
        }
        # 资讯的参数
        param_cms = {
            "cb" : cb_con,
            "keyword" : stock, 
            "type" : "8193", 
            "pageindex" : page,
            "pagesize" : "10",
            "name" : "web",
            "_" : int(time.time()*1000)
        }

        # 构造公告连接地址
        url_ann = url_ann_base + urlencode(param_ann)
        # 构造资讯连接地址
        url_cms = url_cms_base + urlencode(param_cms)

        #########################################################
        # 请求头及相关参数
        # 常用 UA
        pc_agent = [
            "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
            "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
            "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0);",
            "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",
            "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
            "Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
            "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11",
            "Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; The World)",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Avant Browser)",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64; rv:76.0) Gecko/20100101 Firefox/76.0",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36"
        ]

        # 随机选择一个UA
        agent = random.choice(pc_agent)

        # 构造头部文件
        headers = {
            'User-Agent': agent,
            'Referer': 'https://so.eastmoney.com/',
            'Accept': '*/*',
            'Connection': 'keep-alive',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
        }

        ########################################################
        # 爬取最新公告内容和链接

        # 新公告列表
        notice_new = []

        try:
            # 公告请求
            req = urllib.request.Request(url_ann, headers = headers)
            # 获得网址内容
            con = urllib.request.urlopen(req, timeout=5).read()
        except:
            # 公告请求
            req = urllib.request.Request(url_ann, headers = headers)
            # 获得网址内容
            con = urllib.request.urlopen(req, timeout=5).read()

        # 获取内存中的二进制字节
        buff = BytesIO(con)
        # 解压
        f = gzip.GzipFile(fileobj = buff)
        # 解码
        content = f.read().decode('utf-8')
        # 清洗无用字符
        anns = content.split("[{")[1].split("}]")[0].split("},{")

        for ann in anns:

            # re.match 从字符串的开始匹配，开始没有则 匹配失败
            # re.search 在整个字符串匹配，知道找到一个匹配的
            # re.findall 匹配整个字符串所有可匹配的

            # 公告的日期
            notice_date_str = re.findall('"NoticeDate":"(.+?)",', ann)[0][:10]
            # 日期转化为datetime 格式的日期
            date_split = notice_date_str.split("-")
            notice_date = datetime.date(int(date_split[0]), int(date_split[1]), int(date_split[2]))

            # 获取datetime格式的日期
            today_date = datetime.date.today()

            if notice_date >= today_date:

                # 公告标题
                notice_title = re.search('"NoticeTitle":"(.+?)",', ann)
                # 公告的网址
                notice_link = re.search('"Url":"(.+?)",', ann)
                # 公告的内容摘要
                notice_content = re.findall('"NoticeContent":"(.+?)"', ann)

                # 写入内容中暂没包含 内容快照
                notice_new.append([notice_title.group(1), notice_link.group(1)])

        ########################################################
        # 爬取最新资讯内容和链接

        # 新资讯列表
        news_new = []

        try:
            # 公告请求
            req = urllib.request.Request(url_cms, headers = headers)
            # 获得网址内容
            con = urllib.request.urlopen(req, timeout=5).read()
        except:
            # 公告请求
            req = urllib.request.Request(url_cms, headers = headers)
            # 获得网址内容
            con = urllib.request.urlopen(req, timeout=5).read()
            
        # 获取内存中的二进制字节
        buff = BytesIO(con)
        # 解压
        f = gzip.GzipFile(fileobj = buff)
        # 解码
        content = f.read().decode('utf-8')
        # 清洗无用字符
        newses = content.split("[{")[1].split("}]")[0].split("},{")

        for news in newses:

            # re.match 从字符串的开始匹配，开始没有则 匹配失败
            # re.search 在整个字符串匹配，知道找到一个匹配的
            # re.findall 匹配整个字符串所有可匹配的

            # 公告的日期
            news_date_str = re.findall('"Art_CreateTime":"(.+?)",', news)[0][:10]
            # 日期转化为datetime 格式的日期
            date_split = news_date_str.split("-")
            news_date = datetime.date(int(date_split[0]), int(date_split[1]), int(date_split[2]))

            # 获取datetime格式的日期
            today_date = datetime.date.today()

            if news_date >= today_date:

                # 公告标题
                news_title = re.search('"Art_Title":"(.+?)",', news)
                # 公告的网址
                news_link = re.search('"Art_UniqueUrl":"(.+?)",', news)
                # 公告的内容摘要
                news_content = re.findall('"Art_Content":"(.+?)"', news)

                # 写入内容中暂没包含 内容快照
                news_new.append([news_title.group(1), news_link.group(1)])

        # 返回公告和资讯元组
        return (news_new, notice_new)

    # 对抓取的数据处理为string
    def message_send(self, stock, msgs):

        messages = ""

        # 格式装饰
        star = "★" * 19 + "\n" + "★" * 19 + "\n"
        # 判断传递进来的消息长度是否为0来判断信息是否有更新消息
        if len(msgs[0]) != 0 or len(msgs[1]) != 0:        

            # 公告情况
            if len(msgs[1]) != 0:
                messages = messages + star + "◆◆" + stock + "◆◆有更新公告\n\n"
                # 提取公告内容，转换为string格式内容
                for i in range(1, len(msgs[1]) + 1):
                    messages = messages + str(i) + "   标题：" + msgs[1][i-1][0] + "\n\t地址：" + msgs[1][i-1][1] + '\n'

                messages = messages + '\n\n\n'
            else:
                messages = messages + star + "◆◆" + stock + "◆◆没有更新公告\n\n\n"

            # 资讯情况
            if len(msgs[0]) != 0:
                messages = messages + "◆◆" + stock + "◆◆有更新资讯\n\n"
                # 提取资讯内容，转换为string格式内容
                for i in range(1, len(msgs[0]) + 1):
                    messages = messages + str(i) + "   标题：" + msgs[0][i-1][0] + "\n\t地址：" + msgs[0][i-1][1] + '\n'
            else:
                messages = messages + "◆◆" + stock + "◆◆没有更新资讯\n\n\n"

            # 返回转换后的messages，供其他函数调用
            return messages

        # 如果没有新消息，返回meaages,此时值为""
        else:
            return messages

    # 查看文件是否存在，比较内容，查看当天目前查询的内容与前次是否有变化
    def compare_content(self, messages):

        # centos7服务器上的路径
        path = '/root/py/text/'
        # 以日期为名创建text文件
        file_path = path + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())[:10] + ".txt"
        #内容为上述email_send()处理后的内容

        # windows 上的测试路径
        #path = 'D:\\code\\text\\'
        # 以日期为名创建text文件
        #file_path = path + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())[:10] + ".txt"

        # 判断传输进来的messages是否 ""
        # 不是 "" ，则与现有信息对比或创建文件储存
        if messages != "":
            # 如果文件存在，则对比最新获取的信息，信息一致则返回Fasle，否则返回True
            if os.path.exists(file_path):
                f = open(file_path,'r')
                f.seek(0)
                read = f.read()
                f.close()

                # 文件存在，对比，一致，则返回Fasle
                if read == messages:
                    return False

                # 文件存在，但不一致，重写，返回True
                else:
                    f = open(file_path,'w')
                    f.write(messages)
                    f.close()

                    return True
            
            # 文件不存在，则创建文件夹和文件
            else:
                # 文件夹路径存在，文件不存在，创建文件，写入messages
                if os.path.exists(path):
                    f = open(file_path,'w')
                    f.write(messages)
                    f.close()
                # 文件夹不存在，创建文件夹和文件，并写入messages
                else:
                    os.makedirs(path)
                    f = open(file_path,'w')
                    f.write(messages)
                    f.close()

                # 始终返回True
                return True

        # 传递进来的 message 为 "" ，表示无更新内容，则返回 Fasle
        else:
            return False

    # 发送邮件
    def email_send(self, messages):
        
        # 查询本次更新的信息与前次更新的信息是否有变化，有变化则发邮件，无变化则不发邮件
        if self.compare_content(messages):
            # 发送邮件
            # 发送邮箱服务器
            smtpserver = 'mail.pooper.tk'
            # 发送邮箱用户/密码
            user = 'admin'
            password = 'zzg4542431'
            # 发送邮箱
            sender = 'admin@pooper.tk'
            # 接收邮箱
            receivers = ['admin@pooper.tk']
            # 发送邮件主题
            subject = '关注的股票资讯和公告更新情况-' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

            # 编写HTML类型的邮件正文
            msg = MIMEText(messages,'plain','utf-8')
            msg['Subject'] = Header(subject, 'utf-8')
            msg['From'] = 'admin@pooper.tk<admin@pooper.tk>'
            msg["To"] = ";".join(receivers)

            # 连接发送邮件
            try:
                smtp = smtplib.SMTP()
                smtp.connect(smtpserver, 25)
                smtp.login(user, password)
                smtp.sendmail(sender, receivers, msg.as_string())
                print("邮件发送成功！", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

                # 关闭连接
                smtp.quit()

            except smtplib.SMTPException:
                print("Error：无法发送邮件", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
            
        else:
            print("关注的股票资讯和公告更没有更新...", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
            

    def main(self):

        print("I am working now ......", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

        # 利用服务器的 crontab 进行定时运营
        # centos7 中 name.txt 路径, name.txt中一行写一个股票名称，多个多行写，每行只写股票名称，不加其他内容
        text_path = "/root/py/name.txt"

        # 打开 name.txt 文件，读取内容，存入 stocks
        with open(text_path, "r", encoding='utf-8') as f:
            stocks = f.readlines()
            f.close()

        # 对读取的 stocks 的内容进行清洗，使之成为仅有股票名称的list
        i = 0
        while i < len(stocks):
            # 取出每个名称中的空格，和换行符"\n"等
            stocks[i] = stocks[i].strip()
            i = i + 1

        self.checkupdate(stocks)
        
        '''
        # 一直循环,如果程序出错，将全部停止
        while True:

            # name.txt文件地址，windows测试地址
            #text_path = "D:\\code\\name.txt"

            # centos7 中 name.txt 路径, name.txt中一行写一个股票名称，多个多行写，每行只写股票名称，不加其他内容
            text_path = "/root/py/name.txt"

            # 打开 name.txt 文件，读取内容，存入 stocks
            with open(text_path, "r", encoding='utf-8') as f:
                stocks = f.readlines()
                f.close()

            # 对读取的 stocks 的内容进行清洗，使之成为仅有股票名称的list
            i = 0
            while i < len(stocks):
                # 取出每个名称中的空格，和换行符"\n"等
                stocks[i] = stocks[i].strip()
                i = i + 1

            # 获取当前时间,使用datetime.datetime.now().time(),方便比较
            time_now = datetime.datetime.now().time()

            if time_now < datetime.time(8, 30):
                # 每隔10分钟运行一次
                time.sleep(600)

            else:
                # 检查更新股票资讯和公告情况，并对更新资讯和公告大邮件提醒
                self.checkupdate(stocks)
                # 每隔60分钟搜索一次
                time.sleep(3600)
        '''
                
# 主程序,运行
if __name__ == '__main__':
    
    app = app()

    app.main()