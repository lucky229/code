#!/usr/bin/env python3
# -*- coding:UTF-8 -*-

# 20210729更新，从name.txt中读取需要搜索股票的名称
#
#

from selenium import webdriver  # 用来驱动浏览器的
#from selenium.webdriver import ActionChains  # 破解滑动验证码的时候用的 可以拖动图片
from selenium.webdriver.common.by import By  # 按照什么方式查找，By.ID,By.CSS_SELECTOR
from selenium.webdriver.common.keys import Keys  # 键盘按键操作
from selenium.webdriver.support import expected_conditions as EC  # 和下面WebDriverWait一起用的
from selenium.webdriver.support.wait import WebDriverWait  # 等待页面加载某些元素
from selenium.webdriver.chrome.service import Service     # webdriver 服务，关闭浏览器后在关闭服务--》实现完全关闭

import time
import datetime
import os

import smtplib
from email.mime.text import MIMEText
from email.header import Header

# 类操作
class app:

    def __init__(self):
        self.east_url = "https://www.eastmoney.com/"

    # 打开webdriver服务和chrome浏览器
    def open_chrome(self):

        # 无窗口启动设置
        options = webdriver.ChromeOptions()
        options.add_argument('--headless') #无头启动，无窗口加载
        #options.add_argument('window-size=1920x3000') #指定浏览器分辨率
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument("service_args=['–ignore-ssl-errors=true', '–ssl-protocol=TLSv1']")
        options.add_argument('--disable-gpu') #不开启gpu加速
        options.add_argument('--hide-scrollbars') #隐藏滚动条, 应对一些特殊页面
        options.add_argument('blink-settings=imagesEnabled=false') #不加载图片, 提升速度
          
        # 东方财富网主页
        #east_url = "https://www.eastmoney.com/"

        # 开启webdriver服务
        c_service = Service('/usr/bin/chromedriver')
        c_service.command_line_args()
        c_service.start()

        try:
            # 打开浏览器
            driver = webdriver.Chrome(executable_path = "/usr/bin/chromedriver", options = options)
            driver.implicitly_wait(10)
            driver.get(self.east_url)

            #找到输入框
            input_tag = driver.find_element_by_id("code_suggest")

            # 进入所选股票页面
            # 如果本次不输入内容搜素，直接Enter进入后，搜素框ID="searchSuggest"
            # 如果本次输入内容搜素，Enter进入后，搜素框ID="search_key"
            # 保证多股票搜索，随意输入搜索内容进入
            input_tag.send_keys("大连圣亚")
            input_tag.send_keys(Keys.ENTER)

            #所有窗口
            all_handles = driver.window_handles
            #当前窗口
            east_window = driver.current_window_handle
            # 切换窗口
            for handle in all_handles:
                if handle != east_window:
                    #切换至另一窗口
                    driver.switch_to.window(handle)

        
        except:
            # 退出Chrome，然后在重新打开
            driver.quit()
            # 重新打开进入
            driver = webdriver.Chrome(executable_path = "/usr/bin/chromedriver", options = options)
            driver.implicitly_wait(10)
            driver.get(self.east_url)
            input_tag = driver.find_element_by_id("code_suggest")
            input_tag.send_keys("大连圣亚")
            input_tag.send_keys(Keys.ENTER)

            # 窗口切换
            all_handles = driver.window_handles
            east_window = driver.current_window_handle
            for handle in all_handles:
                if handle != east_window:
                    driver.switch_to.window(handle)

        finally:
            pass
        
        return (driver, c_service)

    def checkupdate(self, stocks):
        
        # 打开浏览器和webdriver服务
        driver_and_c_service = self.open_chrome()
        driver = driver_and_c_service[0]
        c_service = driver_and_c_service[1]

        # 接受信息的变量
        messages = ""

        # 对每一只股票的最新资讯和公告进行搜素
        for stock in stocks:

            try:

                # 获取单支股票的资讯和公告更新情况
                message = self.message_send(stock, self.get_message(driver, stock))

                # 如果有更新，统计更新信息
                if message != "":
                    messages = messages + message
                else:
                    pass

                # 获取一支股票资料后等10秒
                time.sleep(10)
            except:
                # 关闭浏览器
                driver.quit()
                # 关闭webdriver 服务，关闭进程
                time.sleep(2)
                c_service.stop()

                # 重新打开chrome和webdriver服务
                driver_and_c_service = self.open_chrome()
                driver = driver_and_c_service[0]
                c_service = driver_and_c_service[1]

                continue
                
            finally:
                pass

        # driver.close()无法关闭进程，使用driver.quit()
        # 本次全部股票资讯和公告全部搜素完毕后，关闭全部浏览器窗口
        driver.quit()    

        # 关闭webdriver 服务，关闭进程
        time.sleep(2)
        c_service.stop()  

        # 如果资讯和公告有更新，加上最后格式
        if messages != "":
            # messages 最后一行加上格式化*
            messages = messages + "★" * 19 + "\n" + "★" * 19 + "\n"
            #print(messages)
        else:
            pass

        # 将所有股票公告和资讯更新情况发送email
        self.email_send(messages)

    # 获取股票最新资讯和公告情况
    def get_message(self, driver, stock):    

        # 资讯板块查找是否有最新
                    
        print(stock, ", Searching now ......", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

        ####################################################
        # 抓取资讯内容
        # 等待搜素网页刷新出来
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "search_key")))

        #找到搜素页面的输入框
        input_search_tag = driver.find_element_by_id("search_key")

        # 清空输入框内容
        input_search_tag.clear()

        # 输入要搜素的股票，进入所选股票页面
        input_search_tag.send_keys(stock)
        input_search_tag.send_keys(Keys.ENTER)

        # 等待5秒
        time.sleep(5)

        # 等待资讯网页刷新出来
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.LINK_TEXT, "资讯")))

        # 进入资讯版块
        driver.find_element_by_link_text("资讯").click()

        # 等待news_item加载完成
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "news_item")))
        #driver.implicitly_wait(5)

        # 抓取news_item 元素
        news_list = driver.find_elements_by_class_name("news_item")

        # 新资讯列表
        news_new = []

        for news in news_list:
            # 每条资讯的发布日期，上市公司会当晚发出第二天的公告，发布时间为第二天的日期
            # 将资讯的时间的年、月、日按照str格式分隔
            news_str_date = news.find_element_by_class_name("news_item_time").get_attribute("textContent")[:10].split("-")
            # 把年月日转化为datetime格式的日期
            news_date = datetime.date(int(news_str_date[0]), int(news_str_date[1]), int(news_str_date[2]))
            
            # 今天日期,换成datetime处理， 用于比较时间先后，
            #today_date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            # 获取datetime格式的日期
            today_date = datetime.date.today()
            
            # 判断今天是否有新的资讯, 如果资讯的日期>=今天的日期，则有新公告        
            if news_date >= today_date:
                #print("今天有新的资讯！")
                # 获取新资讯的标题
                news_title = news.find_element_by_class_name("news_item_t").get_attribute("textContent")
                # 获取资讯内容快照,暂时不用
                #news_content = news.find_element_by_class_name("news_item_c").get_attribute("textContent")
                # 获取新资讯的连接
                #news_link = news.find_element_by_xpath("//a[@target='_blank']").get_attribute("href")       # xpath 方法
                news_link = news.find_element_by_class_name("news_item_url").get_attribute("textContent")    # 寻找元素方法
                #print("资讯标题：", news_title)
                #print("资讯内容：", news_content)
                #print("资讯地址：", news_link)

                # 写入内容中暂没包含 内容快照
                news_new.append([news_title, news_link])
            else:
                pass

        # 等待10秒
        time.sleep(10)

        ################################################
        # 抓取公告内容
        # 等待网页刷新出来
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.LINK_TEXT, "公告")))
        # 进入公告版块
        driver.find_element_by_link_text("公告").click()

        # 等待notice_item加载完成
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "notice_item")))
        #driver.implicitly_wait(5)

        # 抓取notice_item 元素
        notice_list = driver.find_elements_by_class_name("notice_item")

        # 新公告列表
        notice_new = []

        for notice in notice_list:
            # 每条公告的发布日期，上市公司会当晚发出第二天的公告，发布时间为第二天的日期
            # 将公告的时间的年、月、日按照str格式分隔
            notice_str_date = notice.find_element_by_class_name("notice_item_time").get_attribute("textContent")[:10].split("-")
            # 把年月日转化为datetime格式的日期
            notice_date = datetime.date(int(notice_str_date[0]), int(notice_str_date[1]), int(notice_str_date[2]))
            
            # 今天日期,换成datetime处理， 用于比较时间先后，上市公司会在当晚发布第二天的公告，且该公告的发布时间会是第二天的日期
            #today_date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            # 获取datetime格式的日期
            today_date = datetime.date.today()
            
            # 判断今天是否有新的公告, 如果公告的日期>=今天的日期，则有新公告        
            if notice_date >= today_date:
                #print("今天有新的公告了！")
                # 获取新资讯的标题
                notice_title = notice.find_element_by_class_name("notice_item_t").get_attribute("textContent")
                # 获取资讯快照，暂时不用
                #notice_content = notice.find_element_by_class_name("notice_item_c").get_attribute("textContent")
                # 获取新资讯的连接
                #news_link = news.find_element_by_xpath("//a[@target='_blank']").get_attribute("href")       # xpath 方法
                notice_link = notice.find_element_by_class_name("notice_item_link").get_attribute("textContent")    # 寻找元素方法

                # 将最新的资讯和公告写入列表
                notice_new.append([notice_title, notice_link])

            else:
                pass

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
        #messages = "hello world"

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
            receivers = ['8780037@qq.com', '68332309@qq.com', 'admin@pooper.tk']
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

        # 一直循环
        while True:

            # 从 name.txt 文件中读取需要获取信息的股票名称，以方面更改搜索股票的名称
            #stocks = ["大连圣亚", "捷捷微电", "当升科技"]

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
                # 每隔30分钟搜索一次
                time.sleep(1800)
                
# 主程序,运行
if __name__ == '__main__':
    
    app = app()

    app.main()