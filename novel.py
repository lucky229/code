#!/usr/bin/env python3
# -*- coding:UTF-8 -*-

import requests
from bs4 import BeautifulSoup

#目录及各章节地址
def NameAndAdd():
	url = r"http://www.biquge.info/74_74068/"
	headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36"
}
	r = requests.get(url, headers = headers)
	r.encoding = r.apparent_encoding
	soup1 = BeautifulSoup(r.text, "html.parser")
	soup2 = soup1.find_all(id="list")[0].find_all('a')

	#各章节地址
	name_list = []
	add_list = []
	for i in soup2:
		add_list.append(i.get('href'))
		name_list.append(url + i.get('title'))

	return name_list, add_list		

#章节内容
def PageContent():

	#url = r'http://www.biquge.info/0_273/18142455.html'
	url = r"https://www.booktxt.net/20_20832/620223455.html"
	headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36"
}

	r = requests.get(url, headers=headers)
	r.encoding = r.apparent_encoding
	soup1 = BeautifulSoup(r.text, "html.parser")
	#soup2 = soup1.find_all(id="content")[0].text
	soup2 = soup1.find_all(id="content")[0].text
	print(soup2)

	

if __name__ == '__main__':
	PageContent()