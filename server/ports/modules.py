from typing import Protocol
from typing import Any
from typing import Optional

class Module(Protocol):

    @property
    def type(self) -> str:
        """
        A tag for the kind of module module you are storing, ej. "neural network". 
        """

    @property
    def hash(self) -> str:
        """
        A locally unique identifier for the module. 
        """

    @property
    def name(self) -> str:
        """
        The name of the module to store. It DOES NOT act as a unique identifier.
        ej. "perceptron"
        """

    @property
    def arguments(self) -> dict[str, Any]:
        """
        The arguments wich the model was initialized with. ej. "{'in_size'=784, 'out_size'=10}
        """

    @property
    def epoch(self) -> int:
        """
        A model may vary some of it's modules during training. The epoch of a module is the last
        epoch of the model in which the module was included.
        """

class Modules(Protocol): 

    async def put(self, hash: str, type: str, name: str, epoch: int, arguments: dict[str, Any]) -> None:
        ...

    async def list(self, type: Optional[str] = None) -> list[Module]:
        ...

    async def clear(self) -> None:
        ...