from typing import Optional
from typing import Any
from abc import ABC, abstractmethod
from dataclasses import dataclass

@dataclass
class Experiment:
    id: Optional[Any]
    name: str

class Experiments(ABC):

    @abstractmethod
    def create(self, name: str) -> Experiment: ...

    @abstractmethod
    def read(self, name: str) -> Optional[Experiment]: ...

    @abstractmethod
    def delete(self, name: str): ...

    @abstractmethod
    def list(self) -> list[Experiment]: ...