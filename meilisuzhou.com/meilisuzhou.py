#!/usr/bin/env python3
# -*- coding: utf-8 -*-


'''

@author: Charles
@license: Copyright(C), Jinshu Information Technology (Suzhou) Co., Ltd.
@contact: charles.lin@qingbao.cn
@software: Pycharm 2018.1
@file: jiaoyou.py
@time: 2018/9/26 21:19
@desc:

'''

import requests
import csv
import time
import pymysql


proxies = {'http': '39.135.9.109:8080', 'https':'125.77.80.105:8118'}



def get_param(index):
	header = {
	'Host': 'www.meilisuzhou.com',
	'Connection': 'keep-alive',
	'Content-Length': '115',
	'Accept': '*/*',
	'Origin': 'http://www.meilisuzhou.com',
	'X-Requested-With': 'XMLHttpRequest',
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.92 Safari/537.36',
	'DNT': '1',
	'Content-Type': 'application/x-www-form-urlencoded',
	'Referer': 'http://www.meilisuzhou.com/members.aspx',
	'Accept-Encoding': 'gzip, deflate',
	'Accept-Language': 'zh-CN,zh;q=0.9',
	'Cookie': 'ASP.NET_SessionId=3itqhjpzsmumt4bdcimrgi0s; arp_scroll_position=1792'}

	form = {
	'act': 'detail',
	'pindex':str(index),
	'cityid': 'C7703BB702B047249D7B382314E3BC85',
	'selage0':'',
	'selage1':'',
	'unumber':'',
	'selsex': '女',
	'selPhotos': '0'
	}

	param = {
		'header': header,
		'form': form
	}
	return param




#新建csv文件
#女性数据
csvf = open('meilisuzhou_femaledata.csv', 'a+', encoding='utf-8', newline='')
writer = csv.writer(csvf)
writer.writerow(('用户ID','真实姓名','昵称','性别','年龄','出生日期','出生地','城市',
                 '学历','身高','体重','爱好','婚姻','电话','汽车','住房','职业','个人描述'))

# 男性数据
# csvf = open('meilisuzhou_maledata.csv', 'a+', encoding='utf-8', newline='')
# writer = csv.writer(csvf)
# writer.writerow(('用户ID','真实姓名','昵称','性别','年龄','出生日期','出生地','城市',
#                  '学历','身高','体重','爱好','婚姻','电话','汽车','住房','职业','个人描述'))


def start_request(writer, sleep=6):
	# 发送请求
	base = 'http://www.meilisuzhou.com/viewapi/membersearch.ashx'
	url = base.format()

	user_data = []
	for i in range(300):
		print("循环："+str(i+1))
		param = get_param(i+1)
		resp = requests.post(url, proxies=proxies, headers=param.get("header"), data=param.get("form"))
		try:
			user_data += resp.json()
		except Exception as e:
			print("error: " + str(e))
	print(user_data)


	# 保存
	for users in user_data:
		usernumber = users.get('Usernumber') #用户ID
		userlogin = users.get('Userlogin')   #用户名
		muid = users.get('Muid')
		name = users.get('Name') #昵称
		sex = users.get('Sex')  #性别
		age = users.get('Age')  #年龄


		try:
			realname = users.get('Realname')    #真实姓名
			birthdate = users.get('Birthdate')  #出生日期
			born = users.get('Born')            #出身地
			cityname = users.get('Cityname')    #城市
			degree = users.get('Degree')
			degreename = users.get('Degreename')#学历
			delname = users.get('Delname')
			height = users.get('Height')        #身高
			weight = users.get('Weight')        #体重
			likeing = users.get('Likeing')      #爱好
			marry = users.get('Marry')
			marryname = users.get('Marryname')  #婚姻
			mobile = users.get('Mobile')        #电话
			usecarname = users.get('Usecarname')#汽车
			usercar = users.get('Usercar')
			yanzhengname = users.get('Yanzhengname')#是否验证
			zhiye = users.get('Zhiye')          #职业
			zhugnfangname = users.get('Zhugnfangname')#住房
			description = users.get('Description')#个人介绍

		except:
			realname = '无'
			birthdate = '无'
			born = '无'
			cityname = '无'
			degree = '无'
			degreename = '无'
			delname = '无'
			height = '无'
			weight = '无'
			likeing = '无'
			marry = '无'
			marryname = '无'
			mobile = '无'
			usecarname = '无'
			usercar = '无'
			yanzhengname = '无'
			zhiye = '无'
			zhugnfangname = '无'
			description = '无'


		# 逐行写入并打印
		writer.writerow((userlogin,realname,name,sex,age,birthdate,born,cityname,degreename,
		                 height,weight,likeing,marryname,mobile,usecarname,zhugnfangname,zhiye,description))
		print(userlogin,realname,name,sex,age,birthdate,born,cityname,degreename,
		                 height,weight,likeing,marryname,mobile,usecarname,zhugnfangname,zhiye,description)
		save_to_mysql(usernumber,userlogin,muid,realname,name,sex,age,birthdate,born,cityname,degree,degreename,
		                 delname,height,weight,likeing,marry, marryname,mobile,usecarname,usercar,yanzhengname,
		              zhiye,zhugnfangname,description)

	#降低访问速度
	time.sleep(sleep)



def save_to_mysql(usernumber,userlogin,muid,realname,name,sex,age,birthdate,born,cityname,degree,degreename,
		                 delname,height,weight,likeing,marry, marryname,mobile,usecarname,usercar,yanzhengname,
		              zhiye,zhugnfangname,description):
	try:
		conn = pymysql.connect(host='localhost', port=3306, user='root', password='111111', db='meilisuzhou',charset="utf8")
		cursor = conn.cursor()



		# 爬取女性数据
		insert_sql = """
                    insert into femaledata(usernumber,userlogin,muid,realname,name,sex,age,birthdate,born,cityname,degree,degreename,
		                 delname,height,weight,likeing,marry, marryname,mobile,usecarname,usercar,yanzhengname,
		              zhiye,zhugnfangname,description)
                    values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s, %s,%s)
                """

		# # 爬取男性数据
		# insert_sql = """
		#                     insert into maledata(usernumber,userlogin,muid,realname,name,sex,age,birthdate,born,cityname,degree,degreename,
		# 		                 delname,height,weight,likeing,marry, marryname,mobile,usecarname,usercar,yanzhengname,
		# 		              zhiye,zhugnfangname,description)
		#                     values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s, %s,%s)
		#                 """

		cursor.execute(insert_sql, (usernumber,userlogin,muid,realname,name,sex,age,birthdate,born,cityname,degree,degreename,
		                 delname,height,weight,likeing,marry, marryname,mobile,usecarname,usercar,yanzhengname,
		              zhiye,zhugnfangname,description))
		conn.commit()
		cursor.close()
		conn.close()
	except Exception as e:
		print('wrong' + str(e))


#开始递归爬取
if __name__ == '__main__':
    start_request(writer)
