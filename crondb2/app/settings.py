# settings.py
import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '../../.env')
load_dotenv(dotenv_path)

DB_HOST = os.environ.get("DB_HOST", "localhost")
DB_SCHEMA = os.environ.get("DB_SCHEMA")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
ITUNES_LIBRARY_FILE = os.environ.get("ITUNES_LIBRARY_FILE")
ITUNES_MUSIC_DIR = os.environ.get("ITUNES_MUSIC_DIR")
