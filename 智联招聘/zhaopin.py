# -*- coding:utf-8 -*-

import requests
from bs4 import BeautifulSoup
from multiprocessing import Pool
from Spider_Practice.spider_exercise.getpages import pages


def get_zhaopin(page):
    url = "http://sou.zhaopin.com/jobs/searchresult.ashx?jl=上海&kw=Python&p={0}&kt=3".format(page)
    print("第{0}页".format(page))
    wbdata = requests.get(url).content
    soup = BeautifulSoup(wbdata,'lxml')

    job_name = soup.select("table.newlist > tr > td.zwmc > div > a")
    salarys = soup.select("table.newlist > tr > td.zwyx")
    company = soup.select("table.newlist > tr > td.gsmc")
    locations = soup.select("table.newlist > tr > td.gzdd")
    times = soup.select("table.newlist > tr > td.gxsj > span")


    for name, salary, company, location, time in zip(job_name, salarys, company, locations, times):
        data = {
            'name': name.get_text(),
            'salary': salary.get_text(),
            'company': company.get_text(),
            'location': location.get_text(),
            'time': time.get_text(),
        }
        print(data)



if __name__ == '__main__':
    pool = Pool(processes=2)
    pool.map_async(get_zhaopin, range(1, pages + 1))
    pool.close()
    pool.join()


