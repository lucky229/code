#!/usr/bin/env python3
# -*- coding:UTF-8 -*-

# 20210813更新，从name.txt中读取需要搜索公司的名称
# 主要用于从中国裁判文书网搜索最新裁判文书
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
        self.court_url = "https://wenshu.court.gov.cn/"

    # 打开webdriver服务和chrome浏览器
    def getCaseMsg(self,name):

        # 无窗口启动设置
        options = webdriver.ChromeOptions()
        options.add_argument('--headless') #无头启动，无窗口加载
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        #options.add_argument("service_args=['–ignore-ssl-errors=true', '–ssl-protocol=TLSv1']")
        options.add_argument('--disable-gpu') #不开启gpu加速
        #options.add_argument('--hide-scrollbars') #隐藏滚动条, 应对一些特殊页面
        #options.add_argument('blink-settings=imagesEnabled=false') #不加载图片, 提升速度
        
        # driver_path 路径  
        driver_path = '/usr/bin/chromedriver'
        #driver_path = "D:\\Python\\Python38\\Scripts\\chromedriver.exe"

        # 开启webdriver服务
        c_service = Service(driver_path)
        c_service.command_line_args()
        c_service.start()

        try:
            # 打开浏览器
            driver = webdriver.Chrome(executable_path = driver_path, options = options)
            driver.implicitly_wait(10)
            driver.get(self.court_url)

            # 等待网页刷新出来
            time.sleep(10)

            #找到输入框
            login_tag = driver.find_element_by_xpath("//li[@id='loginLi']")

            login_or_not = login_tag.get_attribute("textContent")

            # 登录并开始搜索信息
            if login_or_not.split()[0] == "登录":
                login_tag.click()
                time.sleep(10)
                # 切换至iframe
                iframe = driver.find_elements_by_tag_name('iframe')

                # 如果iframe 没有加载出来，刷新直到加载出来
                while iframe == None:
                    driver.refresh()
                    time.sleep(10)
                    iframe = driver.find_elements_by_tag_name('iframe')


                driver.switch_to.frame(iframe[0])
                
                time.sleep(5)

                name_tag = driver.find_element_by_class_name("phone-number-input")
                name_tag.send_keys("18183137718")
                time.sleep(5)
                pass_tag = driver.find_element_by_xpath("//div/input[@type='password']")
                pass_tag.send_keys("CNcq@20151111")
                time.sleep(5)
                commit_button = driver.find_element_by_class_name("login-button-container")
                commit_button.click()
                time.sleep(5)

                # 切换回主页面
                driver.switch_to.default_content()

            else:
                time.sleep(5)

            # 搜索窗口
            input_search_tag = driver.find_element_by_class_name("search-inp")
            # 输入搜索内容
            input_search_tag.send_keys(name)
            time.sleep(5)
            # 点击搜索按钮
            driver.find_element_by_class_name("search-click").click()
            time.sleep(10)

            court_list = driver.find_elements_by_class_name("LM_list")

            court_text = ""
            for court in court_list:
                court_date_list = court.find_element_by_class_name("cprq").get_attribute("textContent").split("-")
                # 文书发布时间
                court_date = datetime.date(int(court_date_list[0]), int(court_date_list[1]), int(court_date_list[2]))
                # 今天的前一天，鉴于发布时间的不确定性，以前一天的日期为判断依据
                yesterday_bef = datetime.date.today() + datetime.timedelta(days=(-1))

                if court_date >= yesterday_bef:
                    caseName = court.find_element_by_class_name("caseName").get_attribute("textContent")
                    court_text = court_text + "案件名称：" + caseName + "\n\n"
                    
                    slfyName = court.find_element_by_class_name("slfyName").get_attribute("textContent")
                    court_text = court_text + "审判法院：" + slfyName + "\n"

                    ah = court.find_element_by_class_name("ah").get_attribute("textContent")
                    court_text = court_text + "案件号：" + ah + "\n"

                    cprq = court.find_element_by_class_name("cprq").get_attribute("textContent")
                    court_text = court_text + "日期：" + cprq + "\n\n"

                    cply = court.find_elements_by_class_name("list_reason").get_attribute("textContent")
                    court_text = court_text + "裁判理由：" + cply + "\n\n\n\n"

                    court_text = court_text + "★"*30 + "\n\n\n"

                    # 下载裁判文书
                    court.find_element_by_class_name("a_xz").click()


                else:
                    pass
        
        
        except:
            # 退出Chrome，然后在重新打开
            driver.quit()

            # 打开浏览器
            driver = webdriver.Chrome(executable_path = driver_path, options = options)
            driver.implicitly_wait(10)
            driver.get(self.court_url)

            # 等待网页刷新出来
            time.sleep(10)

            #找到输入框
            login_tag = driver.find_element_by_xpath("//li[@id='loginLi']")

            login_or_not = login_tag.get_attribute("textContent")

            # 登录并开始搜索信息
            if login_or_not.split()[0] == "登录":
                login_tag.click()
                time.sleep(10)
                # 切换至iframe
                iframe = driver.find_elements_by_tag_name('iframe')

                # 如果iframe 没有加载出来，刷新直到加载出来
                while iframe == None:
                    driver.refresh()
                    time.sleep(10)
                    iframe = driver.find_elements_by_tag_name('iframe')


                driver.switch_to.frame(iframe[0])
                
                time.sleep(5)

                name_tag = driver.find_element_by_class_name("phone-number-input")
                name_tag.send_keys("18183137718")
                time.sleep(5)
                pass_tag = driver.find_element_by_xpath("//div/input[@type='password']")
                pass_tag.send_keys("CNcq@20151111")
                time.sleep(5)
                commit_button = driver.find_element_by_class_name("login-button-container")
                commit_button.click()
                time.sleep(5)

                # 切换回主页面
                driver.switch_to.default_content()

            else:
                time.sleep(5)

            # 搜索窗口
            input_search_tag = driver.find_element_by_class_name("search-inp")
            # 输入搜索内容
            input_search_tag.send_keys(name)
            time.sleep(5)
            # 点击搜索按钮
            driver.find_element_by_class_name("search-click").click()
            time.sleep(10)

            court_list = driver.find_elements_by_class_name("LM_list")

            court_text = ""
            for court in court_list:
                court_date_list = court.find_element_by_class_name("cprq").get_attribute("textContent").split("-")
                # 文书发布时间
                court_date = datetime.date(int(court_date_list[0]), int(court_date_list[1]), int(court_date_list[2]))
                # 今天的前一天，鉴于发布时间的不确定性，以前一天的日期为判断依据
                yesterday_bef = datetime.date.today() + datetime.timedelta(days=(-1))

                if court_date >= yesterday_bef:
                    caseName = court.find_element_by_class_name("caseName").get_attribute("textContent")
                    court_text = court_text + "案件名称：" + caseName + "\n\n"
                    
                    slfyName = court.find_element_by_class_name("slfyName").get_attribute("textContent")
                    court_text = court_text + "审判法院：" + slfyName + "\n"

                    ah = court.find_element_by_class_name("ah").get_attribute("textContent")
                    court_text = court_text + "案件号：" + ah + "\n"

                    cprq = court.find_element_by_class_name("cprq").get_attribute("textContent")
                    court_text = court_text + "日期：" + cprq + "\n\n"

                    cply = court.find_elements_by_class_name("list_reason").get_attribute("textContent")
                    court_text = court_text + "裁判理由：" + cply + "\n\n\n\n"

                    court_text = court_text + "★"*30 + "\n\n\n"

                    # 下载裁判文书
                    court.find_element_by_class_name("a_xz").click()


                else:
                    pass

        finally:
            # 关闭浏览器和服务
            driver.quit()
            c_service.stop()
        
        return court_text


    # 发送邮件
    def email_send(self, messages):
        
        # 发送邮件
        # 发送邮箱服务器
        smtpserver = 'mail.pooper.tk'
        # 发送邮箱用户/密码
        user = 'admin'
        password = '123456'
        # 发送邮箱
        sender = 'admin@pooper.tk'
        # 接收邮箱
        receivers = ['admin@pooper.tk']
        # 发送邮件主题
        subject = '关注公司的诉讼情况-' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

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
            

    def main(self):

        print("I am looking for the courts - ", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))


        # name.txt文件地址，windows测试地址
        #text_path = "D:\\code\\wenshu\\name.txt"

        # ubuntu20.04 中 name.txt 路径, name.txt中一行写一个公司名称，多个多行写，每行只写公司名称，不加其他内容
        text_path = "/home/wenshu/name.txt"

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

        case_text = ""
        for name in stocks:
            msg = self.getCaseMsg(name)
            if msg == "":
                pass
            else:
                case_text = case_text + name + "  的最新案件情况如下：\n\n\n" + msg

        if case_text == "":
            print("There are no case upgrade - ", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        else:
            self.email_send(case_text)

                
# 主程序,运行
if __name__ == '__main__':
    
    app = app()

    app.main()