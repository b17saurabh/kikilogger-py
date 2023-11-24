import datetime
import logging
from elasticsearch import Elasticsearch


class ElasticsearchAppender(logging.Handler):
    def __init__(self, es_host, index, es_credentials=None):
        super().__init__()

        self.es_host = es_host
        self.index = index
        self.es_credentials = es_credentials
        if self.es_credentials:
            self.username = self.es_credentials['username']
            self.password = self.es_credentials['password']
        self.client = Elasticsearch(
            hosts=[self.es_host], http_auth=(self.username, self.password))

    def emit(self, record):
        log_entry = self.format(record)
        index_name = f'{self.index}-{datetime.now().strftime("%Y-%m-%d")}'
        self.client.index(index=index_name,
                          doc_type='_doc',
                          body=log_entry)
