import logging

FORMAT = '%(asctime)-15s %(command)s %(action)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger('asdf')
logger.setLevel(logging.DEBUG)
