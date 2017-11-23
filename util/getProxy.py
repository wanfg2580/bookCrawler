# encoding=UTF-8
import requests
import json
from loggerConfig import Config

logger = Config.loggerinfo()


class proxy:
    logger.info("proxy")

    def getdata(self):
        data = requests.get(url='http://172.29.18.45:8000/').text
        proxy = json.loads(data)
        logger.info("获取到代理ip个数" + str(len(proxy)))
        result = []
        for line in proxy:
            ipString = 'http://' + str(line[0]) + ':' + str(line[1])
            result.append(ipString)
        logger.info(result)
        return result

proxy=proxy()