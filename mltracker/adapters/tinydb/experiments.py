from os import path, makedirs
from uuid import uuid4
from typing import Optional
from tinydb import TinyDB, where
from mltracker.ports.experiments import Experiment
from mltracker.ports.experiments import Experiments as Collection

class Experiments(Collection):
    def __init__(self, database: TinyDB):
        self.database = database
        self.table = self.database.table('experiments')

    def read(self, name: str) -> Optional[Experiment]:
        result = self.table.get(where('name') == name)
        return Experiment(id=result['id'], name=result['name']) if result else None
    
    def create(self, name: str) -> Experiment:
        result = self.table.get(where('name') == name)
        if result:
            raise ValueError(f'Experiment with name {name} already exists')
        id = uuid4()
        self.table.insert({'id': str(id), 'name': name})
        return Experiment(id=id, name=name)

    def update(self, experiment: Experiment):
        self.table.update({'name': experiment.name}, where('id') == str(experiment.id))

    def delete(self, name: str):
        self.table.remove(where('name') == name)
    
    def list(self) -> list[Experiment]:
        return [Experiment(id=result['id'], name=result['name']) for result in self.table.all()]