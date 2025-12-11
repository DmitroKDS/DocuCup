from fastapi import APIRouter, HTTPException

import db.select, db.update
import config

from . import schemes


router = APIRouter()

@router.get("/")
async def get_credits(id: int) -> schemes.Credits:
    # Get right password
    res = await db.select.__init__(
        """
        SELECT credits FROM users
        WHERE id = %s
        """,
        (id,)
    )

    # Check email
    if len(res)==0:
        raise HTTPException(status_code=401, detail="Invalid user id")
    credits = res[0][0]

    return {"credits": credits}


@router.post("/")
async def add_credits(id: int, credits: int) -> schemes.Credits:
    # Get right password
    res = await db.update.__init__(
        """
        UPDATE users
        SET credits = credits + %s
        WHERE id = %s
        """,
        (credits, id)
    )

    return {"credits": credits}


@router.patch("/")
async def minus_credits(id: int, credits: int) -> schemes.Credits:
    # Get right password
    res = await db.update.__init__(
        """
        UPDATE users
        SET credits = credits - %s
        WHERE id = %s
        """,
        (credits, id)
    )

    return {"credits": credits}