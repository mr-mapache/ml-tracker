from typing import Any 
from server.connections import UnitOfWork
from server.adapters.schemas import Owner, Iteration

class Iterations:
    
    def __init__(self, uow: UnitOfWork, owner: Owner):
        self.uow = uow
        self.owner = owner

    @property
    def db(self):
        return self.uow.db['iterations']
    
    async def put(self, hash: str, phase: str, epoch: int, arguments: dict[str, Any]) -> None:
        await self.db.update_one({'owner': str(self.owner.id), 'hash': hash}, {'$set':  
            {'hash': hash, 'phase': phase, 'epoch': epoch, 'arguments': arguments, 'owner': str(self.owner.id) } },
        upsert=True)   

    async def list(self) -> list[Iteration]:
        cursor = self.db.find({'owner': str(self.owner.id)})
        return [Iteration(
            hash=data['hash'],
            phase=data['phase'],
            epoch=data['epoch'],
            arguments=data['arguments']
        ) async for data in cursor]

    async def clear(self) -> None:
        await self.db.delete_many({'owner': str(self.owner.id)})
        