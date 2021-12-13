#!/usr/bin/env python3
# -*- coding:UTF-8 -*-

########################################################################
# 主要对年、半年、季度、2个月、1个月、1周和当天不同周期股票涨幅排前300的进行分析
# 排行股票数据来源于 http://www.iwencai.com/unifiedwap/home/stock
# 股票行业分类来源于wind分类
# 主要分析内容：1、每个周期涨幅前100的主要行业排名；
#              2、排名上涨幅度情况；
#
# Author: zzg
# Version: V1.0
# Date: 2021.7.27
#
########################################################################

import xlrd       # 读取excel表格
import pymysql       # 操作数据库
import datetime
import os

import smtplib
from email.mime.text import MIMEText
from email.header import Header

# 创建股票分析的类
class StockAnalysis:

    def __init__(self):

        # 假期，除周六和周日外的非交易日
        # 2021年11月18日没有导出数据，按节假日处理
        self.holiday = [datetime.date(2021, 9, 20), datetime.date(2021, 9, 21), datetime.date(2021, 10, 1), \
                        datetime.date(2021, 10, 4), datetime.date(2021, 10, 5), datetime.date(2021, 10, 6), \
                        datetime.date(2021, 10, 7), datetime.date(2021, 11, 18), \
                        # 2022年法定节假日
                        datetime.date(2022, 1, 3), datetime.date(2022, 1, 31), datetime.date(2022, 2, 1), \
                        datetime.date(2022, 2, 2), datetime.date(2022, 2, 3), datetime.date(2022, 2, 4), \
                        datetime.date(2022, 4, 4), datetime.date(2022, 4, 5), datetime.date(2022, 5, 2), \
                        datetime.date(2022, 5, 3), datetime.date(2022, 5, 4), datetime.date(2022, 6, 3), \
                        datetime.date(2022, 9, 12), datetime.date(2022, 10, 3), datetime.date(2022, 10, 4), \
                        datetime.date(2022, 10, 5), datetime.date(2022, 10, 6), datetime.date(2022, 10, 7)]
        # 创建统计区间变量和 表述的字典
        self.dic_day = {"rate_d":"当天", "rate_5d":"前 5个 交易日", "rate_10d":"前 10个 交易日", "rate_22d":"前 22个 交易日", \
                    "rate_40d":"前 40个 交易日", "rate_65d":"前 65个 交易日", "rate_125d":"前 125个 交易日", "rate_250d":"前 250个 交易日"}
        # 当天日期转成str
        #self.str_today = self.beforeday().strftime("%Y%m%d")   # 测试用上个交易日
        self.str_today = self.tradingday().strftime("%Y%m%d")
        self.table_name = "stock" + self.str_today
        self.somedays = ["rate_d", "rate_5d", "rate_10d", "rate_22d", "rate_40d", "rate_65d", "rate_125d", "rate_250d"]
        self.top = 100

    # 数据可以连接和关闭
    def operate_sql(self):

        # 打开数据库连接
        db = pymysql.connect(host="localhost", user="root", password="123456",database="stock", charset="utf8")

        # ubuntu 中打开数据库连接
        #db = pymysql.connect(host="localhost", user="root", password="1029384756",database="stock", charset="utf8")
             
        # 使用 cursor() 方法创建一个游标对象 cursor
        cursor = db.cursor()

        #try:
        # 数据库的操作，
        self.insertmsg_sql(self.table_name, self.stockmsg(self.str_today), db, cursor)

        
        con_hangye = self.look(db, cursor, self.table_name, self.somedays, self.top)
        con_hangyeroder = self.hangyeorder(db, cursor, self.table_name, self.somedays)
        con_stock = self.stockup(db, cursor, self.table_name)
        con = self.content_html(con_hangyeroder + con_hangye + con_stock)

        self.email_send(con)

        # 测试输出
        path_html = "D:\\code\\stock\\stockweb\\stock" + datetime.datetime.now().strftime("%Y-%m-%d %H%M%S") + ".html"
        with open(path_html, "w", encoding='utf-8') as f:
            f.write(con)
            f.close()
        
        #except:
        #    print("程序出差，请检查后再试！", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))


        # 关闭光标对象
        cursor.close()
         
        # 关闭数据库连接
        db.close()
        print("股票分析报告已生成，欢迎查阅！（‐＾▽＾‐）", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    # 创建数据表，并插入或更新数据表信息
    def insertmsg_sql(self, table_name, stock_list, db, cursor):
        # stock_list 为股票信息列表； db 数据库连接； cursor 光标对象

        # 先判断今天的数据是否导出
        if stock_list == []:
            #print("暂无今天的股票数据 %s ，请导出后再试！" % (self.str_today + ".xls"), \
            #    datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            pass

        else:

            # 表格名称
            #table_name = self.table_name

            # 删除数据表再重新创建
            order_drop = """DROP TABLE IF EXISTS %s""" % table_name
            cursor.execute(order_drop)

            # 创建数据表格，表头包括：代码，名称，行业，250/125/65/40/22/10/5个交易日涨幅，及当天和当年涨幅，其他
            sql = """CREATE TABLE IF NOT EXISTS %s(num int(10) primary key auto_increment,
                                                code varchar(100), 
                                                name varchar(100), 
                                                hangye varchar(100),
                                                rate_250d float,
                                                rate_125d float,
                                                rate_65d float,
                                                rate_40d float,
                                                rate_22d float,
                                                rate_10d float,
                                                rate_5d float,
                                                rate_d float,
                                                rate_thisyear float,
                                                rate_500d float,
                                                rate_750d float,
                                                goday varchar(100),
                                                else_msg varchar(100)
                                                )ENGINE=innodb DEFAULT CHARSET=utf8;""" % table_name

            # 使用 execute()  方法执行 SQL 查询
            cursor.execute(sql)

            #data = [['001', 'aa', 'bb', 'dsf', 0.1, 0.2, 0.30], ['002', 'bb', 'ds', 'da', 0.11, 0.22, 0.33]]
            
            # 在表格中出入数据
            order_insert = "INSERT INTO %s"%table_name + """(code, name, hangye, rate_250d, rate_125d, rate_65d,
                    rate_40d, rate_22d, rate_10d, rate_5d, rate_d, rate_thisyear, rate_500d, rate_750d, 
                    goday) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"""

            # 更新表格数据命令
            order_update = """UPDATE %s SET name = '%s', hangye = '%s', rate_250d = %s, rate_125d = %s, rate_65d = %s, 
                    rate_40d = %s, rate_22d = %s, rate_10d = %s, rate_5d = %s, rate_d = %s, rate_thisyear = %s, 
                    rate_500d = %s, rate_750d = %s, goday = '%s' where code = '%s';"""

            # 用证券代码检查是否包含数据行
            order_check = """SELECT code, name from %s where code = %s"""

            # 一句写入数据库，且效率高，但无法判断是否有重复
            #cursor.executemany(order_insert, stock_list)

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
            print("暂无 %s 的股票数据，请导出后再试！" % (str_today + ".xls"), \
                datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

       
        return code_list

    # 将" —" 转换为 0.0, 专门在 stockmsg()中使用
    def to0(self, msg):

        if msg == " —":
            msg = 0.0
        else:
            pass

        return msg

    # 数据排列分组，统计数量，并构造html的table代码
    def look(self, db, cursor, table_name, somedays, top):
        # db 数据库连接； cursor 光标对象； tablename 表格名称； someday 股票统计的区间; top 排名前多少位

        # str_day 格式改为xxxx年xx月xx日
        str_day = self.str_today[:4] + "年" + self.str_today[4:6] + "月" + self.str_today[-2:]+ "日"

        table_hangye_all = ""
        # 各阶段涨幅行业前五名行业的明细
        for someday in somedays:
            # 统计前前 top 名行业排前五的行业情况
            order_looks = """select * from
                            (select hangye, count(*)as num_st from 
                            (select * from {0} order by {1} desc limit {2}) as a
                            group by hangye) as b order by b.num_st desc limit 5;""".format(table_name, someday, top)

            # 查询行业前100范围内，单个行业包含哪些股票
            order_look_stock = """select name, code, {0} from 
                                (select * from {1} order by {0} desc limit {2})as a
                                where hangye="{3}";"""

            # 涨幅前的股票
            cursor.execute(order_looks)
            get_hangey = cursor.fetchall()

            # html代码
            table_hangye = """<h4>∷∷▶在 {0} {1}涨幅前{2}的股票分析</h4><p>股票行业情况分析：此阶段股票涨幅靠前五个行业分别为：
                            {3}, {4}, {5}, {6}, {7}。具体情况见下表：</p><table border="1"><tr><th>序号</th>
                            <th>行业</th><th>股票数量</th><th>股票明细</th></tr>
                            """.format(str_day, self.dic_day[someday], top, get_hangey[0][0], get_hangey[1][0], \
                                get_hangey[2][0], get_hangey[3][0], get_hangey[4][0],)
            # HTML表格代码
            table_td = """<tr><td>{0}</td><td>{1}</td><td>{2}</td><td>{3}</td></tr>"""

            # 循环取出前五个行业的股票明细
            for i in list(range(len(get_hangey))):
                
                # 每个行业的的股票           
                cursor.execute(order_look_stock.format(someday, table_name, top, get_hangey[i][0]))
                get_hangey_st = cursor.fetchall()

                # 存放取出的股票
                st_mx = ""
                for m in list(range(len(get_hangey_st))):

                    # 在股票名称上添加超链接
                    # 股票代码
                    if get_hangey_st[m][1][0] == "6":
                        stock_code = "sh" + get_hangey_st[m][1]
                    else:
                        stock_code = "sz" + get_hangey_st[m][1]

                    stock_link = "http://quote.eastmoney.com/" + stock_code + ".html"
                    name_link = "<a href='{0}'>{1}</a>".format(stock_link, get_hangey_st[m][0])

                    # 全部股票已 "，"隔开
                    if m != len(get_hangey_st) - 1:
                        st_mx = st_mx + name_link + "(" + str(get_hangey_st[m][2]) + "%)" + ", "
                    # 最后一只股票后面不加 "，"
                    else:
                        st_mx = st_mx + name_link + "(" + str(get_hangey_st[m][2]) + "%)"

                # html 表格代码
                table_hangye = table_hangye + table_td.format(i + 1, get_hangey[i][0], get_hangey[i][1], st_mx)
                table_hangye = table_hangye + "\n"

            # 表格结束
            table_hangye = table_hangye + "</table>" + "\n"
            #print(table_hangye)

            table_hangye_all = table_hangye_all + table_hangye

        # 提交
        db.commit()

        return table_hangye_all

    # 股票涨幅行业分析，并构造行业分析的html代码
    def hangyefenxi(self, db, cursor, table_name, someday, top):

        # 行业分析统计的几个阶段
        # "rate_d", "rate_5d", "rate_10d", "rate_22d", "rate_40d", "rate_65d", "rate_125d", "rate_250d"
        day_hangye = ["rate_d", "rate_5d", "rate_22d", "rate_40d", "rate_65d", "rate_125d", "rate_250d"]

        # 统计前前100名行业排前五的行业情况
        order_looks = """select * from
                        (select hangye, count(*)as num_st from 
                        (select * from {0} order by {1} desc limit {2}) as a
                        group by hangye) as b order by b.num_st desc limit 5;""".format(table_name, someday, top)


        # html代码
        table_hangye = """<h4>∷∷▶在 {0} {1}涨幅前{2}的股票行业分布分析</h4><p>股票行业分布情况分析：此阶段股票涨幅靠前五
                        个行业分别为：{3}, {4}, {5}, {6}, {7}。具体情况见下表：</p><table border="1">
                        <tr><th>序号</th><th>行业</th><th>股票数量</th><th>股票明细</th></tr>
                        """.format(str_day, self.dic_day[someday], top, get_hangey[0][0], get_hangey[1][0], \
                            get_hangey[2][0], get_hangey[3][0], get_hangey[4][0])

        # HTML表格代码
        table_td = """<tr><td>{0}</td><td>{1}</td><td>{2}</td><td>{3}</td></tr>"""

        # 提交
        db.commit()

    # 行业排名情况统计
    def hangyeorder(self, db, cursor, table_name, somedays):
        # 主要统计当天、5个交易日、10个交易日、22个交易日、40个交易日、65个交易日、125个交易日、250个交易日累计涨幅排名
        # 前100名的行业，行业排名前五的
        #

        # str_day 格式改为xxxx年xx月xx日
        str_day = self.str_today[:4] + "年" + self.str_today[4:6] + "月" + self.str_today[-2:]+ "日"
        #str_day = "2021年8月10日"

        #somedays = ["rate_d", "rate_5d", "rate_10d", "rate_22d", "rate_40d", "rate_65d", "rate_125d", "rate_250d"]
        #top = 100

        # html代码
        table_hangyeorder = """<h4>∷∷▶在 {0} 不同阶段涨幅前{1}的股票分析</h4><p>股票行业情况分析。具体情况见下表：</p><table border="1"><tr><th>区间</th>
                        <th>第一名</th><th>第二名</th><th>第三名</th><th>第四名</th><th>第五名</th></tr>
                        """.format(str_day, self.top)
        # HTML表格代码
        table_td = """<tr><td>{0}</td><td>{1}</td><td>{2}</td><td>{3}</td><td>{4}</td><td>{5}</td></tr>"""

        data_hangyes = []
        for someday in somedays:
            # 行业排名分析
            order_hangye = """select * from
                            (select hangye, count(*)as num_st from 
                            (select * from {0} order by {1} desc limit {2}) as a
                            group by hangye) as b order by b.num_st desc limit 5;""".format(table_name, someday, self.top)

            cursor.execute(order_hangye)
            data_hangye = cursor.fetchall()

            # 每个阶段，排名前五行业
            data_hangyes.append([someday, data_hangye[0][0], data_hangye[1][0], data_hangye[2][0], data_hangye[3][0], data_hangye[4][0]])

            table_hangyeorder = table_hangyeorder + table_td.format(someday, data_hangye[0][0] + "(" + str(data_hangye[0][1])+")", \
                            data_hangye[1][0] + "(" + str(data_hangye[1][1])+")", data_hangye[2][0] + "(" + str(data_hangye[2][1])+")",\
                            data_hangye[3][0] + "(" + str(data_hangye[3][1])+")", data_hangye[4][0] + "(" + str(data_hangye[4][1])+")",)

        table_hangyeorder = table_hangyeorder + "</table>" + "\n"

        # 行业出现的次数和排名变化
        # 将行业全部放入列表 hangye_all
        hangye_all = []
        for hangye_list in data_hangyes:
            for i in list(range(1, len(hangye_list))):
                hangye_all.append(hangye_list[i])

        # 统计行业出现的次数，放入字典，并按照降序排列
        hangye_dict = {}
        for key in hangye_all:
            hangye_dict[key] = hangye_dict.get(key, 0) + 1

        # 按照行业出现次数降序排列后的列表
        hangye_order_reverse = sorted(hangye_dict.items(), key=lambda x:x[1], reverse=True)

        # 行业从 250d 至 d 的变化
        hangye_change = []
        for hangye_cishu in hangye_order_reverse:
            hangye_change_mx = ""
            hangye_count = 0
            # 行业从 250d 到 d 的变化顺序
            for qujian_hangye in data_hangyes:
                if hangye_cishu[0] in qujian_hangye:
                    hangye_count = hangye_count + 1
                    if hangye_count != 1:
                        hangye_change_mx = qujian_hangye[0] + "(" + str(qujian_hangye.index(hangye_cishu[0])) + ") → " + hangye_change_mx
                    else:
                        hangye_change_mx = qujian_hangye[0] + "(" + str(qujian_hangye.index(hangye_cishu[0])) + ")" + hangye_change_mx

                else:
                    pass

            hangye_change.append(hangye_change_mx)

        # 构建行业出现次数和变动情况的 html 代码
        table_hangye_change = """<h4>∷∷▶在 {0} 不同阶段涨幅前{1}的股票行业情况分析</h4><p>股票行业出现的次数，以及从前250交易日至今不同
                        阶段涨幅行业的出现次数和行业的变动情况情况分析。具体情况见下表：</p><table border="1"><tr><th>序号</th>
                        <th>行业</th><th>出现次数</th><th>行业变动情况</th></tr>
                        """.format(str_day, self.top)
        # HTML表格代码
        table_td_hangye_change = """<tr><td>{0}</td><td>{1}</td><td>{2}</td><td>{3}</td></tr>"""

        # 表格内容
        for num in list(range(len(hangye_order_reverse))):
            table_hangye_change = table_hangye_change + table_td_hangye_change.format(num+1, hangye_order_reverse[num][0], \
                        hangye_order_reverse[num][1], hangye_change[num])
        table_hangye_change = table_hangye_change + "</table>" + "\n"

        #print(table_hangyeorder)
        return table_hangyeorder + table_hangye_change

    # 股票涨幅个股分析，并构造个股分析的html代码，筛选的股票增加入通达信软件的 up板块
    def stockup(self, db, cursor, tablename):
        # 选股策略：1、统计截止今日前125个交易日涨幅排行前200股票的行业，选择行业排前五的行业；
        #          2、个股趋势向上，指标为前10/22/40/65/125/250个交易日价格逐步上涨，即涨幅逐步增大；
        #          3、排除上市不足一个月的股票：即22交易日涨幅=250交易日涨幅的股票；
        #          4、按照22个交易日涨幅排序，取前50只个股。

        # str_day 格式改为xxxx年xx月xx日
        str_day = self.str_today[:4] + "年" + self.str_today[4:6] + "月" + self.str_today[-2:]+ "日"

        # 统计 前125 个交易日涨幅前 200 名的行业排前五的行业情况
        order_look_hangye = """select hangye from
                        (select hangye, count(*)as num_st from 
                        (select * from {0} order by {1} desc limit {2}) as a
                        group by hangye) as b order by b.num_st desc limit 5;""".format(tablename, "rate_125d", 200)

        cursor.execute(order_look_hangye)

        # 行业数据
        data_hangye = cursor.fetchall()
        # 排名前五的行业名称转换成元组
        data_hangye = (data_hangye[0][0], data_hangye[1][0], data_hangye[2][0], data_hangye[3][0], data_hangye[4][0])

        # 股票250的涨幅逐排名前500，125交易日涨幅大于50%, 22交易日涨幅大于30%, 上市大于半年
        order_look_stock = """select * from (select * from (select * from {0} order by rate_250d desc limit 500)
                             as a where rate_125d > 50 and rate_22d > 30 and rate_250d != rate_125d) as b
                             order by rate_22d desc;""".format(tablename)
        '''
        # 股票10/22/40/65/125/250的涨幅逐步增加的股票, 上市大于半年
        order_look_stock = """select * from (select * from {0} where rate_250d > rate_125d and
                    rate_125d > rate_65d and rate_65d > rate_40d and rate_40d > rate_22d and 
                    rate_22d > rate_10d and hangye in {1}) as a
                    order by rate_22d desc limit 80;""".format(tablename, data_hangye)
        '''

        cursor.execute(order_look_stock)

        data_stock = cursor.fetchall()
        
        # 转换为html代码
        # 列表显示序号、代码、股票名称、行业、当天涨幅、22/125交易日涨幅
        table_stock = """<h4>∷∷▶在 {0}统计筛选的股票如下表：</h4><p>筛选规则：股票最近250个交易日的涨幅排名前500名，
                        最近125个交易日涨幅大于50%, 最近22个交易日涨幅大于30%, 股票上市时间大于半年。其中与上一交易日相比排名
                        上升大于10和新进入该排行榜的股票，均以 ※※ 进行标注。 </p>
                        <table border="1"><tr><th>序号</th><th>代码</th><th>股票名称</th><th>行业</th><th>当天涨幅</th>
                        <th>22交易日涨幅</th><th>125交易日涨幅</th><th>22交易日涨幅排名变动</th><th>22交易日出现次数</th></tr>""".format(str_day)
        # HTML表格代码
        table_td = """<tr><td>{0}</td><td><a href='{1}'>{2}</a></td><td><a href='{1}'>{3}</a></td><td>{4}</td>\
                    <td>{5}%</td><td>{6}%</td><td>{7}%</td><td>{8}</td><td>{9}</td></tr>"""
        
        # 存放取出的股票HTML代码
        st_mx = ""

        # 放入通达信 up.blk 板块
        tdx_up = ""

        # 上一交易日数据库table名称
        table_bef_name = "stock" + self.beforeday().strftime("%Y%m%d")

        # 循环取出筛选出的股票，构建html代码
        # i+1 也是22交易日涨幅排名
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
            # 股票在东方财富网的网址
            stock_link = "http://quote.eastmoney.com/" + stock_code + ".html"

            # 查询股票的排名，传递进两个参数：数据表名称、股票代码
            order_look_order = """select c.num_new, c.code from (select (@rownum:=@rownum+1) as num_new, b.* from (select * from
                                (select * from {0} order by rate_250d desc limit 500) as a
                                where rate_125d > 50 and rate_22d > 30 and rate_250d != rate_125d) as b,
                                (select @rownum:=0) as d order by rate_22d desc limit 200) as c where code = {1};"""
            
            # 查询股票在上个交易日的排名
            # 查询上个交易日数据表是否存在
            order_exist_table = "show tables like '%s'" % table_bef_name
            cursor.execute(order_exist_table)
            yesorno = cursor.fetchone()

            # 如果查询返回None，则重新插入数据
            if yesorno == None:
                self.insertmsg_sql(table_bef_name, self.stockmsg(table_bef_name[5:]), db, cursor)
            else:
                pass

            cursor.execute(order_look_order.format(table_bef_name, data_stock[i][1]))
            num_bef = cursor.fetchone()

            # 查询股票在本交易日的排名
            cursor.execute(order_look_order.format(self.table_name, data_stock[i][1]))
            num_tod = cursor.fetchone()

            if num_bef == None:
                else_msg = "新入   ※※"
            else:
                if num_bef[0] == num_tod[0]:
                	else_msg = "----"
                elif num_bef[0] < num_tod[0]:
                    else_msg = "下降" + str(num_tod[0] - num_bef[0])[:-2] + "位 ↓"
                else:
                    else_msg = "上升" + str(num_bef[0] - num_tod[0])[:-2] + "位 ↑"
                    if num_bef[0] - num_tod[0] > 10:
                        else_msg = else_msg + "   ※※"

            # 最近22个交易日出现次数
            # stock_times初始值为1， 表示今天筛选出； 计数器21，向前计算21个交易日，和今天一起22个交易日
            stock_times = 1
            bef_days = 1
            # 循环计算最近22个交易日出现的次数
            while bef_days < 22:
                # 数据表名
                table_bef_days_name = "stock" + self.beforeday(bef_days).strftime("%Y%m%d")
                # 数据表内查询  股票是否在 bef_days 交易日前的筛选出的范围内
                cursor.execute(order_look_order.format(table_bef_days_name, data_stock[i][1]))
                stock_msg = cursor.fetchone()

                # 统计出现次数
                if stock_msg == None:
                    pass
                else:
                    stock_times = stock_times + 1

                # 计数器增加
                bef_days = bef_days + 1



            # 构建股票信息元组
            tuple_stock = (i+1, stock_link, data_stock[i][1], data_stock[i][2], data_stock[i][3], data_stock[i][11], \
                        data_stock[i][8], data_stock[i][5], else_msg, stock_times)
            #print(tuple_stock)

            # 构建HTML表格代码
            st_mx = st_mx + table_td.format(*tuple_stock)

        # html 表格代码
        table_stock = table_stock + st_mx   
        table_stock = table_stock + "\n"

        # 表格结束
        table_stock = table_stock + "</table>" + "\n"
        #print(table_hangye)

        # 通达信 up 板块
        path_tdx_up = "D:\\zd_ciccwm\\T0002\\blocknew\\UPUP.blk"
        # 将筛选的股票写入通达信软件的 up 板块，可以直接在通达信软件中查看 up 板块股票
        with open(path_tdx_up, "w", encoding="utf-8") as f:
            f.write(tdx_up)
            f.close()

        # 提交
        db.commit()

        return table_stock

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

    # 完整的HTML代码，发送邮件的HTML格式全部内容
    def content_html(self, msg):

        # html 头部
        con_head = """ <!DOCTYPE html> <html> 
        <head>  <meta charset="utf-8"> <title>股票分析</title> </head>
        <body>  <h3>股票情况概述</h3> <p>--自己编写的股票分析程序--</p>"""

        # html 尾部
        con_end = " </body> </html>"
        
        # 完整的邮件发送的HTML代码
        con = con_head + msg + con_end
        
        return con

    # 发送邮件
    def email_send(self, messages):
        # message 邮件发送的信息
        
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

# 主文件
if __name__ == '__main__':
    
    app = StockAnalysis()
    app.operate_sql()
    