# -*- coding:utf-8 -*-

import requests
from bs4 import BeautifulSoup
import re
import lxml

url = "http://sou.zhaopin.com/jobs/searchresult.ashx?jl=上海&kw=Python&p=1&kt=3"
wbdata = requests.get(url).content
soup = BeautifulSoup(wbdata,'lxml')

items = soup.select("div#newlist_list_content_table > table")
count = len(items) - 1
# 每页职位信息数量
print(count)

job_count = re.findall(r"共<em>(.*?)</em>个职位满足条件", str(soup))[0]
# 搜索结果页数
pages = (int(job_count) // count) + 1
print(pages)
