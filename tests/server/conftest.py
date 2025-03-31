from pytest_asyncio import fixture
from uuid import UUID

from fastapi import FastAPI
from httpx import AsyncClient, ASGITransport

from server.settings import Settings
from server.connections import Database, UnitOfWork
from server.adapters.experiments import Experiments, Owner
from server.endpoints import experiments
from server.endpoints import models
from server.endpoints import modules
from server.endpoints import metrics
from server.endpoints import iterations

@fixture(scope='function')
def settings() -> Settings:
    return Settings()

@fixture(scope='function')
async def database(settings: Settings):
    database = Database(settings)
    try:
        await database.setup()
        yield database
    finally:
        await database.drop()
        await database.teardown()

@fixture(scope='function')
async def repository(database: Database):
    async with UnitOfWork(database) as uow:
        yield Experiments(uow, Owner(id=UUID('0a178a4e-5280-4065-ba42-08f877c59e03')))
        ### Owner mocks an actual User retrieved from security service from api key.
        await uow.commit()


@fixture(scope='function')
async def client(repository: Experiments): 
    api = FastAPI()
    api.include_router(experiments.router)
    api.include_router(models.router)
    api.include_router(modules.router)
    api.include_router(metrics.router)
    api.include_router(iterations.router)
    api.dependency_overrides[experiments.repository] = lambda: repository
    async with AsyncClient(transport=ASGITransport(api), base_url='http://testserver') as client:
        yield client