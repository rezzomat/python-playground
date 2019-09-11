import logging
import traceback


class Log:
    def __init__(self, pg):
        self.pg = pg

    async def insert(self, level, info):
        await self.pg.execute("INSERT INTO Log (date, level, record) VALUES (CURRENT_TIMESTAMP, $1, $2)", level, info)


class AsyncpgHandler(logging.Handler):

    def __init__(self, pg):
        self.pg = pg
        self.log = Log(pg)

    def emit(self, record):
        trace = None
        exc = record.__dict__['exc_info']
        if exc:
            trace = traceback.format_exc()
            self.log.insert(record.__dict__['levelname'], record.__dict__['msg'])


def get_logger(name, pg):
    FORMAT = '%(asctime)-15s %(command)s %(action)s'
    logging.basicConfig(format=FORMAT)
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    db_handler = AsyncpgHandler(pg)
    logger.addHandler(db_handler)
    return logger


FORMAT = '%(asctime)-15s %(command)s %(action)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger('asdf')
logger.setLevel(logging.DEBUG)
