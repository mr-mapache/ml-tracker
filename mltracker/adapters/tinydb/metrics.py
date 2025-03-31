from typing import override

from tinydb import TinyDB, where
from cattrs import structure
from cattrs import unstructure

from mltracker.ports.owner import Owner
from mltracker.ports.metrics import Metric
from mltracker.ports.metrics import Metrics as Collection

class Metrics(Collection):
    def __init__(self, database: TinyDB, owner: Owner):
        self.owner = owner
        self.database = database
        self.table = self.database.table('metrics')
    
    @override
    def add(self, metric: Metric):
        self.table.insert(unstructure(metric) | {'model': str(self.owner.id)})

    @override
    def list(self) -> list[Metric]:
        metrics = self.table.search(where('model') == str(self.owner.id))
        return [structure({key: value for key, value in metric.items() if key != 'model'}, Metric) for metric in metrics]
    
    @override
    def clear(self):
        self.table.remove(where('model') == str(self.owner.id))