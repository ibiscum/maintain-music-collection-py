from app.api.models import ItunesDataSchema, ItunesDataDB
from app.db import itunes_data, itunes_data_play_month, database


async def post(payload: ItunesDataDB):
    query = itunes_data.insert().values(
        persistent_id=payload.persistent_id,
        track_id=payload.track_id,
        track_name=payload.track_name,
        artist=payload.artist,
        album_artist=payload.album_artist,
        album=payload.album,
        genre=payload.genre,
        disc_number=payload.disc_number,
        disc_count=payload.disc_count,
        track_number=payload.track_number,
        track_count=payload.track_count,
        album_year=payload.album_year,
        date_modified=payload.date_modified,
        date_added=payload.date_added,
        volume_adjustment=payload.volume_adjustment,
        play_count=payload.play_count,
        play_date_utc=payload.play_date_utc,
        artwork_count=payload.artwork_count,
        md5_id=payload.md5_id
    )
    return await database.execute(query=query)


async def get(persistent_id: str):
    query = itunes_data.select().where(
        persistent_id == itunes_data.c.persistent_id)
    return await database.fetch_one(query=query)


async def get_all():
    query = itunes_data.select()
    return await database.fetch_all(query=query)


async def put(persistent_id: str, payload: ItunesDataSchema):
    query = (itunes_data.update().where(
        persistent_id == itunes_data.c.persistent_id)
        .values(
            track_id=payload.track_id,
            track_name=payload.track_name,
            artist=payload.artist,
            album_artist=payload.album_artist,
            album=payload.album,
            genre=payload.genre,
            disc_number=payload.disc_number,
            disc_count=payload.disc_count,
            track_number=payload.track_number,
            track_count=payload.track_count,
            album_year=payload.album_year,
            date_modified=payload.date_modified,
            date_added=payload.date_added,
            volume_adjustment=payload.volume_adjustment,
            play_count=payload.play_count,
            play_date_utc=payload.play_date_utc,
            artwork_count=payload.artwork_count,
            md5_id=payload.md5_id
        )
        .returning(itunes_data.c.persistent_id)
    )
    return await database.execute(query=query)


async def delete(persistent_id: str):
    query = itunes_data.delete().where(
        persistent_id == itunes_data.c.persistent_id)
    return await database.execute(query=query)
