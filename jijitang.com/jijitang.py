#!/usr/bin/env python3
# -*- coding: utf-8 -*-


'''

@author: Charles
@license: Copyright(C), Jinshu Information Technology (Suzhou) Co., Ltd.
@contact: charles.lin@qingbao.cn
@software: Pycharm 2018.1
@file: jijitang.com.py
@time: 2018/9/27 10:07
@desc:

'''

import requests
import csv
import time
import pymysql


#新建csv文件
csvf = open('jijitang_userdata.csv', 'a+', encoding='utf-8', newline='')
writer = csv.writer(csvf)
writer.writerow(('昵称','id','学历','学校','学院','专业','经验','简介'))

# 初识URL参数
last = 2065
lastid = '5b96fb1bc2f15ecd73ddf606'

def start_request(writer, last, lastid, sleep=2):

	# 发送请求
	base = 'http://www.jijitang.com/profile/list?sort=recommend&last={last}&ltId={lastid}'
	url = base.format(last=last, lastid=lastid)
	resp = requests.get(url)
	data = resp.json()

	# 保存
	for users in data:
		nickname = users.get('nickname')  # 昵称
		userid = users.get('_id')   # ID

		try:
			profile = users.get('profile')  # 简介
			role = users.get('institution').get('role')  # 学历
			institute = users.get('institution').get('institute')  # 所属学校
			dept = users.get('institution').get('dept')  # 所属学院
			experience = users.get('experience')  # 经验
			field = users.get('field')  # 专业
		except:
			profile = '无'
			role = '无'
			institute = '无'
			dept = '无'
			experience = '无'
			field = '无'


		# 逐行写入并打印
		writer.writerow((nickname, userid, role, institute, dept, field, profile, experience))
		print(nickname, userid, role, institute, dept, field, profile, experience)
		save_to_mysql(nickname, userid, role, institute, dept, field, profile, experience)

	#最后一个用户信息
	#用户信息的rate对应last参数
	#用户信息的_id对应lastid参数
	last_user = data[-1]
	last = last_user.get('rate')
	lastid = last_user.get('_id')

	#降低访问速度
	time.sleep(sleep)

	#根据最后一个用户的last和lastid,实现对下一批用户信息的爬取操作（递归）
	return start_request(writer, last, lastid,)


def save_to_mysql(nickname, userid, role, institute, dept, field, profile, experience):
	try:
		conn = pymysql.connect(host='localhost', port=3306, user='root', password='111111', db='jijitang',charset="utf8")
		cursor = conn.cursor()

		insert_sql = """
                    insert into user_data(nickname, userid, role, institute, dept, field, profile, experience)
                    values(%s, %s, %s, %s, %s, %s, %s, %s)
                """
		cursor.execute(insert_sql, (nickname, userid, role, institute, dept, field, profile, experience))
		conn.commit()
		cursor.close()
		conn.close()
	except Exception as e:
		print('wrong' + str(e))


#开始递归爬取
if __name__ == '__main__':
    start_request(writer, last, lastid)




