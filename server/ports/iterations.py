from typing import Protocol
from typing import Any

class Iteration(Protocol):
    """
    An iteration refers to the occurrence of a machine model being processed. 
    Each repetition of this process constitutes a single iteration.
    """

    @property
    def hash(self) -> str:
        """
        A locally unique identifier for an iteration.
        """

    @property
    def phase(self) -> str:
        """
        The phase of the iteration process. ej. 'validation'. 
        """

    @property
    def epoch(self) -> int:
        """
        Refers to the epoch of the model, aka the number of times that
        a model was iterated on 'train' phase.
        """

    @property
    def arguments(self) -> dict[str, Any]:
        """
        Refers to the external parameters for wich the model was iterated on.
        ej. 'batch_size'. 
        """
 

class Iterations(Protocol):


    async def put(self, hash: str, phase: str, epoch: int, arguments: dict[str, Any]) -> None:
        ...

    async def list(self) -> list[Iteration]:
        ...

    async def clear(self) -> None:
        ...