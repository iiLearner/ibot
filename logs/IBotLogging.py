import logging


class IBotLogging(logging.Handler):
    def emit(self, record):
        print(record.getMessage())
