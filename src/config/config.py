"""
Application configuration module.

Loads settings from environment variables and the .env file.
Contains database connection parameters and other
configuration constants.

Use this module to import configuration
parameters into other parts of the application.
"""

import os
import re

from dotenv import load_dotenv

# Load variables from .env
load_dotenv()

# Database settings
DB_USER: str | None = os.getenv("DB_USER")
DB_PASSWORD: str | None = os.getenv("DB_PASSWORD")
DB_HOST: str | None = os.getenv("DB_HOST")
DB_NAME: str | None = os.getenv("DB_NAME")
DB_PORT: str | None = os.getenv("DB_PORT")

#  Form a URI to connect to the database
DATABASE_URI: str = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset=utf8mb4"

# Number of matches per page
PER_PAGE = 10

SCORE_DIFF = 2
MIN_GAMES = 6
MIN_SETS: int = 2
MIN_TIE_BREAK_POINTS = 7

MAX_LENGTH = 64
NAME_PATTERN = re.compile(r'^[^\W\d_]+(?:-[^\W\d_]+)*$', re.UNICODE)
MIN_PAGE: int = 1
