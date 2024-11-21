from abc import ABC
from abc import abstractmethod
from typing import Any
from dataclasses import dataclass, asdict

@dataclass
class Metric:
    name: str
    value: Any
    batch: int
    epoch: int
    phase: str

class Metrics(ABC):

    @abstractmethod
    def add(self, metric: Metric): ...

    @abstractmethod
    def list(self) -> list[Metric]: ...
    
    @abstractmethod
    def clear(self): ...