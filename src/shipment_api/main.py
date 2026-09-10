from fastapi import FastAPI, HTTPException, Depends,status
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel
from typing import List,Optional,Any
from scalar_fastapi import get_scalar_api_reference


app = FastAPI(title="FastAPI with SQLAlchemy + Pydantic + Postgresql")


@app.get("/")
async def root():
    return {"message": "Shipment API is running!"}



@app.get("/scalar",include_in_schema=False)
def get_scalar():
    return get_scalar_api_reference(openapi_url=app.openapi_url, title="Shipment API")
