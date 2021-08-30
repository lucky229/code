#!/usr/bin/evn python3
# -*- coding:UTF-8 -*-

"""
即时通讯原理 
@@@ 客户端代码

"""

from socket import *
import threading

ip,port ='127.0.0.1',8888

Client = socket(AF_INET,SOCK_STREAM)
Client.connect((ip,port))

def  sends() -> '发送函数':
    while 1:

        say = bytes(input("[*]我说: "),encoding='utf-8')
        Client.send(say)
def recvs() -> '接受函数':
    while 1:

        print('[*] 服务端说: %s  ' % Client.recv(1024).decode('utf-8'))

receive = threading.Thread(target =recvs ,args=() )
receive.start()
# 创建发送线程
send = threading.Thread(target =sends ,args=() )
send.start()