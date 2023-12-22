from app.api.models import ItunesDataSchema
from app.db import itunes_data, database


async def post(payload: ItunesDataSchema):
    query = itunes_data.insert().values(title=payload.title,
                                        description=payload.description)
    return await database.execute(query=query)


async def get(persistent_id: str):
    query = itunes_data.select().where(
        persistent_id == itunes_data.c.persistent_id)
    return await database.fetch_one(query=query)


async def get_all():
    query = itunes_data.select()
    return await database.fetch_all(query=query)


async def put(id: int, payload: ItunesDataSchema):
    query = (
        itunes_data
        .update()
        .where(id == itunes_data.c.id)
        .values(title=payload.title, description=payload.description)
        .returning(itunes_data.c.id)
    )
    return await database.execute(query=query)


async def delete(id: int):
    query = itunes_data.delete().where(id == itunes_data.c.id)
    return await database.execute(query=query)
