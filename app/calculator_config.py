"""Configuration management using python-dotenv."""
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    LOG_DIR = os.getenv("CALCULATOR_LOG_DIR", "logs")
    HISTORY_DIR = os.getenv("CALCULATOR_HISTORY_DIR", "data")
    HISTORY_FILE = os.path.join(HISTORY_DIR, "history.csv")
    LOG_FILE = os.path.join(LOG_DIR, "calculator.log")
    
    MAX_HISTORY_SIZE = int(os.getenv("CALCULATOR_MAX_HISTORY_SIZE", "50"))
    AUTO_SAVE = os.getenv("CALCULATOR_AUTO_SAVE", "true").lower() == "true"
    PRECISION = int(os.getenv("CALCULATOR_PRECISION", "4"))
    MAX_INPUT_VALUE = float(os.getenv("CALCULATOR_MAX_INPUT_VALUE", "1e9"))
    DEFAULT_ENCODING = os.getenv("CALCULATOR_DEFAULT_ENCODING", "utf-8")