"""Configuration management using python-dotenv."""

import os
from dotenv import load_dotenv

# Load environment variables from a .env file into the system environment
load_dotenv()


class Config:
    """Centralized configuration settings for the calculator application."""

    # Directory where log files are stored
    LOG_DIR = os.getenv("CALCULATOR_LOG_DIR", "logs")

    # Directory where calculation history is stored
    HISTORY_DIR = os.getenv("CALCULATOR_HISTORY_DIR", "data")

    # Full path to the history CSV file
    HISTORY_FILE = os.path.join(HISTORY_DIR, "history.csv")

    # Full path to the log file
    LOG_FILE = os.path.join(LOG_DIR, "calculator.log")

    # Maximum number of history records to retain
    MAX_HISTORY_SIZE = int(os.getenv("CALCULATOR_MAX_HISTORY_SIZE", "50"))

    # Enable or disable automatic history saving
    AUTO_SAVE = os.getenv("CALCULATOR_AUTO_SAVE", "true").lower() == "true"

    # Number of decimal places used for rounding results
    PRECISION = int(os.getenv("CALCULATOR_PRECISION", "4"))

    # Maximum allowed numeric input value
    MAX_INPUT_VALUE = float(os.getenv("CALCULATOR_MAX_INPUT_VALUE", "1e9"))

    # Default file encoding used for reading/writing files
    DEFAULT_ENCODING = os.getenv("CALCULATOR_DEFAULT_ENCODING", "utf-8")