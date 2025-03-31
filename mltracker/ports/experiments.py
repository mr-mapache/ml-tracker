from uuid import UUID 
from typing import Optional
from abc import ABC, abstractmethod
from attrs import define
from mltracker.ports.models import Models

@define
class Experiment: 
    id: UUID
    name: str 
    models: Models

class Experiments(ABC):

    @abstractmethod
    def create(self, name: str) -> Experiment:...

    @abstractmethod
    def read(self, **kwargs) -> Optional[Experiment]:...

    @abstractmethod
    def update(self, id: str, name: str) -> Experiment:...

    @abstractmethod
    def delete(self, id: str) -> None:...

    @abstractmethod
    def list(self) -> list[Experiment]:...

    @abstractmethod
    def clear(self) -> None:...