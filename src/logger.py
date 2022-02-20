import logging

# Def logging class
def log_events():
    logger = logging.getLogger(__name__)

    # Check if there is a logger class defined already
    if not logger.hasHandlers():
        handler = logging.StreamHandler()
        fmt = '💬 %(levelname)s %(asctime)s %(filename)s %(funcName)s %(lineno)d %(message)s'
        formatter = logging.Formatter(fmt)
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    return logger