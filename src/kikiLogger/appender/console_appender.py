import logging


class ConsoleAppender(logging.StreamHandler):
    def __init__(self):
        super().__init__()
