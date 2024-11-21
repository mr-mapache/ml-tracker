from abc import ABC
from abc import abstractmethod
from typing import Any
from typing import Optional
from dataclasses import dataclass, asdict

@dataclass
class Metric:
    name: str
    value: Any
    batch: Optional[int] = None
    epoch: Optional[int] = None
    phase: Optional[str] = None

class Metrics(ABC):

    @abstractmethod
    def add(self, metric: Metric): ...

    @abstractmethod
    def list(self) -> list[Metric]: ...
    
    @abstractmethod
    def clear(self): ...