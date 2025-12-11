from fastapi import Depends, FastAPI

import db.create
from dependencies import get_query_token, get_token_header
from internal import admin
from routers import auth
from routers import credits
from routers import doc
from routers import doc_features

import db
import asyncio

import logging

app = FastAPI(dependencies=[Depends(get_query_token)])

logger = logging.getLogger("fastapi")
logger.setLevel(logging.INFO)

app.include_router(
    auth.router,
    prefix = '/auth',
    tags=["Auth (/auth)"]
)
app.include_router(
    credits.router,
    prefix = '/credits',
    tags=["Credits (/credits)"]
)
app.include_router(
    doc.router,
    prefix = '/doc',
    tags=["Document (/doc)"]
)
app.include_router(
    doc_features.router,
    prefix = '/doc',
    tags=["Document features (/doc)"]
)
app.include_router(
    admin.router,
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(get_token_header)],
    responses={418: {"description": "I'm a teapot"}},
)

asyncio.run(db.create.__init__())

@app.get("/")
async def root():
    return {"message": "Hello it is DocuCup backend!"}

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app)