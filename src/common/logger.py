import logging


FORMAT = '%(asctime)s  %(name)s:%(lineno)s -> (%(levelname)s)  %(message)s'
logging.basicConfig(format=FORMAT, level=logging.DEBUG)


def module_logger(n=__name__):
    """Return logger object to use"""
    logger = logging.getLogger(n)
    logger.setLevel(logging.DEBUG)
    handler = logging.StreamHandler()
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter(FORMAT)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.propagate = 0
    return logger

