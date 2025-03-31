from uuid import UUID, uuid4
from typing import Optional 
from server.connections import UnitOfWork
from server.adapters.schemas import Owner, Model
from server.adapters.modules import Modules
from server.adapters.metrics import Metrics
from server.adapters.iterations import Iterations

class Models:
    def __init__(self, uow: UnitOfWork, owner: Optional[Owner] = None):
        self.uow = uow
        self.owner = owner

    @property
    def db(self):
        return self.uow.db['models']
        
    async def create(self, hash: str, name: str) -> Model:
        assert self.owner, "Owner necessary for this operation."
        id = uuid4()
        await self.db.insert_one({'id': str(id), 'hash': hash, 'name': name, 'epoch':0, 'owner': str(self.owner.id)}) 
        return Model(
            id=id,
            hash=hash,
            name=name,
            epoch=0,
            modules=Modules(self.uow, Owner(id)),
            metrics=Metrics(self.uow, Owner(id)),
            iterations=Iterations(self.uow, Owner(id))
        )

    async def read(self, *, hash: str) -> Optional[Model]:
        assert self.owner, "Owner necessary for this operation."
        data = await self.db.find_one({'hash': hash, 'owner': str(self.owner.id)})
        if data:
            return Model(
                id=UUID(data['id']),
                hash=data['hash'],
                name=data['name'],
                epoch=data['epoch'],
                modules=Modules(self.uow, Owner(UUID(data['id']))),
                metrics=Metrics(self.uow, Owner(UUID(data['id']))),
                iterations=Iterations(self.uow, Owner(UUID(data['id'])))
            )
        else:
            return None

    async def delete(self, id: UUID):
        await self.db.delete_one({'id': str(id)})

    async def get(self, id: UUID) -> Optional[Model]:
        data = await self.db.find_one({'id': str(id)})
        if data:
            return Model(
                id=UUID(data['id']),
                hash=data['hash'],
                name=data['name'],
                epoch=data['epoch'],
                modules=Modules(self.uow, Owner(UUID(data['id']))),
                metrics=Metrics(self.uow, Owner(UUID(data['id']))),
                iterations=Iterations(self.uow, Owner(UUID(data['id'])))
            )
        else:
            return None
    
    async def update(self, id: UUID, epoch: int) -> Model:    
        await self.db.update_one({'id': str(id)}, {'$set': {'epoch': epoch}})  
        return await self.get(id)

    async def list(self) -> list[Model]:
        assert self.owner, "Owner necessary for this operation."
        cursor = self.db.find({'owner': str(self.owner.id)}) 
        return [ Model(
            id=UUID(data['id']),
            hash=data['hash'],
            name=data['name'],
            epoch=data['epoch'],
            modules=Modules(self.uow, Owner(UUID(data['id']))),
            metrics=Metrics(self.uow, Owner(UUID(data['id']))),
            iterations=Iterations(self.uow, Owner(UUID(data['id'])))
        ) async for data in cursor]
    

    async def clear(self):
        assert self.owner, "Owner necessary for this operation."
        await self.db.delete_many({'owner': str(self.owner.id)}) 