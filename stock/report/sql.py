#!/usr/bin/env python3
# -*- coding:UTF-8 -*-

import pymysql


import time
import datetime
import os

def send_sql():

    # 打开数据库连接
    db = pymysql.connect(host="localhost", user="root", password="123456",database="test", charset="utf8")
     
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()

    # 表格名称
    #str_today = datetime.date.today().strftime("%Y%m%d")
    #table_name = "stock" + str_today
    str_today = "20210728"
    table_name = "stock" + str_today
    someday = "rate_d"
    top = 200

    # 统计前前100名行业排前五的行业情况
    order_looks = """select * from
                      (select hangye, count(*)as num_st from 
                      (select * from {0} order by {1} desc limit {2}) as a
                      group by hangye) as b order by b.num_st desc limit 5;""".format(table_name, someday, top)

    # 查询行业前100范围内，单个行业包含哪些股票
    order_look_stock = """select name, {0} from 
                        (select * from {1} order by {0} desc limit {2})as a
                        where hangye="{3}";"""

    cursor.execute(order_looks)
    get_hangey = cursor.fetchall()



    table_hangye = """<h4>当天（{0}）涨幅前{1}的股票分析</h4><p>股票行业情况分析：今天股票涨幅靠前三个行业分别为：{2}, {3}, {4}。具体情况见下表：</p>
                    <table border="1"><tr><th>序号</th><th>行业</th><th>股票数量</th><th>股票明细</th></tr>
                    """.format(str_today, top, get_hangey[0][0], get_hangey[1][0], get_hangey[2][0])
    table_td = """<tr><td>{0}</td><td>{1}</td><td>{2}</td><td>{3}</td></tr>"""

    for i in list(range(len(get_hangey))):
        
        cursor.execute(order_look_stock.format(someday, table_name, top, get_hangey[i][0]))
        get_hangey_st = cursor.fetchall()
        st_mx = ""
        for m in list(range(len(get_hangey_st))):
            if m != len(get_hangey_st) - 1:
                st_mx = st_mx + get_hangey_st[m][0] + ", "
            else:
                st_mx = st_mx + get_hangey_st[m][0]

        table_hangye = table_hangye + table_td.format(i + 1, get_hangey[i][0], get_hangey[i][1], st_mx)
        table_hangye = table_hangye + "\n"
    print(table_hangye)


    #print(get_hangey, type(get_hangey), len(get_hangey))
    #print(get_hangey_st, type(get_hangey_st), len(get_hangey_st))


    # 提交
    db.commit()

    # 关闭光标对象
    cursor.close()
     
    # 关闭数据库连接
    db.close()









if __name__ == '__main__':
    send_sql()