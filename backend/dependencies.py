from typing import Annotated

from fastapi import Header, HTTPException

import config


async def get_token_header(x_token: Annotated[str, Header()]):
    if x_token != config.TOKEN:
        raise HTTPException(status_code=400, detail="X-Token header invalid")


async def get_query_token(token: str):
    if token != config.TOKEN:
        raise HTTPException(status_code=400, detail="X-Token header invalid")