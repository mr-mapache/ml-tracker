from typing import Optional
from typing import Any
from abc import ABC, abstractmethod
from dataclasses import dataclass, asdict
from copy import deepcopy
from mltracker.ports.modules import Module
from mltracker.ports.metrics import Metrics
from mltracker.ports.iterations import Iterations

@dataclass
class Aggregate:
    id: Any
    epochs: int
    modules: dict[str, Module]
    metrics: Metrics
    iterations: Iterations

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, Aggregate):
            return False
        return asdict(self) == asdict(value)
    
    def __hash__(self) -> int:
        return hash(self.id)

class Aggregates(ABC):

    @abstractmethod    
    def create(self, id: str, modules: list[Module]) -> Aggregate:...

    @abstractmethod
    def put(self, id: str, epoch: int, modules: list[Module]):...
    
    @abstractmethod    
    def get(self, id: str) -> Optional[Aggregate]:...
    
    @abstractmethod    
    def patch(self, id: str, epochs: int):...
    
    @abstractmethod    
    def remove(self, aggregate: Aggregate):...
