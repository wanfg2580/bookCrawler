# -*- coding: utf-8 -*-
from util.DBUtil import MysqlUtil
bookDB = MysqlUtil('localhost', 3306, 'root', 'root', 'book')
sql ='insert into books (bname,address,bsize,author,download,passwd,bigclass,smallclass) VALUE ("{}","{}","{}","{}","{}","{}","{}","{}")'.format('水水水水', '7','7','7','7','7','7','7');
print(sql)
bookDB.execue(sql)
bookDB.close()