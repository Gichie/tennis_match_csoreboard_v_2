"""
Application logging configuration module.

Configures logging with console output and file rotation.
Creates a directory for storing logs if it does not exist.
"""

import logging
import os
from logging.handlers import RotatingFileHandler


def setup_logger() -> None:
    """
    Sets up and returns the configured logger.

    Creates the 'logs' directory to store log files,
    configures console output and a file with rotation when
    the maximum size (2 MB) is reached.

    :return: None
    """
    log_format = '%(asctime)s - %(levelname)s - %(message)s'
    # Setting up basic logging
    logging.basicConfig(level=logging.INFO, format=log_format)

    # Setting up a file handler with rotation
    # # Sets the name of the directory where logs will be stored
    log_dir = 'logs'

    # Creates the specified directory (and all intermediate directories, if necessary)
    # The exist_ok=True parameter means that if the directory already exists, the code will not throw an error
    os.makedirs(log_dir, exist_ok=True)

    # Generates a full path to a log file by combining the directory name and file name.
    log_file = os.path.join(log_dir, 'app.log')

    file_handler = RotatingFileHandler(log_file, maxBytes=512 * 512 * 4, backupCount=2)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(logging.Formatter(log_format))

    # Adding a file handler to the root logger
    logging.getLogger().addHandler(file_handler)
    # Setting the level for the root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    root_logger.propagate = True
