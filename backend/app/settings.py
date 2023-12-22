# settings.py
import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '../../.env')
load_dotenv(dotenv_path)

POSTGRES_HOST = os.environ.get("POSTGRES_HOST", "localhost")
POSTGRES_DB = os.environ.get("POSTGRES_DB")
POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD")
ITUNES_LIBRARY_FILE = os.environ.get("ITUNES_LIBRARY_FILE")
ITUNES_MUSIC_DIR = os.environ.get("ITUNES_MUSIC_DIR")
DATABASE_URL = os.environ.get("DATABASE_URL") 
