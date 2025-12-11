from fastapi import APIRouter, HTTPException

from typing import List

import db.select, db.update
import config
from . import document

from datetime import datetime, timezone

from . import schemes


router = APIRouter()


@router.post("/")
async def add_doc(id: str, title: str, user_id: int) -> schemes.IdDocument:
    # Check data
    check_res = await document.check_info(id, title, user_id)
    if isinstance(check_res, str):
        raise HTTPException(status_code=400, detail=check_res)
    
    # Add document to db
    now = datetime.now(timezone.utc)
    id = await db.update.__init__(
        """
        INSERT INTO documents (id, title, user_id, created_at)
        VALUES (%s, %s, %s, %s)
        """,
        (id, title, user_id, now)
    )
    
    return {"id": id}


@router.get("/")
async def get_doc(id: str) -> schemes.GetDocument:
    # Check id
    res = await db.select.__init__(
        """
        SELECT title, user_id FROM documents
        WHERE id = %s
        """,
        (id,)
    )

    if len(res)==0:
        raise HTTPException(status_code=401, detail="Invalid id")

    title, user_id = res[0]

    return {"title": title, "user_id": user_id}


@router.patch("/")
async def edit_doc_title(id: str, title: str) -> schemes.Complete:
    # Check id
    res = await db.select.__init__(
        """
        SELECT id FROM documents
        WHERE id = %s
        """,
        (id,)
    )

    if len(res)==0:
        raise HTTPException(status_code=401, detail="Invalid id")
    
    # Update document
    await db.update.__init__(
        """
        UPDATE documents
        SET title = %s
        WHERE id = %s
        """,
        (title, id)
    )

    return {"complete": True}


@router.delete("/")
async def delete_doc(id: str) -> schemes.Complete:
    await db.update.__init__(
        """
        DELETE FROM documents
        WHERE id = %s
        """,
        (id,)
    )

    return {"complete": True}


@router.get("/user")
async def get_users_docs(user_id: str) -> schemes.Documents:
    # Check id
    res = await db.select.__init__(
        """
        SELECT id, title FROM documents
        WHERE user_id = %s
        ORDER BY id ASC
        """,
        (user_id,)
    )

    return {
        "docs": [
            {"id": id, "title": title} for id, title in res
        ]
    }