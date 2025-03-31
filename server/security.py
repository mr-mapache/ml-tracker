from uuid import UUID
from pydantic import BaseModel
from fastapi import Request

class User(BaseModel):
    id: UUID

async def user(request: Request) -> User:
    ### To be implemented retrieving an user given api key in headers.
    return User(id=UUID('0a178a4e-5280-4065-ba42-08f877c59e03'))