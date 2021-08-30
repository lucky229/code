#!/usr/bin/env python3
# -*- coding:UTF-8 -*-

import urllib.request
from urllib.parse import urlencode
import time
import random
import re
import math

from io import BytesIO
import gzip

def getMsg():

    # 服务器前随机数据
    num = random.randint(1,100)
    # 随机数字
    numm = random.randint(112401080181359666863,112408018548274208226)

    """
    代码：F12
    名称：F14
    最新价：F2
    涨跌幅：F3
    涨跌额：F4
    成交手：F5
    成交额：F6
    振幅：F7
    换手率：F8
    市盈率：F9
    量比：F10
    最高：F16
    最低：F16
    今开：F17
    昨收：F18
    市净率：F23
    总市值：F20
    流通市值：F21
    60日涨跌幅：F24
    年初至今涨幅：F25

    """
    # 第一页
    page = 1

    url1 = 'http://%d.push2.eastmoney.com/api/qt/clist/get?cb=jQuery%d_%d'% (num, numm, int(time.time()*1000))
    url2 = '&pn=1&pz=20&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&fid=f3&'
    url3 = 'fs=m:0+t:6,m:0+t:80,m:1+t:2,m:1+t:23&fields=f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,'
    url4 = 'f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,f22,f11,f62,f128,f136,f115,f152&_=%d'% int(time.time()*1000)

    url = url1 + url2 + url3 + url4

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
        "Mozilla/5.0 (X11; Linux x86_64; rv:76.0) Gecko/20100101 Firefox/76.0"
    ]

    # 随机选择一个UA
    agent = random.choice(pc_agent)

    # 构造头部文件
    headers = {
        'User-Agent': agent,
        'Referer': 'http://quote.eastmoney.com/',
        'Accept': '*/*',
        'Connection': 'keep-alive',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Accept-Encoding': 'gzip, deflate',
    }

    req = urllib.request.Request(url, headers = headers)
    
    con = urllib.request.urlopen(req).read().decode("utf8")

    total = int(re.findall('"total":(.*?),',con)[0])
    pages = math.ceil(total/20)
    #print(total, pages)

    msg_all = []

    while page < pages + 1:

        if page == 1:
            pass
        else:
            # 构造下一个访问地址
            url2 = '&pn=%d&pz=20&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&fid=f3&' % page
            url = url1 + url2 + url3 + url4

            # 随机选择一个UA
            agent = random.choice(pc_agent)

            headers = {
                'User-Agent': agent,
                'Referer': 'http://quote.eastmoney.com/',
                'Accept': '*/*',
                'Connection': 'keep-alive',
                'Accept-Language': 'zh-CN,zh;q=0.9',
                'Accept-Encoding': 'gzip, deflate',
            }

            # 向地址发出响应
            req = urllib.request.Request(url, headers = headers)
            # 获取也没内容
            con = urllib.request.urlopen(url).read().decode("utf8")



        data = con.split("[")[1][1:-6].split("},{")

        code = re.findall('"f12":(.*?),',data[0])[0]
        code = code[1:-1]

        name = re.findall('"f14":(.*?),',data[0])[0]
        name = name[1:-1]

        close = re.findall('"f2":(.*?),',data[0])[0]
        close = to_0(close)

        rate = re.findall('"f3":(.*?),',data[0])[0]
        rate = to_0(rate)

        zhangde = re.findall('"f4":(.*?),',data[0])[0]
        zhangde = to_0(zhangde)

        chengjl = re.findall('"f5":(.*?),',data[0])[0]
        chengjl = to_0(chengjl)

        chengje = re.findall('"f6":(.*?),',data[0])[0]
        chengje = to_0(chengje)

        zhenfu = re.findall('"f7":(.*?),',data[0])[0]
        zhenfu = to_0(zhenfu)

        high = re.findall('"f15":(.*?),',data[0])[0]
        high = to_0(high)

        low = re.findall('"f16":(.*?),',data[0])[0]
        low = to_0(low)

        ope = re.findall('"f17":(.*?),',data[0])[0]
        ope = to_0(ope)

        closebef = re.findall('"f18":(.*?),',data[0])[0]
        closebef = to_0(closebef)

        liangbi = re.findall('"f10":(.*?),',data[0])[0]
        liangbi = to_0(liangbi)

        huanshoulv = re.findall('"f8":(.*?),',data[0])[0]
        huanshoulv = to_0(huanshoulv)

        pe = re.findall('"f9":(.*?),',data[0])[0]
        pe = to_0(pe)

        pb = re.findall('"f23":(.*?),',data[0])[0]
        pb = to_0(pb)

        # 从网页爬取的信息
        msg = [code, name, close, rate, zhangde, chengjl, chengje, zhenfu, high, low, ope, closebef, liangbi, huanshoulv, pe, pb]

        # 计算 priceindex

        # 页面 + 1
        page = page + 1




def to_0(data):

    if data == '"-"':
        data = 0
    else:
        data = data

    return data

def getzi():

    url_ann_base = "https://searchapi.eastmoney.com/bussiness/Web/GetSearchList?"
    url_cms_base = "https://searchapi.eastmoney.com/bussiness/Web/GetCMSSearchList?"
    page = 1
    cb_con = "jQuery" + str(random.randint(35101808371915740692, 35109802815209746756)) + "_" + str(int(time.time()*1000))

    param_ann = {
        "cb" : cb_con,
        "keyword" : "大连圣亚", 
        "type" : "401", 
        "pageindex" : page,
        "pagesize" : "10",
        "name" : "normal",
        "_" : int(time.time()*1000)
    }

    # 构造连接地址
    url = url_ann_base + urlencode(param_ann)
    print(url)
    # 构造头部文件
    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
        'Referer': 'http://quote.eastmoney.com/',
        'Accept': '*/*',
        'Connection': 'keep-alive',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Accept-Encoding': 'gzip, deflate',
    }

    # 请求
    req = urllib.request.Request(url, headers = headers)
    # 获得网址内容
    con = urllib.request.urlopen(req).read()
    # 获取内存中的二进制字节
    buff = BytesIO(con)
    # 解压
    f = gzip.GzipFile(fileobj = buff)
    # 解码
    content = f.read().decode('utf-8')
    # 清洗无用字符
    anns = content.split("[{")[1].split("}]")[0].split("},{")

    # re.match 从字符串的开始匹配，开始没有则 匹配失败
    # re.search 在整个字符串匹配，知道找到一个匹配的
    # re.findall 匹配整个字符串所有可匹配的
    notice_title = re.search('"NoticeTitle":"(.+?)",', anns[0])
    notice_url = re.search('"Url":"(.+?)",', anns[0])
    notice_date = re.findall('"NoticeDate":"(.+?)",', anns[0])[0][:10]
    notice_content = re.findall('"NoticeContent":"(.+?)"', anns[0])[0]

    print(notice_title.group(1))
    print(notice_url.group(1))
    print(notice_date)


 
if __name__ == '__main__':
    getzi()


