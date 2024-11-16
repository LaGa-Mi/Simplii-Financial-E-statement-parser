import logging

def setup_logger(name: str, level=logging.INFO):
    """Function to setup a logger with the given name and log level."""
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s',  datefmt='%H:%M:%S')
    
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)
    
    return logger

def log_info(logger: logging.Logger, message: str):
    """Function to log an info message."""
    logger.info(message)

def log_warning(logger: logging.Logger, message: str):
    """Function to log a warning message."""
    logger.warning(message)

def log_error(logger: logging.Logger, message: str):
    """Function to log an error message."""
    logger.error(message)

def log_critical(logger: logging.Logger, message: str):
    """Function to log a critical message."""
    logger.critical(message)