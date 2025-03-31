from uuid import UUID
from abc import ABC, abstractmethod
from typing import Optional
from attrs import define 

from mltracker.ports.metrics import Metrics
from mltracker.ports.modules import Modules
from mltracker.ports.iterations import Iterations

@define
class Model:
    id: UUID
    hash: str
    name: str
    epoch: int  
    modules: Modules
    metrics: Metrics
    iterations: Iterations

class Models(ABC):

    @abstractmethod
    def create(self, hash: str, name: str) -> Model:
        ...

    @abstractmethod
    def read(self, *, hash: str) -> Optional[Model]:
        ...
        
    @abstractmethod
    def update(self, hash: str, epoch: int) -> Model:
        ...

    @abstractmethod
    def delete(self, hash: str):
        ...

    @abstractmethod
    def clear(self):
        ...

    @abstractmethod
    def list(self) -> list[Model]:
        ...