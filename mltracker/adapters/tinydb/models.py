from uuid import uuid4, UUID
from typing import Optional
from tinydb import TinyDB, where
from typing import override

from mltracker.ports.models import Models as Collection
from mltracker.ports.models import Model

from mltracker.ports.owner import Owner
from mltracker.adapters.tinydb.modules import Modules
from mltracker.adapters.tinydb.metrics import Metrics
from mltracker.adapters.tinydb.iterations import Iterations

class Models(Collection):
    def __init__(self, database: TinyDB, owner: Owner):
        self.database = database
        self.owner = owner
        self.table = self.database.table('models')

    @override
    def create(self, hash: str, name: str) -> Model:
        id = uuid4()
        if self.table.search(where('experiment') == str(self.owner.id) and where('hash') == hash):
            raise ValueError(f'Model with hash {hash} already exists') 
        self.table.insert({'id': str(id), 'hash': hash, 'name': name, 'epoch': 0} | {'experiment': str(self.owner.id)})
        return Model(
            id=id,
            hash=hash, 
            name=name,
            epoch=0,  
            modules=Modules(self.database, Owner(id=id)),
            metrics=Metrics(self.database, Owner(id=id)),
            iterations=Iterations(self.database, Owner(id=id))
        )

    @override
    def update(self, hash: str, epoch: int) -> Model:
        self.table.update({'epoch': epoch}, where('experiment') == str(self.owner.id) and where('hash') == hash)
        return self.read(hash)

    @override
    def read(self, hash: str) -> Optional[Model]: 
        model = self.table.get(where('experiment') == str(self.owner.id) and where('hash') == hash) 
        return Model( 
            id=UUID(model['id']),
            hash=model['hash'],
            name=model['name'], 
            epoch = model['epoch'], 
            modules=Modules(self.database, Owner(id=UUID(model['id']))),
            metrics=Metrics(self.database, Owner(id=UUID(model['id']))),
            iterations=Iterations(self.database, Owner(id=UUID(model['id'])))
        ) if model else None

    @override
    def get(self, id: UUID) -> Optional[Model]:
        model = self.table.get(where('id') == str(id)) 
        return Model(
            id=id, 
            hash=model['hash'],
            name=model['name'], 
            epoch = model['epoch'], 
            modules=Modules(self.database, Owner(id=id)),
            metrics=Metrics(self.database, Owner(id=id)),
            iterations=Iterations(self.database, Owner(id=id))
        ) if model else None

    @override
    def delete(self, id: UUID) -> None:  
        if not self.get(id):
            raise ValueError(f'Model with hash {hash} does not exist') 
        self.table.remove(where('id') == str(id))

    @override
    def list(self) -> list[Model]:
        models = self.table.search(where('experiment') == str(self.owner.id))
        return [Model(
            id=UUID(model['id']),
            hash=model['hash'],  
            name=model['name'],
            epoch=model['epoch'],  
            modules=Modules(self.database, Owner(id=UUID(model['id']))),
            metrics=Metrics(self.database, Owner(id=UUID(model['id']))),
            iterations=Iterations(self.database, Owner(id=UUID(model['id'])))
        ) for model in models]
    
    @override
    def clear(self): 
        for model in self.list():
            self.delete(model.id)