from typing import Any 
from server.connections import UnitOfWork
from server.adapters.schemas import Owner, Metric

class Metrics:
    def __init__(self, uow: UnitOfWork, owner: Owner):
        self.uow = uow
        self.owner = owner

    @property
    def db(self):
        return self.uow.db['metrics']
         

    async def add(self, name: str, value: Any, epoch: int, phase: str) -> None:
        await self.db.insert_one(
            {'name': name, 'value': value, 'epoch': epoch, 'phase': phase, 'owner': str(self.owner.id)}
        )

    async def list(self) -> list[Metric]:
        cursor = self.db.find({'owner': str(self.owner.id)})
        return [Metric(
            name=data['name'], 
            value=data['value'], 
            phase=data['phase'], 
            epoch=data['epoch']
        ) async for data in cursor]
    

    async def clear(self) -> None:
        await self.db.delete_many({'owner': str(self.owner.id)})