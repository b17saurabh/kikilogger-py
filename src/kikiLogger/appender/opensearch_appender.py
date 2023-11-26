import datetime
import logging
from opensearchpy import OpenSearch

class OpenSearchAppender(logging.Handler):
    def __init__(self, os_host, index, os_credentials=None):
        super().__init__()

        self.os_host = os_host
        self.index = index
        self.os_credentials = os_credentials
        if self.os_credentials:
            self.username = self.os_credentials['username']
            self.password = self.os_credentials['password']
        self.client = OpenSearch(
            hosts=[self.os_host], http_auth=(self.username, self.password))


    def log(self, record):
        log_entry = self.format(record)
        index_name = f'{self.index}-{datetime.now().strftime("%Y-%m-%d")}'
        self.client.index(index=index_name,
                            doc_type = '_doc',
                            body=log_entry)
