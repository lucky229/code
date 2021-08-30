#!/usr/bin/env python3
# -*- coding:UTF-8 -*-

import pymysql
import os, xlrd
import datetime

from WindPy import w

import smtplib
from email.mime.text import MIMEText
from email.header import Header


class Stock:

    # 对东方财富导出的数据整理
    def stockmsg(self, str_today):

        # 东方财富导出数据路径
        stocknum_path = "D:\\code\\stock\\report\\stockcode\\" + str_today + ".xls"

        # 存放数据的列表
        code_list = []

        # 判断文件是否存在
        if os.path.exists(stocknum_path):

            # 打开excel
            book = xlrd.open_workbook(stocknum_path)
            sh = book.sheet_by_index(0)

            #print("{0} {1} {2}".format(sh.name, sh.nrows, sh.ncols))

            # 获取各列对应的列号
            m = 0
            while m < sh.ncols:
                if sh.cell_value(0, m) == "代码":
                    col_code = m
                elif sh.cell_value(0, m) == "名称":
                    col_name = m
                elif sh.cell_value(0, m) == "所属行业":
                    col_hangye = m
                elif sh.cell_value(0, m) == "涨幅%":
                    col_rate_d = m
                elif sh.cell_value(0, m) == "今年涨幅%":
                    col_rate_thisyear = m
                elif sh.cell_value(0, m) == "250日涨幅":
                    col_rate_250d = m
                elif sh.cell_value(0, m) == "125日涨幅":
                    col_rate_125d = m
                elif sh.cell_value(0, m) == "65日涨幅":
                    col_rate_65d = m
                elif sh.cell_value(0, m) == "40日涨幅":
                    col_rate_40d = m
                elif sh.cell_value(0, m) == "22日涨幅":
                    col_rate_22d = m
                elif sh.cell_value(0, m) == "10日涨幅":
                    col_rate_10d = m
                elif sh.cell_value(0, m) == "5日涨幅":
                    col_rate_5d = m
                elif sh.cell_value(0, m) == "500日涨幅":
                    col_rate_500d = m
                elif sh.cell_value(0, m) == "750日涨幅":
                    col_rate_750d = m
                elif sh.cell_value(0, m) == "上市日期":
                    col_goday = m
                else:
                    pass

                m = m + 1
                
            # 循环，取出各股票数据
            i = 1
            while i < sh.nrows:

                # 股票代码
                stock_code = sh.cell_value(i, col_code)
                '''
                if stock_code[0] == "6":
                    stock_code = "SH" + stock_code
                else:
                    stock_code = "SZ" + stock_code
                '''
                # 股票名称
                stock_name = sh.cell_value(i, col_name)
                # 删除空格
                stock_name = stock_name.strip()

                # 股票行业
                stock_hangye = sh.cell_value(i, col_hangye)
                # 删除空格
                stock_hangye = stock_hangye.strip()

                # 股票上市日期
                stock_goday = sh.cell_value(i, col_goday)
                # 删除空格
                stock_goday = stock_goday.strip()

                # 一年，250交易日涨幅
                stock_rate_250d = sh.cell_value(i, col_rate_250d)
                # 如果为“ -”，改写为0
                stock_rate_250d = self.to0(stock_rate_250d)

                # 半年， 125交易日涨幅
                stock_rate_125d = sh.cell_value(i, col_rate_125d)
                stock_rate_125d = self.to0(stock_rate_125d)

                # 季度， 65个交易日
                stock_rate_65d = sh.cell_value(i, col_rate_65d)
                stock_rate_65d = self.to0(stock_rate_65d)

                # 2个月， 40个交易日
                stock_rate_40d = sh.cell_value(i, col_rate_40d)
                stock_rate_40d = self.to0(stock_rate_40d)

                # 1个月，22个交易日
                stock_rate_22d = sh.cell_value(i, col_rate_22d)
                stock_rate_22d = self.to0(stock_rate_22d)

                # 两周，10个交易日
                stock_rate_10d = sh.cell_value(i, col_rate_10d)
                stock_rate_10d = self.to0(stock_rate_10d)

                # 一周， 5个交易日
                stock_rate_5d = sh.cell_value(i, col_rate_5d)
                stock_rate_5d = self.to0(stock_rate_5d)

                # 当天涨幅
                stock_rate_d = sh.cell_value(i, col_rate_d)
                stock_rate_d = self.to0(stock_rate_d)

                # 当年涨幅
                stock_rate_thisyear = sh.cell_value(i, col_rate_thisyear)
                stock_rate_thisyear = self.to0(stock_rate_thisyear)

                # 两年涨幅
                stock_rate_500d = sh.cell_value(i, col_rate_500d)
                stock_rate_500d = self.to0(stock_rate_500d)

                # 三年涨幅
                stock_rate_750d = sh.cell_value(i, col_rate_750d)
                stock_rate_750d = self.to0(stock_rate_750d)

                # 单支股票的信息放入 code_list
                code_list.append([stock_code, stock_name, stock_hangye, stock_rate_250d, stock_rate_125d, \
                                stock_rate_65d, stock_rate_40d, stock_rate_22d, stock_rate_10d, \
                                stock_rate_5d, stock_rate_d, stock_rate_thisyear, stock_rate_500d, \
                                stock_rate_750d, stock_goday])
                i = i + 1

        # 没有文件            
        else:
            #print("今天的股票数据 %s 还没有导出！" % (self.str_today + ".xls"))

            pass
        
        return code_list

    # 将" —" 转换为 0.0, 专门在 stockmsg()中使用
    def to0(self, msg):

        if msg == " —":
            msg = 0.0
        else:
            pass

        return msg


    def get_name(self):
        text_path = "D:\\code\\name.txt"
        with open(text_path, "r", encoding='utf-8') as f:
            stocks = f.readlines()
            f.close()

        i = 0
        while i < len(stocks):
            stocks[i] = stocks[i].strip()
            i = i + 1
        print(stocks, type(stocks))




    def readexcel(self):


        path_excel = "D:\\code\\stock\\report\\stockcode\\aa.xls"

        with open(path_excel, "rb") as f:
            book = f.readlines()
            f.close()

        for ss in book:
            ss = str(ss.decode(encoding="gb2312"))
            #print(type(book), len(book))
            #print(ss)


            tt = ss.split("\t")
            for i in list(range(len(tt))):
                tt[i] = tt[i].strip()

            print(type(tt), len(tt))
            print(tt)

    def xlrdexcel(self):

        path_excel = "D:\\code\\stock\\report\\stockcode\\aa.xls"

        # 打开excel
        book = xlrd.open_workbook(path_excel)
        sh = book.sheet_by_index(0)

        print(type(sh), len(sh))


    def readtxt(self):


        path_excel = "D:\\code\\stock\\report\\stockcode\\bb..txt"

        with open(path_excel, "rb") as f:
            book = f.readlines()
            f.close()

        for ss in book:
            ss = str(ss.decode(encoding="gb2312"))
            #print(type(book), len(book))
            #print(ss)


            tt = ss.split("\t")
            for i in list(range(len(tt))):
                tt[i] = tt[i].strip()

            print(type(tt), len(tt))
            print(tt)


if __name__ == '__main__':
    app = Stock()
    app.readtxt()
    #app.readexcel()
    #app.xlrdexcel()