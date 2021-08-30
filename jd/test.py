#!/usr/bin/env python3
# -*- coding:UTF-8 -*-

import time
import cv2
import random
import openpyxl
from urllib import request
from selenium import webdriver
import numpy as np
from selenium.webdriver.common.action_chains import ActionChains
 
#chromdriver下载地址http://npm.taobao.org/mirrors/chromedriver/
#下载好了需要设置好PATH
browser=webdriver.Chrome(executable_path="D:\\Python\\Python38\\Scripts\\chromedriver.exe")
 
def login_myhome():
    handle1=browser.current_window_handle
    _xpath=r"//a[contains(@href,'home')]"
    browser.find_element_by_xpath(_xpath).click()
    time.sleep(2)
 
    handles=browser.window_handles
    print(handles)
    for newhandle in handles:
        if newhandle != handle1:
            browser.switch_to.window(newhandle)
    print(browser.current_window_handle)
 
    #TODO:login my jingbean home
    _xpath=r"//a[contains(@href,'myJingBean')]"
    browser.find_element_by_xpath(_xpath).click()
    time.sleep(2)
    handle2=browser.current_window_handle
    #TODO:login jd vip home
    _xpath=r"//li[@class='li-item2']/div/a[contains(@class,'c-btn')]"
    browser.find_element_by_xpath(_xpath).click()
    time.sleep(2)
    #TODO:switch handles
    handles=browser.window_handles
    print(handles)
    for newhandle in handles:
        if newhandle != handle1 and newhandle!=handle2:
            browser.switch_to.window(newhandle)
    print(browser.current_window_handle)
    #TODO: get bean
    _xpath=r"//span[@class='icon-sign']"
    browser.find_element_by_xpath(_xpath).click()
    time.sleep(2)
 
    browser.quit()
 
 
def move(btn,x,y):
    distance=y
    has_gone_dist=0
    remaining_dist=y
    print('btn:')
    print(btn)
    #获取滑块
    element=browser.find_element_by_xpath(btn)
    ActionChains(browser).click_and_hold(on_element=element).perform()
    time.sleep(0.5)
 
    while remaining_dist>0:
        ratio=remaining_dist / distance
        if ratio<0.1:
            #结束阶段移动较慢
            span=random.randint(3,5)
        elif ratio>0.9:
            #开始阶段移动较慢
            span = random.randint(5,8)
        else:
            #中间部分移动较快
            span = random.randint(15, 20)
        #由于京东验证机制比较严格，模仿手动移动，每次移动上下有5像素的偏差
        ActionChains(browser).move_by_offset(span,random.randint(-5,5)).perform()
        remaining_dist-=span
        has_gone_dist+=span
        time.sleep(random.randint(5,20)/100)
 
    print(remaining_dist)
    #回移一下
    ActionChains(browser).move_by_offset(remaining_dist,random.randint(-5,5)).perform()
    #松下按键
    ActionChains(browser).release(on_element=element).perform()
    time.sleep(2)
 
def getPic():
    #取登录图片的大图
    img1=r'//div/div[@class="JDJRV-bigimg"]/img'
    #取登录图片的小图
    img2=r'//div/div[@class="JDJRV-smallimg"]/img'
    bigimg=browser.find_element_by_xpath(img1).get_attribute("src")
    smallimg = browser.find_element_by_xpath(img2).get_attribute("src")
 
    #下载两个图片到本地,是两张彩色的原图
    request.urlretrieve(bigimg,'backimg')
    request.urlretrieve(smallimg,'slideimg')
    #获取图片并做灰化
    template=cv2.imread('backimg',0)
    block=cv2.imread('slideimg',0)
    #将灰化的图片进行保存
    blockName='block.jpg'
    templateName='template.jpg'
    cv2.imwrite(blockName,block)
    cv2.imwrite(templateName, template)
    #对小滑块又进行了一次灰化处理
    block=cv2.imread(blockName)
    block=cv2.cvtColor(block,cv2.COLOR_BGR2GRAY)
    block=abs(255-block)
    cv2.imwrite(blockName,block)
    #将进终灰化过的图片读出来
    block=cv2.imread(blockName)
    template=cv2.imread(templateName)
 
    #获取偏移量
    #result返回block在template的位置，返回一个数组
    result=cv2.matchTemplate(block,template,cv2.TM_CCOEFF_NORMED)
    #print(result)
    x,y=np.unravel_index(result.argmax(),result.shape)
 
    print("x is {} y is {}".format(x,y))
 
    btn='//div[@class="JDJRV-slide-inner JDJRV-slide-btn"]'
    move(btn,x,int(y / 1.3))
 
def getpersoninfo(channel):
    #读取本地存放url,帐号，密码和文件。
    wb=openpyxl.load_workbook('personinfo.xlsx')
    sheet=wb[channel]
    url=sheet['A2'].value
    username=sheet['B2'].value
    pwd=sheet['C2'].value
    return url,username,pwd
 
def login():
    #channel='jd'
    #info=getpersoninfo(channel)
    #url=info[0]
    #username=info[1]
    #password=info[2]
    url="https://www.jd.com"
    username= "username"
    password= "password"
    browser.get(url)
    browser.maximize_window()
    link_loin=browser.find_element_by_link_text('你好，请登录')
    link_loin.click()
    time.sleep(1)
    account_login=browser.find_element_by_link_text('账户登录')
    account_login.click()
    time.sleep(1)
    user=browser.find_element_by_id('loginname')
    user.clear()
    pwd=browser.find_element_by_id('nloginpwd')
    pwd.clear()
    user.send_keys(username)
    pwd.send_keys(password)
    time.sleep(1)
    submit=browser.find_element_by_id('loginsubmit')
    submit.click()
    time.sleep(2)
 
def main():
    #TODO: login url
    login()
    #TODO: getPic and slider identify
    while True:
        try:
            getPic()
            #每次滑块验证等待5秒
            time.sleep(5)
        except:
            print("登入成功")
            break
    time.sleep(2)
 
    login_myhome()
 
 
if __name__=='__main__':
    main()