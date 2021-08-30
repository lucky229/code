#!/usr/bin/env python3
# -*- coding:UTF-8 -*-

import pandas as pd


def hw():
	startnum = 100
	n = 0

	while startnum < 1000-5:
		num = 1
		for i in range(6):
			num = num * (startnum + i)

		if num % 10000 == 0 and num % 100000 != 0:
			print(startnum , "--", (startnum + 5))
			n = n + 1

		startnum = startnum +1

	print("这样的连续6个三位数共有{0}组".format(n))

if __name__ == '__main__':
	hw()