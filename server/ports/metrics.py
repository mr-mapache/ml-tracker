from typing import Any
from typing import Protocol


class Metric(Protocol):

    @property
    def name(self) -> str:
        """
        The name of the metric. ej. 'accuracy'.
        """

    @property
    def value(self) -> Any:
        """
        The value of the metric, ej. [[1., 0.][0., 1.]] or 0.1
        """

    @property
    def epoch(self) -> int:
        """
        The epoch of the model for wich the metric was recorded.
        """ 

    @property
    def phase(self) -> str:
        """
        The phase of the iteration for wich the metric was recorded.
        """
        

class Metrics(Protocol):

    async def add(self, name: str, value: Any, epoch: int, phase: str) -> None:
        ...
        

    async def list(self) -> list[Metric]:
        ...


    async def clear(self) -> None:
        ...