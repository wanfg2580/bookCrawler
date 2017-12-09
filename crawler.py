# -*- coding: utf-8 -*-
from loggerConfig import Config
import requests
import re
import time
import random
from util.DBUtil import MysqlUtil

logger = Config.loggerinfo()
bookDB = MysqlUtil('localhost', 3306, 'root', 'root', 'book')

bookstr = r'<div.*?desc">.*?<p>文件名称：(.*?)</p>.*?<p>文件大小：(.*?)</p>.*?<p>作者信息：(.*?)</p>.*?' + \
          r'<p>网盘密码：百度网盘密码：(.*?)&nbsp;.*?<div class="list">.*?href="(.*?)"'

categorystr = r'<div class="left">.*?<a.*?rel="category tag">(.*?)</a>.*?<a.*?rel="category tag">(.*?)</a>'


def getinfo(url, index):
    headers = [
        'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.94 Safari/537.36',
        'Mozilla/5.0 (Linux; Android 4.0.4; Galaxy Nexus Build/IMM76B) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.133 Mobile Safari/535.19',
        'Mozilla/5.0 (Linux; Android 4.1.1; Nexus 7 Build/JRO03D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Safari/535.19',
        'Mozilla/5.0 (Linux; U; Android 4.0.4; en-gb; GT-I9300 Build/IMM76D) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30',
        'Mozilla/5.0 (Linux; U; Android 2.2; en-gb; GT-P1000 Build/FROYO) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1',
        'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:21.0) Gecko/20100101 Firefox/21.0',
        'Mozilla/5.0 (Android; Mobile; rv:14.0) Gecko/14.0 Firefox/14.0',
        'Mozilla/5.0 (iPad; CPU OS 5_0 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 > > Mobile/9A334 Safari/7534.48.3',
        'Mozilla/5.0 (iPod; U; CPU like Mac OS X; en) AppleWebKit/420.1 (KHTML, like Gecko) Version/3.0 Mobile/3A101a Safari/419.3']
    header_index = random.randint(0, len(headers) - 1)
    header = {'User-Agent': headers[header_index]}

    # proxys = proxy.getdata()
    # proxy_index = random.randint(0,len(proxys))
    # proxy_a = {"http": 'http://103.251.167.18:1080'}

    # response = requests.get(url, proxies=proxy_a, headers=header)
    data = getweb(url, header)

    items = getitems(bookstr, data)
    flag = 0

    for i in range(0, len(items)):
        if '"' in items[i]:
            items[i] = items[i].replace('"', ' ')
    if items and len(items) > 0:
        categoryurl = 'http://mebook.cc/{}.html'.format(index)
        category = getweb(categoryurl, header)
        cateitem = getitems(categorystr, category)

        bigclass = cateitem and cateitem[1] or ''
        smallclass = cateitem and cateitem[0] or ''

        sql = 'insert into books (bname,address,bsize,author,download,passwd,bigclass,smallclass) values("{}","{}","{}","{}","{}","{}","{}","{}")'.format(
            items[0], url, items[1], items[2], items[4], items[3], bigclass, smallclass)
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
    result = []
    if items and len(items) > 0:
        for i in range(0, len(items[0])):
            result.append(items[0][i])
    return result


def getweb(url, header):
    response = requests.get(url, headers=header)
    data = response.text
    return data


def main():
    url = "http://mebook.cc/download.php?id="
    for i in range(19401, 20000):  # 20000
        getinfo(url + str(i), i)
        time.sleep(2)
    bookDB.close()


if __name__ == '__main__':
    main()
