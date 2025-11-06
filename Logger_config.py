# Project: abcapstonefa25istTeam1
# Purpose Details: Logger code, which imports logging code and automatically creates folders
# Course: Fall 2025 Abington Capstone Project Quantum Cryptosystem
# Author: Madisyn
# Date Developed: 11/05/2025
# Last Date Changed: 11/06/2025
# Revision: 1.0

import logging
import os
from datetime import datetime

# Sets up and returns a configured logger that writes both to console
# and to a timestamped log file
def setup_logger(name, log_dir="logs", level=logging.INFO):

    # Create logs directory if it doesn’t exist already
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # Create a timestamped log filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_filename = os.path.join(log_dir, f"capstone_{timestamp}.log")

    # Configure a consistent log format
    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # File handler (writes all messages)
    file_handler = logging.FileHandler(log_filename, mode="a")
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.DEBUG)

    # Console handler (shows INFO+ messages)
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(level)

    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # Avoid duplicate handlers if setup_logger is called more than once
    if not logger.handlers:
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    logger.debug(f"Logger initialized for {name}")
    return logger
