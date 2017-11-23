# encoding=UTF-8
from loggerConfig import Config
import requests
import re
import time
import random
from util.getProxy import proxy

targetPath = 'books/books1000.txt'
file_object = open(targetPath, 'a')
logger = Config.loggerinfo()


def getinfo(url):
    headers = [
        'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.94 Safari/537.36',
        'Mozilla/5.0 (Linux; Android 4.0.4; Galaxy Nexus Build/IMM76B) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.133 Mobile Safari/535.19']
    header_index = random.randint(0,len(headers) - 1)
    header = {'User-Agent': headers[header_index]}

    # proxys = proxy.getdata()
    # proxy_index = random.randint(0,len(proxys))
    # proxy_a = {"http": 'http://103.251.167.18:1080'}

    # response = requests.get(url, proxies=proxy_a, headers=header)
    response = requests.get(url, headers=header)
    data = response.text
    string = r'<div.*?desc">.*?<p>文件名称：(.*?)</p>.*?<p>(.*?)</p>.*?<p>(.*?)</p>.*?<p>(.*?)</p>.*?' + \
             r'<p>(.*?)</p>.*?<p>网盘密码：百度网盘密码：(.*?)(&nbsp;)*</p>.*?<div class="list">.*?href="(.*?)"'
    pattern = re.compile(string, re.DOTALL)
    items = re.findall(pattern, data)
    ret = []

    for item in items:
        if item[0] is not None and len(item[0]) > 0:
            bookcon = '图书地址：' + url + '\n' + \
                      '书名：' + item[0] + '\n' + \
                      item[1] + '\n' + item[2] + '\n' + item[3] + '\n' + item[4] + '\n' + \
                      '网盘密码：' + item[5] + \
                      '\n下载地址：' + item[7] + '\n\n'
        logger.info(url + "抓取到内容")
        ret.append(bookcon)

    if len(ret) <= 0:
        logger.info(url + "无内容")
    savefile(ret)


def savefile(con):
    for content in con:
        file_object.write(content)


def main():
    url = "http://mebook.cc/download.php?id="
    for i in range(1010, 2000):  # 20000
        getinfo(url + str(i))
        time.sleep(1)
    file_object.close()


if __name__ == '__main__':
    main()
