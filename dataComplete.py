# -*- coding: utf-8 -*-
from util.DBUtil import MysqlUtil
from loggerConfig import Config
import re
import random
import requests
import time


logger = Config.loggerinfo()
bookDB = MysqlUtil('localhost', 3306, 'root', 'root', 'book')
categorystr = r'<a.*?rel="category tag">(.*?)</a>.*?<a.*?rel="category tag">(.*?)</a>'
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

def tranferData(data):
    info = bookDB.fetchmany(data)
    for line in info:
        id = line[0]
        index = line[2].split('=')[1]
        categoryurl = 'http://mebook.cc/{}.html'.format(index)
        logger.info(categoryurl)
        category = getweb(categoryurl, header)
        cateitem = getitems(categorystr, category)

        bigclass = cateitem and cateitem[1] or ''
        smallclass = cateitem and cateitem[0] or ''
        time.sleep(1)

        sql = 'update books set bigclass = "{}",smallclass="{}" where id="{}"'.format(
            bigclass, smallclass, id)
        logger.info(sql)
        bookDB.execue(sql)
        bookDB.commit()


def complete():
    sql = 'select * from books where bigclass=""'
    data = bookDB.execue(sql)
    bookDB.commit()
    tranferData(data)
    bookDB.close()

if __name__ == '__main__':
    complete()