from typing import override

from tinydb import TinyDB, where
from cattrs import unstructure
from cattrs import structure

from mltracker.ports.owner import Owner
from mltracker.ports.iterations import Iteration
from mltracker.ports.iterations import Iterations as Collection

class Iterations(Collection):
    def __init__(self, database: TinyDB, owner: Owner):
        self.owner = owner
        self.database = database
        self.table = self.database.table('iterations')

    @override
    def add(self, iteration: Iteration):
        self.table.insert(unstructure(iteration) | {'owner': str(self.owner.id)})
    
    @override
    def put(self, iteration: Iteration):
        iterations = self.table.search(where('owner') == str(self.owner.id) and where('phase') == iteration.phase)
        if not iterations:
            self.table.insert(unstructure(iteration) | {'owner': str(self.owner.id)})
        elif iteration.hash == iterations[-1]['hash']:
            self.table.update(unstructure(iteration) | {'owner': str(self.owner.id)}, doc_ids=[iterations[-1].doc_id])
        else:
            self.table.insert(unstructure(iteration) | {'owner': str(self.owner.id)})

    @override
    def list(self) -> list[Iteration]:
        iterations = self.table.search(where('owner') == str(self.owner.id))
        return [structure({key: value for key, value in iteration.items() if key != 'owner'}, Iteration) for iteration in iterations]
    
    @override
    def clear(self):
        self.table.remove(where('owner') == str(self.owner.id))