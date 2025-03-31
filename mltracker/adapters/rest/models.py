from uuid import uuid4, UUID
from typing import Optional
from typing import override
from requests import post, put, patch, get, delete

from mltracker.ports.models import Models as Collection
from mltracker.ports.models import Model
from mltracker.ports.owner import Owner
from mltracker.adapters.tinydb.modules import Modules
from mltracker.adapters.tinydb.metrics import Metrics
from mltracker.adapters.tinydb.iterations import Iterations

class Models(Collection):
    def __init__(self, uri: str, owner: Owner):
        self.uri = uri
        self.owner = owner 

    @override
    def create(self, hash: str, name: str) -> Model:
        raise NotImplementedError

    @override
    def update(self, hash: str, epoch: int) -> Model:
        raise NotImplementedError

    @override
    def read(self, hash: str) -> Optional[Model]: 
        raise NotImplementedError

    @override
    def get(self, id: UUID) -> Optional[Model]:
        raise NotImplementedError
    
    @override
    def delete(self, id: UUID) -> None:  
        raise NotImplementedError

    @override
    def list(self) -> list[Model]:
        raise NotImplementedError
    

    @override
    def clear(self): 
        raise NotImplementedError