from fastapi import APIRouter, HTTPException

import db.select, db.update
import config
from . import user

import jwt
import uuid

from datetime import datetime, timedelta, timezone

from . import schemes


router = APIRouter()


@router.post("/")
async def add_user(email: str, password: str) -> schemes.UserToken:
    # Check data
    check_res = await user.check_info(email, password)
    if isinstance(check_res, str):
        raise HTTPException(status_code=400, detail=check_res)
    email, password = check_res

    # Add user to db
    now = datetime.now(timezone.utc)
    id = await db.update.__init__(
        """
        INSERT INTO users (email, password, credits, created_at)
        VALUES (%s, %s, %s, %s)
        """,
        (email, password, 100, now)
    )

    # Generate token
    token = jwt.encode(
        {
            "sub": id,
            "jti": str(uuid.uuid4()),
            "type": "access",
            "iat": now,
            "exp": now + timedelta(days=config.JWT_EXPIRES_PERIOD)
        },
        config.JWT_SECRET_KEY,
        algorithm="HS256"
    )

    return {"token": token}


@router.get("/")
async def get_user(email: str, password: str) -> schemes.UserToken:
    # Get right password
    res = await db.select.__init__(
        """
        SELECT id, password FROM users
        WHERE email = %s
        """,
        (email,)
    )

    # Check email
    if len(res)==0:
        raise HTTPException(status_code=401, detail="Invalid email")
    id, right_password = res[0]

    # Check password
    if right_password!=password:
        raise HTTPException(status_code=401, detail="Invalid password")

    # Generate token
    now = datetime.now(timezone.utc)
    token = jwt.encode(
        {
            "sub": str(id),
            "jti": str(uuid.uuid4()),
            "type": "access",
            "iat": now,
            "exp": now + timedelta(days=config.JWT_EXPIRES_PERIOD)
        },
        config.JWT_SECRET_KEY,
        algorithm="HS256"
    )

    return {"token": token}