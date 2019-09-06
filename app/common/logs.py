"""
Configuring and initializing loggers
"""

import logging
import os
from app import project_dir

LOG_DIR_PATH = os.path.join(project_dir, "log")
MAIN_LOG_FILE_PATH = os.path.join(LOG_DIR_PATH, "main.log")
LOG_FORMAT = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
# Every time we start the app, the old logs are overriden
LOGGING_FILE_MODE = 'w'
LOG_LEVEL = logging.DEBUG


def init_log():
    """
    Initializing basic log configuration.
    Logs are written to the 'log' folder under the project's root folder
    """
    if not os.path.exists(LOG_DIR_PATH):
        os.makedirs(LOG_DIR_PATH)

    logging.basicConfig(filename=MAIN_LOG_FILE_PATH,
                        level=LOG_LEVEL,
                        format=LOG_FORMAT,
                        filemode=LOGGING_FILE_MODE)
