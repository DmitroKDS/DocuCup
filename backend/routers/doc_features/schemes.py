from pydantic import BaseModel
from typing import Optional


class Response(BaseModel):
    res: str