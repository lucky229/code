#!/usr/bin/env python3
# -*- coding:UTF-8 -*-

import os
import time

def makefile():
    path = 'D:\\code\\text\\'
    file_path = path + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())[:10] + ".txt"
    messages = "hello world,again，哈哈哈 "

    if os.path.exists(file_path):
        f = open(file_path,'r')
        f.seek(0)
        read = f.read()
        f.close()
        #print(read)
        if read == messages:
            print('yes')
            return False
        else:
            f = open(file_path,'w')
            f.write(messages)
            print("复写，ok")
            return True
        
        
    else:
        os.makedirs(path)
        f = open(file_path,'w')
        f.write(messages)
        f.close()

        return True
 
if __name__ == '__main__':
    print("It is bigen..............")
    print(makefile())