from pydantic import BaseModel, Field
from datetime import date, datetime, time, timedelta


class ItunesDataSchema(BaseModel):
    track_id: int
    track_name: str
    artist: str
    album_artist: str
    album: str
    genre: str
    disc_number: int
    disc_count: int
    track_number: int
    track_count: int
    album_year: date
    date_modified: datetime
    date_added: datetime
    volume_adjustment: int
    play_count: int
    play_date_utc: datetime
    artwork_count: int
    md5_id: str


class ItunesDataDB(ItunesDataSchema):
    persistent_id: str
