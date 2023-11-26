import logging

class TxtFileAppender(logging.FileHandler):
    def __init__(self, filename):
        super().__init__(filename)
