# -*- coding: utf-8 -*-
import pymysql


class MysqlUtil:
    def __init__(self, host, port, username, password, db):
        self.__port = port
        self.__host = host
        self.__dbname = db
        self.__db = None
        self.__cursor = None
        self.__username = username
        self.__passwd = password

    def initconn(self):
        self.__db = pymysql.connect(
            host=self.__host,
            port=self.__port,
            user=self.__username,
            passwd=self.__passwd,
            db=self.__dbname,
            charset='utf8'
        )
        self.__cursor = self.__db.cursor()

    def close(self):
        self.__cursor.close()
        self.__db.close()

    def commit(self):
        self.__db.commit()

    def execue(self, sql):
        if self.__db is None:
            self.initconn()
        return self.__cursor.execute(sql)

    def fetchmany(self, data):
        return self.__cursor.fetchmany(data)