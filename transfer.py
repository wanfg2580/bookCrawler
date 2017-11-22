# encoding=UTF-8
import loggerConfig


def creazyRead():
    ms = open("books/books.txt")
    file = open("books/books_nourl.txt", "a")
    loggerConfig.logger.info("test")
    for line in ms.readlines():
        if '图书地址' in line or '适用版本' in line or '更新日期' in line or '作者信息' in line:
            continue
        file.write(line)


if __name__ == '__main__':
    creazyRead()