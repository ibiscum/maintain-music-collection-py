from typing import List

from fastapi import APIRouter, HTTPException, Path

from app.api import crud
from app.api.models import ItunesDataDB, ItunesDataSchema

router = APIRouter()


@router.post("/", response_model=ItunesDataDB, status_code=201)
async def create_entry(payload: ItunesDataDB):
    await crud.post(payload)

    response_object = {
        "persistent_id": payload.persistent_id,
        "track_id": payload.track_id,
        "track_name": payload.track_name,
        "artist": payload.artist,
        "album_artist": payload.album_artist,
        "album": payload.album,
        "genre": payload.genre,
        "disc_number": payload.disc_number,
        "disc_count": payload.disc_count,
        "track_number": payload.track_number,
        "track_count": payload.track_count,
        "album_year": payload.album_year,
        "date_modified": payload.date_modified,
        "date_added": payload.date_added,
        "volume_adjustment": payload.volume_adjustment,
        "play_count": payload.play_count,
        "play_date_utc": payload.play_date_utc,
        "artwork_count": payload.artwork_count,
        "md5_id": payload.md5_id
    }

    return response_object


@router.get("/{persistent_id}", response_model=ItunesDataDB)
async def read_entry(persistent_id: str = Path(..., ),):
    item = await crud.get(persistent_id)
    if not item:
        raise HTTPException(status_code=404, detail="Entry not found")
    return item


@router.get("/", response_model=List[ItunesDataDB])
async def read_all_entries():
    return await crud.get_all()


@router.put("/{persistent_id}", response_model=ItunesDataDB)
async def update_note(payload: ItunesDataSchema,
                      persistent_id: str = Path(..., ),):
    persistent_id = await crud.get(persistent_id)
    if not persistent_id:
        raise HTTPException(status_code=404, detail="Entry not found")

    persistent_id = await crud.put(persistent_id, payload)

    response_object = {
        "persistent_id": persistent_id,
        "track_id": payload.track_id,
        "track_name": payload.track_name,
        "artist": payload.artist,
        "album_artist": payload.album_artist,
        "album": payload.album,
        "genre": payload.genre,
        "disc_number": payload.disc_number,
        "disc_count": payload.disc_count,
        "track_number": payload.track_number,
        "track_count": payload.track_count,
        "album_year": payload.album_year,
        "date_modified": payload.date_modified,
        "date_added": payload.date_added,
        "volume_adjustment": payload.volume_adjustment,
        "play_count": payload.play_count,
        "play_date_utc": payload.play_date_utc,
        "artwork_count": payload.artwork_count,
        "md5_id": payload.md5_id
    }

    return response_object


@router.delete("/{persistent_id}", response_model=ItunesDataDB,
               summary="Delete Entry")
async def delete_note(persistent_id: str = Path(..., )):
    item = await crud.get(persistent_id)

    if not item:
        raise HTTPException(status_code=404, detail="Entry not found")

    await crud.delete(persistent_id)

    return item
