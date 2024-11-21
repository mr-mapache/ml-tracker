from typing import Any
from abc import ABC, abstractmethod
from dataclasses import dataclass, asdict, field
from mltracker.ports.modules import Module

@dataclass
class Dataset:
    hash: str
    name: str
    arguments: dict[str, Any]

@dataclass
class Iteration:
    hash: str
    phase: str
    epoch: int
    dataset: Dataset
    arguments: dict[str, Any]
    modules: list[Module]

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, Iteration):
            return False
        return self.hash == value.hash
    
    def __hash__(self) -> int:
        return hash(self.hash)
    

class Iterations(ABC):
    
    @abstractmethod
    def put(self, iteration: Iteration): ...

    @abstractmethod
    def list(self) -> list[Iteration]: ...

    @abstractmethod
    def clear(self): ...