import logging
import inspect


def make_logger(file="logfile.log", level=logging.NOTSET):
    # Get module name of caller
    caller = inspect.stack()[1]
    module = inspect.getmodule(caller[0])
    name = module.__name__

    # Create logger and set logging level
    logger = logging.getLogger(name)
    logger.setLevel(level)

    formatter = logging.Formatter(
        " %(asctime)s :: %(levelname)s :: %(name)s :: %(message)s"
    )

    # Create file and stream handler, file handler filters level, stream handler outputs all
    file_handler = logging.FileHandler(file)
    file_handler.setLevel(level)
    file_handler.setFormatter(formatter)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    return logger
