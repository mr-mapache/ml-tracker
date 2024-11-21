from typing import Any
from mltracker.ports.iterations import Iterations as Collection
from mltracker.ports.iterations import Iteration, asdict
from mltracker.ports.modules import Module
from mltracker.ports.iterations import Dataset
from tinydb import TinyDB, where


class Iterations(Collection):
    def __init__(self, owner: Any, database: TinyDB):
        self.owner = str(owner)
        self.database = database
        self.table = self.database.table('iterations')

    def put(self, iteration: Iteration):
        self.table.upsert({
            'owner': self.owner, 
            'hash': iteration.hash, 
            'iteration': {key: value for key, value in asdict(iteration).items() if key != 'hash'}
        }, where('hash') == iteration.hash)

    def list(self) -> list[Iteration]:
        results = self.table.search(where('owner') == self.owner)
        return [Iteration(
            hash=result['hash'],
            phase=result['iteration']['phase'],
            epoch=result['iteration']['epoch'],
            dataset=Dataset(**result['iteration']['dataset']),
            arguments=result['iteration']['arguments'],
            modules=[Module(**module) for module in result['iteration']['modules']],
        ) for result in results]
                          
    def clear(self):
        self.table.remove(where('owner') == self.owner)