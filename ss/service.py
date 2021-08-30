#!/usr/bin/evn python3
# -*- coding:UTF-8 -*-

"""
即时通讯原理 
@@@ 服务端代码

"""

from socket import *
import threading

ip = '0.0.0.0'
port =8888
# 定义 socket 参数

Server = socket(AF_INET,SOCK_STREAM)
Server.bind((ip,port))
Server.listen()
print("[*] SocketServer 正在监听...")

# 接受函数
def  recvs():
    while 1:
        print(' [*] 客户端说: %s '% client.recv(1024).decode('utf-8'))

#发送函数
def  sends():
    while 1:
        say = bytes(input(' [*] 我说: ') , encoding='utf-8')
        client.send(say)
# 堵塞接受请求

client,client_ip  = Server.accept()
print(client_ip[0] +':'+str(client_ip[1])+' 连接成功！' )

# 创建接受线程
receive = threading.Thread(target =recvs ,args=() )
receive.start()
# 创建发送线程
send = threading.Thread(target =sends ,args=() )
send.start()