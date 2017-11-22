# encoding=UTF-8
import requests
import json
from loggerConfig import Config

logger = Config.loggerinfo()


class proxy:
    logger.info("proxy")

    def getdata(self):
        data = requests.get(url='http://172.29.18.187:8000/').text
        proxy = json.loads(data)
        logger.info("获取到代理ip个数" + str(len(proxy)))
        result = []
        for line in proxy:
            ipString = 'http://' + str(line[0]) + ':' + str(line[1])
            result.append(ipString)
        return result


if __name__ == '__main__':
    proxy.getdata()
