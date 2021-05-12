# -*- codeing = utf-8 -*-

'''
title：爬虫之B站视频评论
writer：山客
The_last_update_date：2021.5.12
'''

from bs4 import BeautifulSoup  # 网页解析，获取数据
import re  # 正则表达式，进行文字匹配`
import urllib.request
import urllib.error  # 制定URL，获取网页数据
import requests
import json
import time  # 时间
import random  # 随机
import math
import xlwt  # 进行excel操作
import xlrd
from xlutils.copy import copy


# 抓取网页
def get_html(url: str):
	headers = {
		'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',  # 支持类型
		'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36',
	}  # 爬虫模拟访问信息

	try:
		r = requests.get(url, timeout=30, headers=headers)
		r.raise_for_status()
		r.endcodding = 'utf-8'
		return r.text
	except requests.HTTPError as e:
		print(e)
		print("HTTPError")
	except requests.RequestException as e:
		print(e)
	except:
		print("Unknown Error !")


# 分析网页，整理信息
def get_content(url: str, page: int):
	comments = []

	# 抓取网页，并且将数据下载到本地
	html = get_html(url)

	try:
		s = json.loads(html)  # 原始数据默认为s['data']
		print("JsonLoad Successed!")

		# 获取每页评论栏的数量
		# num = int(s['data']['page']['account'])
		num = len(s['data']['replies'])
		# print("该第 " + str(page) + " 页所有评论数： ", num)

		i = 0
		while i < num:
			# 获取每则评论
			comment = s['data']['replies'][i]

			InfoDict = {}  # 用于存储每则评论的具体信息
			InfoDict['Uname'] = comment['member']['uname']
			InfoDict['Time'] = time.strftime(
				"%Y-%m-%d %H:%M:%S",
				time.localtime(comment['ctime']))  # api中ctime是编码形式，需要特殊处理
			InfoDict['Content'] = comment['content']['message']

			# 保存到总评论表中
			comments.append(InfoDict)
			i += 1

		# with open("tmp.txt", 'w') as tmp_w:
		# tmp_w.write(comments)
		# print(len(comments))

		return comments
	except:
		print("JsonLoad Error!")


def write_in_xls(BV_ID: str, content: list, path: str, pages: int):
	# 创建/调用工作表
	if pages == 1:
		# 创建workbook对象
		workbook = xlwt.Workbook()
		sheet = workbook.add_sheet(BV_ID)
		col = ('Uname', 'Time', 'Comment')
		l_col = len(col)
		for i in range(l_col):
			sheet.write(0, i, col[i])  # line行i列，写入col[i]
	else:
		# 打开workbook对象
		old_book = xlrd.open_workbook(path)
		workbook = copy(old_book)
		sheet = workbook.get_sheet(0)

	l_con = len(content)

	line = 1
	for i in range(l_con):
		# print("loading....")

		comment = content[i]
		row = 0
		for k, v in comment.items():
			sheet.write(line + (pages - 1) * 20, row, v)
			row += 1

		line += 1

	# print(line)
	workbook.save(path)


def BV_to_AV(BV_ID: str) -> int:
	keys = {'1': '13', '2': '12', '3': '46', '4': '31', '5': '43', '6': '18', '7': '40', '8': '28', '9': '5',
			'A': '54', 'B': '20', 'C': '15', 'D': '8', 'E': '39', 'F': '57', 'G': '45', 'H': '36', 'J': '38',
			'K': '51', 'L': '42', 'M': '49', 'N': '52', 'P': '53', 'Q': '7', 'R': '4', 'S': '9', 'T': '50',
			'U': '10', 'V': '44', 'W': '34', 'X': '6', 'Y': '25', 'Z': '1',
			'a': '26', 'b': '29', 'c': '56', 'd': '3', 'e': '24', 'f': '0', 'g': '47', 'h': '27',
			'i': '22', 'j': '41', 'k': '16', 'm': '11', 'n': '37', 'o': '2', 'p': '35', 'q': '21',
			'r': '17', 's': '33', 't': '30', 'u': '48', 'v': '23', 'w': '55', 'x': '32', 'y': '14', 'z': '19'
	}

	# 去除Bv号前的"Bv"字符
	Bv_No_1 = BV_ID[2:]

	# 将key对应的value存入一个列表
	Bv_No_2 = []
	for index, char in enumerate(Bv_No_1):
		Bv_No_2.append(int(str(keys[char])))

	# 3. 对列表中不同位置的数进行*58的x次方的操作
	Bv_No_2[0] = int(Bv_No_2[0] * math.pow(58, 6))
	Bv_No_2[1] = int(Bv_No_2[1] * math.pow(58, 2))
	Bv_No_2[2] = int(Bv_No_2[2] * math.pow(58, 4))
	Bv_No_2[3] = int(Bv_No_2[3] * math.pow(58, 8))
	Bv_No_2[4] = int(Bv_No_2[4] * math.pow(58, 5))
	Bv_No_2[5] = int(Bv_No_2[5] * math.pow(58, 9))
	Bv_No_2[6] = int(Bv_No_2[6] * math.pow(58, 3))
	Bv_No_2[7] = int(Bv_No_2[7] * math.pow(58, 7))
	Bv_No_2[8] = int(Bv_No_2[8] * math.pow(58, 1))
	Bv_No_2[9] = int(Bv_No_2[9] * math.pow(58, 0))

	# 4.求出这10个数的合
	sum = 0
	for i in Bv_No_2:
		sum += i
	# 5. 将和减去100618342136696320
	sum -= 100618342136696320
	# 6. 将sum 与177451812进行异或
	temp = 177451812

	return sum ^ temp


if __name__ == '__main__':
	en = True  # 使能信号
	pages = 1  # 评论条数

	BV_ID = input("BV_ID: ")
	path = "Bilibili_Comments.xls"

	while en:

		# 数据开放接口
		# type - ？; oid - av_id ; sort - ?
		url = "https://api.bilibili.com/x/v2/reply?type=1&oid=" + str(BV_to_AV(BV_ID)) + "&sort=2&pn=" + str(pages)

		if get_content(url, pages):
			content = get_content(url, pages)
			print("Save Successed!")
			# print(type(content))
			write_in_xls(BV_ID, content, path,pages)
			print("Write Successed!")

			pages += 1

			# 为了降低被封ip风险，适当歇息
			coe = random.randint(0, 10)
			Hole_line = list(range(0, 5))
			if coe in Hole_line:
				time.sleep(coe * 1.000000007)
		else:
			en = False

