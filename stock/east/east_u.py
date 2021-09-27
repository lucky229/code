#!/usr/bin/env python3
# -*- coding:UTF-8 -*-

# date:20210820
# content: 自动从东方财富网抓取当天的所有股票行情
#          在行情里面加入一项：价格系数，以20210820开盘前的价格全部为系数100，以后每天的价格系数直接按照找跌幅进行计算
#          并在每天抓取数据后计算，将每天的数据计算后存入数据库
#
#
#

from selenium import webdriver  # 用来驱动浏览器的
#from selenium.webdriver import ActionChains  # 破解滑动验证码的时候用的 可以拖动图片
from selenium.webdriver.common.by import By  # 按照什么方式查找，By.ID,By.CSS_SELECTOR
from selenium.webdriver.common.keys import Keys  # 键盘按键操作
from selenium.webdriver.support import expected_conditions as EC  # 和下面WebDriverWait一起用的
from selenium.webdriver.support.wait import WebDriverWait  # 等待页面加载某些元素
from selenium.webdriver.chrome.service import Service     # webdriver 服务，关闭浏览器后在关闭服务--》实现完全关闭

import datetime
import time
import pymysql

import urllib.request
import random
import re
import math

# 类操作
class app:

    def __init__(self):
        self.east_url = "http://quote.eastmoney.com/center/gridlist.html#hs_a_board"
        self.pricebase = 100

        # 假期，除周六和周日外的非交易日
        self.holiday = [datetime.date(2021, 9, 20), datetime.date(2021, 9, 21), datetime.date(2021, 10, 1), \
                        datetime.date(2021, 10, 4), datetime.date(2021, 10, 5), datetime.date(2021, 10, 6), \
                        datetime.date(2021, 10, 7)]
        
    # 更换为分析地址方法，效率高些
    # 打开webdriver服务和chrome浏览器，放弃，效率太低
    def getData(self):

        # 无窗口启动设置
        options = webdriver.ChromeOptions()
        options.add_argument('--headless') #无头启动，无窗口加载
        #options.add_argument('window-size=1920x3000') #指定浏览器分辨率
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        #options.add_argument("service_args=['–ignore-ssl-errors=true', '–ssl-protocol=TLSv1']")
        options.add_argument('--disable-gpu') #不开启gpu加速
        #options.add_argument('--hide-scrollbars') #隐藏滚动条, 应对一些特殊页面
        #options.add_argument('blink-settings=imagesEnabled=false') #不加载图片, 提升速度
          
        path_chromedriver = "D:\\Python\\Python38\\Scripts\\chromedriver.exe"
        #path_chromedriver = "/usr/bin/chromedriver"
        # 开启webdriver服务
        c_service = Service(path_chromedriver)
        c_service.command_line_args()
        c_service.start()

        try:
            # 打开浏览器
            driver = webdriver.Chrome(executable_path = path_chromedriver, options = options)
            driver.implicitly_wait(10)
            driver.get(self.east_url)

            # 找到总页数
            page_tag = driver.find_element_by_class_name("paginate_page")
            page = page_tag.find_elements_by_xpath("./a")
            # 总页数
            pagetop = int(page[-1].get_attribute("textContent"))
            # 当前页数
            pagecurrent = int(driver.find_element_by_class_name("current").get_attribute("textContent"))

            msg_all = []

            while pagecurrent < pagetop:
                # 股票行业tag
                tbody_tag = driver.find_element_by_xpath("//tbody")
                # 当页股票行情信息
                tr_tags = tbody_tag.find_elements_by_xpath("./tr")

                # 当页内容
                for tr_tag in tr_tags:
                    # 单支股票行情信息
                    td_tag = tr_tag.find_elements_by_xpath("./td")

                    msg = []
                    for i in list(range(len(td_tag))):
                        if i == 0 or i == 3 or i == 18:
                            pass
                        elif i == 5 or i == 9 or i == 15:
                            if td_tag[i].get_attribute("textContent") == "-":
                                msg.append("0")
                            else:
                                msg.append(td_tag[i].get_attribute("textContent")[:-1])
                        else:
                            if td_tag[i].get_attribute("textContent") == "-":
                                msg.append("0")
                            else:
                                msg.append(td_tag[i].get_attribute("textContent"))
                    # priceindex
                    priceindex = self.priceindex(msg[0]) * (100 + float(msg[3]))/100

                    msg.append(priceindex)

                    msg_all.append(msg)

                # 翻页，下一页
                next_tag = driver.find_element_by_class_name("next")
                next_tag.click()

                time.sleep(2)

                # 当前第几页
                page_tag = driver.find_element_by_class_name("paginate_page")
                page = page_tag.find_elements_by_xpath("./a")
                # 当前页数
                pagecurrent = int(driver.find_element_by_class_name("current").get_attribute("textContent"))

                # 如果是最后一页，获取信息
                if pagecurrent == pagetop:

                    # 股票行业tag
                    tbody_tag = driver.find_element_by_xpath("//tbody")
                    # 当页股票行情信息
                    tr_tags = tbody_tag.find_elements_by_xpath("./tr")

                    # 当页内容
                    for tr_tag in tr_tags:
                        # 单支股票行情信息
                        td_tag = tr_tag.find_elements_by_xpath("./td")

                        msg = []
                        for i in list(range(len(td_tag))):
                            if i == 0 or i == 3 or i == 18:
                                pass
                            elif i == 5 or i == 9 or i == 15:
                                if td_tag[i].get_attribute("textContent") == "-":
                                    msg.append("0")
                                else:
                                    msg.append(td_tag[i].get_attribute("textContent")[:-1])
                            else:
                                if td_tag[i].get_attribute("textContent") == "-":
                                    msg.append("0")
                                else:
                                    msg.append(td_tag[i].get_attribute("textContent"))
                        # priceindex
                        priceindex = self.priceindex(msg[0]) * (100 + float(msg[3]))/100

                        msg.append(priceindex)

                        msg_all.append(msg)

                else:
                    pass


        #except:
        #    print("err")
        #    driver.quit()

        finally:
            driver.quit()
            c_service.stop()

        return msg_all

    # 分析地址和传递参数的方法获取数据
    # 效率高
    def getMsg(self):

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
            'Accept-Encoding': 'gzip, deflate'
        }

        try:
            # 请求
            request = urllib.request.Request(url, headers = headers)
            # 获取内容
            con = urllib.request.urlopen(request, timeout=5).read().decode("utf8")
        except:
            # 请求
            request = urllib.request.Request(url, headers = headers)
            # 获取内容
            con = urllib.request.urlopen(request, timeout=5).read().decode("utf8")
            
        # 总页数
        total = int(re.findall('"total":(.*?),',con)[0])
        pages = math.ceil(total/20)
        #print(total, pages)

        # 全部股票信息
        msg_all = []

        while page < pages + 1:

            print("第 %d 页，共 %d 页，数据抓取中......" % (page, pages), time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

            if page == 1:
                pass
            else:
                # 构造下一个访问地址
                url22 = '&pn=%d&pz=20&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&fid=f3&' % page
                url = url1 + url22 + url3 + url4

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

            # 获取地址内容
            try:
                # 向地址发出响应
                request = urllib.request.Request(url, headers = headers)
                # 获取网页内容
                con = urllib.request.urlopen(request, timeout=5).read().decode("utf8")
            except:
                # 向地址发出响应
                request = urllib.request.Request(url, headers = headers)
                # 获取网页内容
                con = urllib.request.urlopen(request, timeout=5).read().decode("utf8")



            datas = con.split("[")[1][1:-6].split("},{")
            for data in datas:

                code = re.findall('"f12":(.*?),',data)[0]
                code = code[1:-1]

                name = re.findall('"f14":(.*?),',data)[0]
                name = name[1:-1]

                close = re.findall('"f2":(.*?),',data)[0]
                close = self.to_0(close)

                rate = re.findall('"f3":(.*?),',data)[0]
                rate = self.to_0(rate)

                zhangde = re.findall('"f4":(.*?),',data)[0]
                zhangde = self.to_0(zhangde)

                chengjl = re.findall('"f5":(.*?),',data)[0]
                chengjl = self.to_0(chengjl)

                chengje = re.findall('"f6":(.*?),',data)[0]
                chengje = self.to_0(chengje)

                zhenfu = re.findall('"f7":(.*?),',data)[0]
                zhenfu = self.to_0(zhenfu)

                high = re.findall('"f15":(.*?),',data)[0]
                high = self.to_0(high)

                low = re.findall('"f16":(.*?),',data)[0]
                low = self.to_0(low)

                ope = re.findall('"f17":(.*?),',data)[0]
                ope = self.to_0(ope)

                closebef = re.findall('"f18":(.*?),',data)[0]
                closebef = self.to_0(closebef)

                liangbi = re.findall('"f10":(.*?),',data)[0]
                liangbi = self.to_0(liangbi)

                huanshoulv = re.findall('"f8":(.*?),',data)[0]
                huanshoulv = self.to_0(huanshoulv)

                pe = re.findall('"f9":(.*?),',data)[0]
                pe = self.to_0(pe)

                pb = re.findall('"f23":(.*?),',data)[0]
                pb = self.to_0(pb)

                # 从网页爬取的信息
                msg = [code, name, close, rate, zhangde, chengjl, chengje, zhenfu, high, low, ope, closebef, liangbi, huanshoulv, pe, pb]

                # 计算 priceindex, 并加入 msg 中
                priceindex = self.priceindex(msg[0]) * (100 + float(msg[3]))/100
                msg.append(priceindex)

                # 单个股票信息保存进 msg_all
                msg_all.append(msg)

            #time.sleep(1)

            # 页面 + 1
            page = page + 1

        return msg_all

    # 转换 "-" 为0
    def to_0(self, data):

        if data == '"-"':
            data = 0
        else:
            data = data

        return data    



    # 获取总页数
    def getPage(self, driver):
        # 获取东方财富沪深A行情的总页数

        # 找到总页数
        page_tag = driver.find_element_by_class_name("paginate_page")

        page = page_tag.find_elements_by_xpath("./a")

        pagetop = int(page[-1].get_attribute("textContent"))

        #curr = page_tag.find_element_by_xpath("./a[@class='current'")
        pagecurrent = int(driver.find_element_by_class_name("current").get_attribute("textContent"))
        #pagecurrent = int(driver.find_element_by_css_selector(".paginate_button.current").get_attribute("textContent"))
        #pagecurrent = curr.get_attribute("textContent")

        return (pagetop, pagecurrent)

    # 价格指数
    def priceindex(self, code):
        
        # 开始计算价格指数的日期
        start_data = datetime.date(2021, 8, 20)
        tablename = "data" + self.beforeday().strftime("%Y%m%d")

        if datetime.date.today() > start_data:

            # 打开数据库连接
            db = pymysql.connect(host="localhost", user="root", password="123456",database="stock", charset="utf8")

            # 使用 cursor() 方法创建一个游标对象 cursor
            cursor = db.cursor()

            sql_look = """select priceindex from {0} where code = {1} """.format(tablename, code)

            cursor.execute(sql_look)
            priceindex = cursor.fetchone()

            if priceindex == None:
                # 以前无此股，则默认为100
                priceindex = self.pricebase
            else:
                # 前一交易日有 priceindex 值，则取出
                priceindex = priceindex[0]

            # 提交
            db.commit()

            # 关闭光标对象
            cursor.close()
             
            # 关闭数据库连接
            db.close()
        else:
            # 查询的priceindex 日期超期，则统一按照100计算
            priceindex = self.pricebase

        return priceindex


    # 连接数据库，写入数据
    def operatTable(self, msg):

        # 打开数据库连接
        db = pymysql.connect(host="localhost", user="root", password="123456",database="stock", charset="utf8")

        # 使用 cursor() 方法创建一个游标对象 cursor
        cursor = db.cursor()

        table_name = "data" + self.tradingday().strftime("%Y%m%d")

        # 在当天，删除数据表再重新创建
        if datetime.date.today().strftime("%Y%m%d") == table_name[4:]:
            order_drop = """DROP TABLE IF EXISTS %s""" % table_name
            cursor.execute(order_drop)
            db.commit()

        else:
            pass

        # 创建数据表格，表头包括：代码，名称，
        sql = """CREATE TABLE IF NOT EXISTS %s(num int(10) primary key auto_increment,
                                            code varchar(100), 
                                            name varchar(100), 
                                            close float,
                                            rate float,
                                            zhangde float,
                                            chengjl varchar(30),
                                            chengje varchar(30),
                                            zhenfu float,
                                            high float,
                                            low float,
                                            open float,
                                            closebef float,
                                            liangbi float,
                                            huanshoulv float,
                                            pe float,
                                            pb float,
                                            priceindex float
                                            )ENGINE=innodb DEFAULT CHARSET=utf8;""" % table_name

        cursor.execute(sql)


        # 在表格中出入数据
        order_insert = "INSERT INTO %s"%table_name + """(code, name, close, rate, zhangde, chengjl, chengje, zhenfu, 
                high, low, open, closebef, liangbi, huanshoulv, pe, pb, priceindex) 
                VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"""
        
        cursor.executemany(order_insert, msg)

        # 提交
        db.commit()

        # 关闭光标对象
        cursor.close()
         
        # 关闭数据库连接
        db.close()

    # 计算出入的多少个交易日前的日期
    def beforeday(self, daydelta=1):
        # daydelta 为0 时，判断今天是否交易日，若不是，返回最近的交易日
        # daydelta 不为0时，并判断最近交易日，并返回最近交易日前 daytelta 交易日的日期

        # 先定义bf_day 为最近交易日
        bf_day = self.tradingday()

        # 需要多少交易以前，循环多少次
        for i in list(range(daydelta)):

            # 星期六是5，星期日是6
            while True:
                # 前一天
                bf_day = bf_day + datetime.timedelta(days = (-1))

                # 判断是否假期，是假期继续循环，不是跳出while
                if bf_day.weekday() in [5, 6] or bf_day in self.holiday:
                    pass                    
                else:
                    break
    
        # 返回要求的日期，datetime.date 格式
        return bf_day

    # 返回最近交易日
    def tradingday(self):

        # 先定义trade_day 为当天
        trade_day = datetime.date.today()

        # 星期六是5，星期日是6
        while True:
                                
            # 判断是否假期，是假期继续循环，不是跳出while
            if trade_day.weekday() in [5, 6] or trade_day.weekday() in self.holiday:
                # 前一天
                trade_day = trade_day + datetime.timedelta(days = (-1))

            else:
                break

        return trade_day

    # 前提：今天是交易日
    # 判断数据库中是否已经有今天的数据表（主要防止一次爬取数据不成功）服务器设置隔半个小时运行一次 
    def isExist(self):
        db = pymysql.connect(host="localhost", user="root", password="123456",database="stock", charset="utf8")

        # 使用 cursor() 方法创建一个游标对象 cursor
        cursor = db.cursor()
        # 查询表格
        order_show = "show tables;"
        cursor.execute(order_show)
        tables_list = cursor.fetchall()
        # 今天的数据表名称
        tab_today = "data" + self.tradingday().strftime("%Y%m%d")

        # 关闭光标对象
        cursor.close()
         
        # 关闭数据库连接
        db.close()

        # 今天的数据是否存在，存在返回 True， 不存在则返回 False
        if tuple((tab_today,)) in tables_list:
            return True
        else:
            return False

    def main(self):

        print("I am working now! -- ", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        if datetime.date.today() == self.tradingday():
            if self.isExist():
                print("Data exist already today! -- ", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
            else:
                self.operatTable(self.getMsg())
                print("I have got the data of the all stocks today! -- ", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        else:
            print("Today is not trading day! -- ", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

# 主程序,运行
if __name__ == '__main__':
    
    app = app()

    app.main()