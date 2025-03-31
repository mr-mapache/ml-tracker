from typing import Protocol
from typing import Any
  
from typing import Any
from typing import Optional 
from server.connections import UnitOfWork
from server.adapters.schemas import Owner, Module

class Modules:    
    def __init__(self, uow: UnitOfWork, owner: Owner):
        self.uow = uow
        self.owner = owner

    @property
    def db(self):
        return self.uow.db['modules']

    async def put(self, hash: str, type: str, name: str, epoch: int, arguments: dict[str, Any]) -> None:
        await self.db.update_one({'hash': hash, 'owner': str(self.owner.id)}, {'$set': {
            'hash': hash, 'type': type, 'name': name, 'epoch': epoch, 'arguments': arguments, 'owner': str(self.owner.id)
        }}, upsert=True)


    async def list(self, type: Optional[str] = None) -> list[Module]:
        cursor = self.db.find({'owner': str(self.owner.id), 'type': type}) if type else self.db.find({'owner': str(self.owner.id)})
        return [ Module(
            hash=data['hash'],
            type=data['type'],
            name=data['name'],
            epoch=data['epoch'],
            arguments=data['arguments']
        ) async for data in cursor]

    async def clear(self) -> None:
        await self.db.delete_many({'owner': str(self.owner.id)})