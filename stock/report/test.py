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

    # 计算出入的多少个交易日前的日期
    def beforeday(daydelta=1):

        # 先定义bf_day 为当天
        bf_day = datetime.date.today()

        # 需要多少交易以前，循环多少次
        for i in list(range(daydelta)):

            # 星期六是5，星期日是6
            while True:
                # 前一天
                bf_day = bf_day + datetime.timedelta(days = (-1))
                
                # 判断是否假期，是假期继续循环，不是跳出while
                if bf_day.weekday() in [5, 6] or bf_day.weekday() in self.holiday:
                    pass
                else:
                    break
 
        # 返回要求的日期，datetime.date 格式
        return bf_day

    def time_str():
        now_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(now_time)
        print(datetime.date.today())

    def codetest(self):
        # 打开数据库连接
        db = pymysql.connect(host="localhost", user="root", password="123456",database="test", charset="utf8")
             
        # 使用 cursor() 方法创建一个游标对象 cursor
        cursor = db.cursor()

        table_name = "stock20210803"

        # 一年新高
        order_up250d = """select (@rownum:=@rownum+1) as num, code, name, hangye, rate_22d, rate_125d, rate_250d from(select * from stock20210806 
                        where rate_250d >0 and rate_250d!=rate_125d and rate_125d>rate_250d and rate_65d>rate_250d 
                        and rate_40d>rate_250d and rate_22d>rate_250d)as a, (select @rownum:=0) as b order by rate_22d desc;"""

        cursor.execute(order_up250d)

        data_stock = cursor.fetchall()

        tdx_up = ""
        for i in list(range(len(data_stock))):

            # 股票代码
            if data_stock[i][1][0] == "6":
                stock_code = "sh" + data_stock[i][1]
                tdx_code = "1" + data_stock[i][1]
            else:
                stock_code = "sz" + data_stock[i][1]
                tdx_code = "0" + data_stock[i][1]

            # 通达信板块
            tdx_up = tdx_up + "\n" + tdx_code

        path_tdx_up250d = "D:\\zd_ciccwm\\T0002\\blocknew\\TEST.blk"
        # 将筛选的股票写入通达信软件的 test 板块，可以直接在通达信软件中查看 up 板块股票
        with open(path_tdx_up250d, "w", encoding="utf-8") as f:
            f.write(tdx_up)
            f.close()

    # 行业排名情况统计
    def hangyeorder(self):
        # 打开数据库连接
        db = pymysql.connect(host="localhost", user="root", password="123456",database="test", charset="utf8")
             
        # 使用 cursor() 方法创建一个游标对象 cursor
        cursor = db.cursor()

        table_name = "stock20210810"
        # str_day 格式改为xxxx年xx月xx日
        #str_day = self.str_today[:4] + "年" + self.str_today[4:6] + "月" + self.str_today[-2:]+ "日"
        str_day = "2021年8月10日"

        somedays = ["rate_d", "rate_5d", "rate_10d", "rate_22d", "rate_40d", "rate_65d", "rate_125d", "rate_250d"]
        top = 100

        # html代码
        table_hangyeorder = """<h4>∷∷▶在 {0} 不同阶段涨幅前{1}的股票分析</h4><p>股票行业情况分析。具体情况见下表：</p><table border="1"><tr><th>区间</th>
                        <th>第一名</th><th>第二名</th><th>第三名</th><th>第四名</th><th>第五名</th></tr>
                        """.format(str_day, top)
        # HTML表格代码
        table_td = """<tr><td>{0}</td><td>{1}</td><td>{2}</td><td>{3}</td><td>{4}</td><td>{5}</td></tr>"""

        data_hangyes = []
        for someday in somedays:
            # 行业排名分析
            order_hangye = """select * from
                            (select hangye, count(*)as num_st from 
                            (select * from {0} order by {1} desc limit {2}) as a
                            group by hangye) as b order by b.num_st desc limit 5;""".format(table_name, someday, top)

            cursor.execute(order_hangye)
            data_hangye = cursor.fetchall()

            table_hangyeorder = table_hangyeorder + table_td.format(someday, data_hangye[0][0] + "(" + str(data_hangye[0][1])+")", \
                            data_hangye[1][0] + "(" + str(data_hangye[1][1])+")", data_hangye[2][0] + "(" + str(data_hangye[2][1])+")",\
                            data_hangye[3][0] + "(" + str(data_hangye[3][1])+")", data_hangye[4][0] + "(" + str(data_hangye[4][1])+")",)

        table_hangyeorder = table_hangyeorder + "</table>" + "\n"

        #print(table_hangyeorder)
        return table_hangyeorder


    def test(self):
        # 打开数据库连接
        db = pymysql.connect(host="localhost", user="root", password="123456",database="test", charset="utf8")
             
        # 使用 cursor() 方法创建一个游标对象 cursor
        cursor = db.cursor()

        table_name = "stock20210807"
        stock_list = self.stockmsg("20210807")

        # 更新表格数据命令
        order_update = """UPDATE %s SET name = '%s', hangye = '%s', rate_250d = %s, rate_125d = %s, rate_65d = %s, 
                rate_40d = %s, rate_22d = %s, rate_10d = %s, rate_5d = %s, rate_d = %s, rate_thisyear = %s, 
                rate_500d = %s, rate_750d = %s, goday = '%s' where code = '%s';"""

        # 在表格中出入数据
        order_insert = "INSERT INTO %s"%table_name + """(code, name, hangye, rate_250d, rate_125d, rate_65d,
                rate_40d, rate_22d, rate_10d, rate_5d, rate_d, rate_thisyear, rate_500d, rate_750d, 
                goday) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"""

        # 一年新高
        order_rownum = """select (@rownum:=@rownum+1) as num, code, name, hangye, rate_22d, rate_125d, rate_250d from(select * from stock20210806 
                        where rate_250d >0 and rate_250d!=rate_125d and rate_125d>rate_250d and rate_65d>rate_250d 
                        and rate_40d>rate_250d and rate_22d>rate_250d)as a, (select @rownum:=0) as b order by rate_22d desc;"""

        # 用证券代码检查是否包含数据行
        order_check = """SELECT code, name from %s where code = %s"""

        # 检车是插入数据还是更新数据，主要为不重复插入数据
        for stockmsg in stock_list:

            # 执行检查命令
            cursor.execute(order_check % (table_name, stockmsg[0]))
            #print(cursor.fetchall(), type(cursor.fetchall()), len(cursor.fetchall()))

            if cursor.fetchall() == ():
                
                # 执行插入命令
                cursor.execute(order_insert, stockmsg)

            else:
                # 执行更新命令
                stockmsg.append(stockmsg[0])
                stockmsg[0] = table_name

                #print(stockmsg)
                cursor.execute(order_update % tuple(stockmsg))
            
            # 提交
            db.commit()

        # 关闭光标对象
        cursor.close()
         
        # 关闭数据库连接
        db.close()





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

    def addrownum(self):

        # 增加自增行序号
        order_rownum = """select (@rownum := @rownum + 1) as line, code from(select * from 
                        (select * from stock20210730 order by rate_250d desc limit 600)as a where rate_250d>500) as b, 
                        (select @rownum:=0) r;"""

        # 这种表达和上面表达结果一直，但是更简洁，注意where 条件位置，@rownum:=0 放的位置和表达方式，与前面的语句用"，"隔开
        order_rownum_else = """select (@rownum := @rownum + 1) as line, a.* from 
                            (select * from stock20210730 order by rate_250d desc limit 600)as a, 
                            (select @rownum:=0) as r where rate_250d>500;"""

        order_100 = """select b.num_new from (select (@rownum:=@rownum+1) as num_new,code, name, hangye from stock20210802, 
                    (select @rownum:=0)as a order by rate_250d desc limit 100)as b where code="688793";"""

        """select d.num_new from (select (@rownum:=@rownum+1) as num_new, b.code, b.name, b.hangye from(select * from
                        (select * from stock20210802 order by rate_250d desc limit 500) as a
                        where rate_125d > 50 and rate_22d > 30 and rate_250d != rate_125d) as b, 
                    (select @rownum:=0)as c order by rate_250d desc limit 100)as d where code="002192";

        
            select c.num_new from (select (@rownum:=@rownum+1) as num_new, b.name, b.code from (select * from
                        (select * from stock20210802 order by rate_250d desc limit 500) as a
                        where rate_125d > 50 and rate_22d > 30 and rate_250d != rate_125d) as b,
                        (select @rownum:=0) as d order by rate_22d desc limit 100)as c where code = "002192";

            select c.num_new from (select (@rownum:=@rownum+1) as num_new, b.name, b.code from (select * from
                                (select * from stock20210802 order by rate_250d desc limit 200) as a
                                where rate_125d > 50 and rate_22d > 30 and rate_250d != rate_125d) as b,
                                (select @rownum:=0) as d order by rate_22d desc limit 100) as c where code="002176";


        """

    def email_send(self, messages):
        # message 邮件发送的信息
        
        # 发送邮箱服务器
        smtpserver = 'mail.pooper.tk'
        # 发送邮箱用户/密码
        user = 'admin'
        password = '123456'
        # 发送邮箱
        sender = 'admin@pooper.tk'
        # 接收邮箱
        receivers = ['8780037@qq.com',]
        # 发送邮件主题
        subject = '股票分析-' + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # 编写HTML类型的邮件正文
        msg = MIMEText(messages,'html','utf-8')
        msg['Subject'] = Header(subject, 'utf-8')
        msg['From'] = 'admin@pooper.tk<admin@pooper.tk>'
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
    app = Stock()
    app.test()