from motor.motor_asyncio import AsyncIOMotorClient

from server.settings import Settings

class Database:
    client: AsyncIOMotorClient
    
    def __init__(self, settings: Settings):
        self.client = AsyncIOMotorClient(host=settings.database.host, port=settings.database.port)

    async def setup(self):
        self.db = self.client['mltracker']

    async def teardown(self):
        self.client.close()

    async def drop(self):
        await self.client.drop_database('mltracker')


class UnitOfWork:
    def __init__(self, database: Database):
        self.client = database.client
        self.db = database.db

    async def begin(self):
        self.session = await self.client.start_session()
        self.session.start_transaction()

    async def commit(self):
        await self.session.commit_transaction()

    async def rollback(self):
        await self.session.abort_transaction()

    async def close(self):
        await self.session.end_session()

    async def __aenter__(self):
        await self.begin()
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        if exc_type:
            await self.rollback()
        else:
            await self.commit() 
        await self.close()