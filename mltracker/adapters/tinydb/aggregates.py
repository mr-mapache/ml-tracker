from typing import Any
from typing import Optional
from mltracker.adapters.tinydb.metrics import Metrics
from mltracker.adapters.tinydb.iterations import Iterations
from mltracker.ports.aggregates import Aggregates as Collection
from mltracker.ports.aggregates import Aggregate, asdict
from mltracker.ports.modules import Module
from tinydb import TinyDB, where

class Aggregates(Collection):
    def __init__(self, owner: Any, database: TinyDB):
        self.owner = str(owner)
        self.database = database
        self.table = self.database.table('aggregates')
        
    def create(self, id: str, modules: list[Module]) -> Aggregate:
        if self.table.contains((where('owner') == self.owner) & (where('id') == id)):
            raise ValueError(f'Aggregate with id {id} already exists')
        
        aggregate = Aggregate(
            id=id, 
            epochs=0, 
            modules=modules,
            metrics=Metrics(id, self.database), 
            iterations=Iterations(id, self.database)
        )

        self.table.insert({
            'owner': self.owner,
            'id': id,
            'epochs': 0,
            'modules': [asdict(module) for module in modules]
        })
        return aggregate
    
    def get(self, id: str) -> Optional[Aggregate]:
        result = self.table.get((where('owner') == self.owner) & (where('id') == id))
        if result:
            return Aggregate(
                **{key: value for key, value in result.items() if key != 'owner' and key != 'modules'},
                modules=[Module(**module) for module in result['modules']],
                metrics=Metrics(id, self.database), 
                iterations=Iterations(id, self.database)
            )
        return None
    
    def patch(self, id: str, epochs: int):
        self.table.update({'epochs': epochs}, (where('owner') == self.owner) & (where('id') == id))
    
    def list(self) -> list[Aggregate]:
        results = self.table.search(where('owner') == self.owner)
        return [Aggregate(
            **{key: value for key, value in result.items() if key != 'owner' and key != 'modules'},
            modules=[Module(**module) for module in result['modules']],
            metrics=Metrics(result['id'], self.database), 
            iterations=Iterations(result['id'], self.database)
        ) for result in results]

    def remove(self, aggregate: Aggregate):
        aggregate.metrics.clear(), aggregate.iterations.clear()
        self.table.remove((where('owner') == self.owner) & (where('id') == aggregate.id))