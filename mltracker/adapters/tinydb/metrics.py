from os import makedirs, path
from mltracker.ports.metrics import Metrics as Collection
from mltracker.ports.metrics import Metric, asdict
from tinydb import TinyDB, where

class Metrics(Collection):
    def __init__(self, owner: str, database: TinyDB):
        self.owner = str(owner)
        self.database = database
        self.table = self.database.table('metrics')
    
    def add(self, metric: Metric):
        self.table.insert({'owner': self.owner, **asdict(metric)})

    def list(self) -> list[Metric]:
        results = self.table.search(where('owner') == self.owner)
        return [Metric(**{key: value for key, value in result.items() if key != 'owner'}) for result in results]
    
    def clear(self):
        self.table.remove(where('owner') == self.owner)