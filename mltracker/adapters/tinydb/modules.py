from typing import override
from typing import Optional
from tinydb import TinyDB, where
from cattrs import structure, unstructure
from typing import Optional

from mltracker.ports.owner import Owner
from mltracker.ports.modules import Module
from mltracker.ports.modules import Modules as Collection 

class Modules(Collection):
    def __init__(self, database: TinyDB, owner: Owner):
        self.owner = owner
        self.database = database
        self.table = self.database.table('modules')
    
    @override
    def list(self, type: str) -> list[Module]:
        results = self.table.search(where('model') == str(self.owner.id) and where('type') == type)
        return [structure({key: value for key, value in result.items() if key != 'model'}, Module) for result in results]
        
    @override
    def last(self, type: str) -> Optional[Module]:
        modules = self.table.search(where('model') == str(self.owner.id) and where('type') == type)
        last = modules[-1] if modules else None
        return structure({key: value for key, value in last.items() if key != 'owner'}, Module) if last else None
    
    @override
    def put(self, module: Module):
        modules = self.table.search(where('model') == str(self.owner.id) and where('type') == module.type)
        if not modules:
            self.table.insert(unstructure(module) | {'model': str(self.owner.id)})
        elif module.hash == modules[-1]['hash']:
            self.table.update({'epoch': module.epoch}, doc_ids=[modules[-1].doc_id])
        else:
            self.table.insert(unstructure(module) | {'model': str(self.owner.id)})

    @override
    def clear(self):
        self.table.remove(where('model') == str(self.owner.id))