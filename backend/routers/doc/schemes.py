from pydantic import BaseModel
from typing import List


class IdDocument(BaseModel):
    id: int

class GetDocument(BaseModel):
    title: str
    user_id: int

class Complete(BaseModel):
    complete: bool

class UserDocument(BaseModel):
    id: str
    title: str

class Documents(BaseModel):
    docs: List[UserDocument]