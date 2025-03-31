from uuid import UUID
from typing import Protocol
from typing import Any
from typing import Optional
from server.ports.metrics import Metrics
from server.ports.modules import Modules
from server.ports.iterations import Iterations


class Model(Protocol):
    """
    A model refers not only the module that was trained, but the whole aggregate,
    it can have tokenizers, loss functions, as modules as well. 
    """

    @property
    def id(self) -> UUID:
        """
        Globally unique identifier a the model.
        """

    @property
    def hash(self) -> str:
        """ 
        Locally unique identifier for a model.
        """ 

    @property
    def name(self) -> str:
        """
        The name of the model. It DOES NOT acts like
        an identifier of the model. 
        """

    @property
    def epoch(self) -> int:
        """
        The current epoch of the model.
        """

    @property
    def metrics(self) -> Metrics:
        """
        Each model owns a collection of metrics.
        """
        
    @property
    def modules(self) -> Modules:
        """
        Each model owns a collection of modules.
        """

    @property
    def iterations(self) -> Iterations:
        """
        Each models owns a collection of iterations. 
        """


class Models(Protocol):
 
    async def create(self, hash: str, name: str) -> Model:
        ...

    async def read(self, *, hash: str) -> Optional[Model]:
        ...

    async def update(self, id: UUID, epoch: int) -> Model:
        ...

    async def delete(self, id: UUID):
        ...

    async def get(self, id: UUID) -> Optional[Model]:
        ...

    async def list(self) -> list[Model]:
        ...

    async def clear(self):
        ...