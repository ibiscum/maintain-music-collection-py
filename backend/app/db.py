# import os

from sqlalchemy import (
    Column,
    DateTime,
    Date,
    Integer,
    MetaData,
    String,
    Text,
    Table,
    create_engine
)

# from sqlalchemy.sql import func

from databases import Database
from app.settings import POSTGRES_DB_URL

# SQLAlchemy
engine = create_engine(POSTGRES_DB_URL)
metadata = MetaData()
itunes_data = Table(
    "itunes_data",
    metadata,
    Column("persistent_id", String(100), primary_key=True),
    Column("track_id", Integer),
    Column("track_name", Text),
    Column("artist", Text),
    Column("album_artist", Text),
    Column("album", Text),
    Column("genre", String(100)),
    Column("disc_number", Integer),
    Column("disc_count", Integer),
    Column("track_number", Integer),
    Column("track_count", Integer),
    Column("album_year", Date),
    Column("date_modified", DateTime),
    Column("date_added", DateTime),
    Column("volume_adjustment", Integer),
    Column("play_count", Integer),
    Column("play_date_utc", DateTime),
    Column("artwork_count", Integer),
    Column("md5_id", String(100))
)

itunes_data_play_month = Table(
    "itunes_data_play_month",
    metadata,
    Column("album_artist", Text),
    Column("play_at", DateTime),
    Column("play_count", Integer)
)

# databases query builder
database = Database(POSTGRES_DB_URL)
