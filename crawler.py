# -*- coding: utf-8 -*-
from loggerConfig import Config
import requests
import re
import time
import random
from util.DBUtil import MysqlUtil
from util.getProxy import proxy

targetPath = 'books/books2000.txt'
file_object = open(targetPath, 'a')
logger = Config.loggerinfo()
bookDB = MysqlUtil('localhost', 3306, 'root', 'root', 'book')

bookstr = r'<div.*?desc">.*?<p>文件名称：(.*?)</p>.*?<p>文件大小：(.*?)</p>.*?<p>作者信息：(.*?)</p>.*?' + \
          r'<p>网盘密码：百度网盘密码：(.*?)&nbsp;.*?<div class="list">.*?href="(.*?)"'

categorystr = r'<div class="left">.*?<a.*?rel="category tag">(.*?)</a>.*?<a.*?rel="category tag">(.*?)</a>'


def getinfo(url, index):
    headers = [
        'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.94 Safari/537.36',
        'Mozilla/5.0 (Linux; Android 4.0.4; Galaxy Nexus Build/IMM76B) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.133 Mobile Safari/535.19']
    header_index = random.randint(0, len(headers) - 1)
    header = {'User-Agent': headers[header_index]}

    # proxys = proxy.getdata()
    # proxy_index = random.randint(0,len(proxys))
    # proxy_a = {"http": 'http://103.251.167.18:1080'}

    # response = requests.get(url, proxies=proxy_a, headers=header)
    data = getweb(url, header)

    items = getitems(bookstr, data)
    flag = 0

    for item in items:
        if item[0] is not None and len(item[0]) > 0:
            categoryurl = 'http://mebook.cc/{}.html'.format(index)
            category = getweb(categoryurl, header)
            cateitem = getitems(categorystr, category)

            bigclass = cateitem and cateitem[0][1] or ''
            smallclass = cateitem and cateitem[0][0] or ''

            sql = 'insert into books (bname,address,bsize,author,download,passwd,bigclass,smallclass) values("{}","{}","{}","{}","{}","{}","{}","{}")'.format(
                item[0], url, item[1], item[2], item[4], item[3], bigclass, smallclass)
            logger.info(sql)
            bookDB.execue(sql)
            bookDB.commit()
            logger.info(url + "抓取到内容")
            flag = 1
    if flag <= 0:
        logger.info(url + "无内容")


def getitems(compilestr, data):
    pattern = re.compile(compilestr, re.DOTALL)
    items = re.findall(pattern, data)
    return items


def getweb(url, header):
    response = requests.get(url, headers=header)
    data = response.text
    return data


def savefile(con):
    for content in con:
        file_object.write(content)


def main():
    url = "http://mebook.cc/download.php?id="
    for i in range(2000, 20000):  # 20000
        getinfo(url + str(i), i)
        time.sleep(2)
    file_object.close()
    bookDB.close()


if __name__ == '__main__':
    main()
