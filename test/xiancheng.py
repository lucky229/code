#!/usr/bin/env python3
# -*- coding:UTF-8 -*-

import threading
import time
import datetime

# 该类是自定义的多线程类
# 多己写多线程时仿造记类实现自己的多线程类即可
class MyThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    # 必须实现函数，run函数被start()函数调用
    def run(self):
        thread_name = threading.current_thread().name
        print(f"开始线程： {thread_name}")
        self.print_time()
        print(f"退出线程： {thread_name}")

    # 可选函数，此处函数的代码可移到run函数内部，也可放到MyThread之外，无关紧要
    # 线程要做的具体事务函数，我们这里就打印两轮时间
    def print_time(self):
        count = 2
        thread_name = threading.current_thread().name
        while count:
            time.sleep(1)
            print(f"{thread_name}： {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S %f')}")
            count -= 1

# 该类是一个演于调用MyThread的类
# 其实其代码也完全可以放在if __name__ == "__main__"处
class TestClass():
    def __init__(self):
        pass

    def main_logic(self):
        # 创建新线程实例
        thread_1 = MyThread()
        thread_2 = MyThread()

        # 启动新线程
        thread_1.start()
        thread_2.start()

        # thread_1.join()即当前线程（亦即主线程）把时间让给thread_1，待thread_1运行完再回到当前线程
        # thread_2.join()即当前线程（亦即主线程）把时间让给thread_2，待thread_1运行完再回到当前线程
        # join()方法非阻塞
        # 如果没对某个线程使用join()方法，那么当前线程（亦即主线程）不会等待该线程执行完再结束，他会直接结束
        # 在多线程的进程中，主线程的地位和其他线程的地位是平等的，不会说主线程退出了就会导致整个进程，进而导致其他线程被迫终止
        # 自己把这两句join()注释掉再运行一遍，可以更好理解这里的说法
        thread_1.join()
        thread_2.join()

        print("退出主线程")

if __name__ == "__main__":
    obj = TestClass()
    obj.main_logic()