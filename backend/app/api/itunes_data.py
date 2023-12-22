from typing import List

from fastapi import APIRouter, HTTPException, Path

from app.api import crud
from app.api.models import ItunesDataDB, ItunesDataSchema

router = APIRouter()


@router.post("/", response_model=ItunesDataDB, status_code=201)
async def create_entry(payload: ItunesDataSchema):
    persistent_id = await crud.post(payload)

    response_object = {
        "persistent_id": persistent_id,
        "title": payload.title,
        "description": payload.description,
    }
    return response_object


@router.get("/{persistent_id}/", response_model=ItunesDataDB)
async def read_entry(persistent_id: str = Path(..., ),):
    persistent_id = await crud.get(persistent_id)
    if not persistent_id:
        raise HTTPException(status_code=404, detail="Entry not found")
    return persistent_id


@router.get("/", response_model=List[ItunesDataDB])
async def read_all_entries():
    return await crud.get_all()


@router.put("/{persistent_id}/", response_model=ItunesDataDB)
async def update_note(payload: ItunesDataSchema, persistent_id: int = Path(..., gt=0),):
    note = await crud.get(persistent_id)
    if not note:
        raise HTTPException(status_code=404, detail="Entry not found")

    note_id = await crud.put(persistent_id, payload)

    response_object = {
        "id": note_id,
        "title": payload.title,
        "description": payload.description,
    }
    return response_object


@router.delete("/{id}/", response_model=ItunesDataDB)
async def delete_note(id: int = Path(..., gt=0)):
    note = await crud.get(id)
    if not note:
        raise HTTPException(status_code=404, detail="Entry not found")

    await crud.delete(id)

    return note
