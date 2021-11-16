from os import name
from sqlalchemy import Column, Table
from sqlalchemy.sql.sqltypes import Integer, String
from sqlalchemy import create_engine, MetaData
from pydantic import BaseModel
from typing import Optional

SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
meta = MetaData()

conn = engine.connect()

# Table
cats = Table(
    "cats",
    meta,
    Column("id", Integer, primary_key=True),
    Column("name", String(255),),
    Column("keeper", String(255)),
    Column("breed", String(255)),
)

# Schema


class Cat(BaseModel):
    id: Optional[int]
    name: str
    keeper: str
    breed: str


# Create table
meta.create_all(engine)

## CRUD OPERATIONS ##

# Create cat


def create_cat(cat: Cat):
    new_cat = {"name": cat.name, "keeper": cat.keeper, "breed": cat.breed}
    result = conn.execute(cats.insert().values(new_cat))
    return conn.execute(cats.select().where(cats.c.id == result.lastrowid)).first()

# Get all cats


def get_cats(offset, limit):
    all_cats = conn.execute(cats.select()).fetchall()[offset:offset+limit]
    return all_cats

# Get cat from id


def get_cat(id: str):
    return conn.execute(cats.select().where(cats.c.id == id)).first()

# Update cat


def update_cat(cat: Cat, id: int):
    conn.execute(
        cats.update()
        .values(name=cat.name, keeper=cat.keeper, breed=cat.breed)
        .where(cats.c.id == id)
    )
    return conn.execute(cats.select().where(cats.c.id == id)).first()

# Delete cat


def delete_cat(id: int):
    conn.execute(cats.delete().where(cats.c.id == id))
    return conn.execute(cats.select().where(cats.c.id == id)).first()
