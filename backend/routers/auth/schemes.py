from pydantic import BaseModel
from typing import Optional

class UserToken(BaseModel):
    token: str