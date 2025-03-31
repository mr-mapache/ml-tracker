from typing import Optional
from uuid import UUID
from uuid import uuid4 
from server.connections import UnitOfWork
from server.adapters.schemas import Owner, Experiment
from server.adapters.models import Models

class Experiments:
    def __init__(self, uow: UnitOfWork, owner: Owner):
        self.uow = uow
        self.owner = owner
        self.models = Models(self.uow)

    @property
    def db(self):
        return self.uow.db['experiments']

    async def create(self, id: Optional[UUID], name: str) -> Experiment:
        id = id or uuid4()
        await self.db.insert_one({'id': str(id or uuid4), 'name': name, 'owner': str(self.owner.id)})
        return Experiment(
            id=id, 
            name=name,
            models=Models(self.uow, Owner(id=id))
        )


    async def get(self, id: UUID) -> Optional[Experiment]:
        data = await self.db.find_one({"id": str(id), 'owner': str(self.owner.id)})
        if data:
            experiment = Experiment(
                id=UUID(data['id']),
                name=data['name'],
                models=Models(self.uow, Owner(id=id))
            ) 
            return experiment
        return None
    

    async def read(self, *, name: str) -> Optional[Experiment]:
        data = await self.db.find_one({"name": str(name), 'owner': str(self.owner.id)})
        if data:
            experiment = Experiment(
                id=UUID(data['id']),
                name=data['name'],
                models=Models(self.uow, Owner(id=data['id']))
            ) 
            return experiment
        return None
    

    async def update(self, id: UUID, name: str) -> Experiment: 
        await self.db.update_one({'id': str(id), 'owner': str(self.owner.id)}, {'$set': {'name': name}})
        return Experiment(
            id=id, 
            name=name,
            models=Models(self.uow, Owner(id=id))
        )
    

    async def list(self) -> list[Experiment]:
        cursor = self.db.find({'owner': str(self.owner.id)}) 
        return [Experiment(
            id=UUID(data['id']),
            name=data['name'],
            models=Models(self.uow, Owner(id=data['id']))
        ) async for data in cursor]
    

    async def delete(self, id: UUID) -> None:
        await self.db.delete_one({'id': str(id), 'owner': str(self.owner.id)})


    async def clear(self) -> None:
        await self.db.delete_many({'owner': str(self.owner.id)})