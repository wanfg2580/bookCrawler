# encoding=UTF-8
import logging
import logging.config
from os import path


class Config:
    @staticmethod
    def loggerinfo():
        log_file_path = path.join(path.dirname(path.abspath(__file__)), './logs/logger.conf')
        logging.config.fileConfig(log_file_path)

        logger = logging.getLogger()
        return logger
