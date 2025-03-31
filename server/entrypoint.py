from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import FastAPI
from fastapi import Depends

from server.settings import Settings
from server.connections import Database
from server.connections import UnitOfWork
from server.security import user, User
from server.adapters.schemas import Owner
from server.endpoints import experiments
from server.endpoints import models
from server.endpoints import iterations
from server.endpoints import modules
from server.endpoints import metrics
from server.adapters.experiments import Experiments

settings = Settings()
database = Database(settings)

@asynccontextmanager
async def lifespan(api):
    await database.setup()
    try:
        yield
    finally:
        await database.teardown()

async def repository(user: Annotated[User, Depends(user)]):
    owner = Owner(user.id)
    async with UnitOfWork(database) as uow:
        yield Experiments(uow, owner)        
        await uow.commit()

api = FastAPI(lifespan=lifespan)
api.include_router(experiments.router)
api.include_router(models.router)
api.include_router(modules.router)
api.include_router(metrics.router)
api.include_router(iterations.router)
api.dependency_overrides[experiments.repository] = repository