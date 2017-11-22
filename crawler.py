# encoding=UTF-8
from loggerConfig import Config
import requests
import re
import time

targetPath = 'books/books.txt'
file_object = open(targetPath, 'a')
logger = Config.loggerinfo()


def getinfo(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36'}
    response = requests.get(url)
    data = response.text
    string = r'<div.*?desc">.*?<p>文件名称：(.*?)</p>.*?<p>(.*?)</p>.*?<p>(.*?)</p>.*?<p>(.*?)</p>.*?' + \
             r'<p>(.*?)</p>.*?<p>网盘密码：百度网盘密码：(.*?)(&nbsp;)*</p>.*?<div class="list">.*?href="(.*?)"'
    pattern = re.compile(string, re.DOTALL)
    items = re.findall(pattern, data)
    ret = []

    for item in items:
        if item[0] is not None and len(item[0]) > 0:
            bookcon = '图书地址：' + url + '\n' +\
                      '书名：' + item[0] + '\n' +\
                      item[1] + '\n' + item[2] + '\n' + item[3] + '\n' + item[4] + '\n' +\
                      '网盘密码：' + item[5] +\
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
    for i in range(1000, 20000):  # 20000
        getinfo(url + str(i))
        time.sleep(1)
    file_object.close()


if __name__ == '__main__':
    main()
