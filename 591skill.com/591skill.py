#!/usr/bin/env python3
# -*- coding: utf-8 -*-


'''

@author: Charles
@license: Copyright(C), Jinshu Information Technology (Suzhou) Co., Ltd.
@contact: charles.lin@qingbao.cn
@software: Pycharm 2018.1
@file: 591skill.py
@time: 2018/9/26 18:10
@desc:

'''

import csv
import requests

#新建csv文件，用于存储数据
csvf = open("user-data.csv", 'a+', encoding='utf-8', newline='')
writer = csv.writer(csvf)
writer.writerow(('昵称', '年龄', '会', '想学', '留言', '城市', '性别'))



# #第一页URL
# url = "http://www.591skill.com/api/recent-skills?page=0"
# resp = requests.get(url)
# data = resp.json()

#网页模版
base = 'http://www.591skill.com/api/recent-skills?page={page}'
#for循环批量构建URL
for page in range(1,200):
	url = base.format(page=page)
	resp = requests.get(url)
	data = resp.json()

	# 获得技能公告信息
	exchangers = data['result']['list']
	for exchanger in exchangers:
		nickname = exchanger.get('nickname')
		age = exchanger.get('age')
		can = exchanger.get('can')
		want = exchanger.get('want')
		remark = exchanger.get('remark')
		city = exchanger.get('city')
		gender = exchanger.get('sex')

		# 存储数据
		writer.writerow((nickname, age, can, want, remark, city, gender))
		# 打印
		print(nickname, age, can, want, remark, city, gender)


#关闭csv文件
csvf.close()