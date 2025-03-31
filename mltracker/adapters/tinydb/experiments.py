from uuid import uuid4, UUID
from typing import override
from typing import Optional 
from tinydb import TinyDB, where

from mltracker.ports.owner import Owner
from mltracker.ports.experiments import Experiment
from mltracker.ports.experiments import Experiments as Repository 
from mltracker.adapters.tinydb.models import Models

class Experiments(Repository):
    def __init__(self, database: TinyDB):
        self.database = database
        self.table = self.database.table('experiments')    
        
    
    @override
    def create(self, name: str) -> Experiment:
        if self.table.search(where('name') == name):
            raise ValueError(f"Experiment with name {name} already exists")
        id = uuid4()
        self.table.insert({'id': str(id), 'name': name})
        return Experiment(
            id=id, 
            name=name, 
            models=Models(self.database, owner=Owner(id=id))
        )
    

    @override    
    def read(self, *, name) -> Optional[Experiment]: 
        data = self.table.get(where('name') == name)  
        return Experiment(
            id=UUID(data['id']),
            name=data['name'], 
            models=Models(self.database, owner=Owner(id=UUID(data['id'])))
        ) if data else None
    

    @override
    def update(self, id: UUID, name: str) -> Experiment:
        self.table.update({'name': name}, where('id') == str(id))
        return Experiment(
            id=id,
            name=name, 
            models=Models(self.database, owner=Owner(id=id))
        )
    
    @override
    def delete(self, id: UUID): 
        document = self.table.get(where('id') == str(id))
        if not document:
            raise ValueError(f"Experiment with id {id} not found")

        experiment = self.read(name=document['name'])
        experiment.models.clear()
        self.table.remove(where('id') == str(id))


    @override
    def clear(self) -> None:
        self.database.table('models').truncate()
        self.database.table('modules').truncate()
        self.database.table('metrics').truncate()
        self.table.truncate()

    @override
    def list(self) -> list[Experiment]:
        return [Experiment(
            id=UUID(data['id']), 
            name=data['name'], 
            models=Models(self.database, owner=Owner(id=UUID(data['id'])))
        ) for data in self.table.all()]