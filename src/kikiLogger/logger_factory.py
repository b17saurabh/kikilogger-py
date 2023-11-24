import logging
import json

from .console_appender import ConsoleAppender
from .elasticsearch_appender import ElasticsearchAppender
from .json_appender import JsonAppender
from .opensearch_appender import OpenSearchAppender
from .txt_file_appender import TxtFileAppender


class MultiAppenderLogger(logging.Logger):
    _instance = None

    def __new__(cls, name, level=logging.NOTSET):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, name, level=logging.NOTSET):
        if not getattr(self, '_is_initialized', False):
            super().__init__(name, level)
            self._is_initialized = True

    async def info_async(self, message, extra=None):
        self.appender.log(logging.INFO, message, extra)
        self.log(logging.INFO, message, extra)

    async def debug_async(self, message, extra=None):
        self.log(logging.DEBUG, message, extra)

    async def error_async(self, message, extra=None):
        self.log(logging.ERROR, message, extra)
    
    async def warning_async(self, message, extra=None):
        self.log(logging.WARNING, message, extra)
    
    async def critical_async(self, message, extra=None):
        self.log(logging.CRITICAL, message, extra)

def getLogger(config_path="loggerConfig.json"):
    with open(config_path) as config_file:
        log_config = json.load(config_file)

    logger = MultiAppenderLogger(log_config.get("name", "multi_appender_logger"))
    logger.setLevel(logging.NOTSET)  # Set the logger's level to NOTSET initially

    for appender_config in log_config.get("appenders", []):
        appender_type = appender_config.get("type", "console")

        if appender_type == "console":
            appender = ConsoleAppender()
        elif appender_type == "txt_file":
            appender = TxtFileAppender(appender_config.get("file_path", "log.txt"))
        elif appender_type == "json":
            appender = JsonAppender(appender_config.get("file_path", "log.json"))
        elif appender_type == "elasticsearch":
            appender = ElasticsearchAppender(
                appender_config.get("es_host", ["localhost:9200"]),
                appender_config.get("index", "logs"),
                appender_config.get("es_credentials", None),
            )
        elif appender_type == "opensearch":
            appender = OpenSearchAppender(
                appender_config.get("os_host", ["localhost:9200"]),
                appender_config.get("index", "logs"),
                appender_config.get("os_credentials", None),
            )
        else:
            raise ValueError(f"Unknown appender type: {appender_type}")

        formatter = logging.Formatter(appender_config.get("format", "%(asctime)s - %(levelname)s - %(message)s"))
        appender.setFormatter(formatter)
        logger.addHandler(appender)

    return logger
