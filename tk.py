#!/usr/bin/env python3
# -*- coding:UTF-8 -*-

import tkinter
# 创建窗体
stock = tkinter.Tk()
# 窗体名称
stock.title("股票信息更新")
# 大小
stock.geometry("500x500+200+50")

# 输入股票名称
label_name = tkinter.Label(stock, text="请输入你想搜索的股票名称（多个股票以英文逗号隔开）：").pack()
entery_name = tkinter.Entry(stock, text="输入股票名称")
entery_name.pack()

# 接受邮件的邮箱
label_email = tkinter.Label(stock, text="请输入接受信息的邮箱（多个邮箱以英文逗号隔开）：").pack()
entery_email = tkinter.Entry(stock, text="输入邮箱")
entery_email.pack()

def hl():
	stock_name = entery_name.get()
	email_name = entery_email.get()
	print("I am working......")
	print(stock_name)
	print(email_name)
	label_msg = tkinter.Label(stock, text=stock_name)
	label_msg.pack()

# 提交按钮
button_sumit = tkinter.Button(stock, text = "summit", command = hl).pack()



#text_msg = tkinter.Text(stock, width = 50, height = 10)
#text_msg.pack()


stock.mainloop()