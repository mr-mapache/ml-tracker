from uuid import UUID
from typing import Protocol
from typing import Optional
from server.ports.models import Models

class Experiment(Protocol):
    
    @property
    def id(self) -> UUID:
        """
        Globally unique identifier for an experiment.
        """

    @property
    def name(self) -> str:
        """
        Locally unique identifier for an experiment
        """

    @property
    def models(self) -> Models:
        """
        Each experiment owns a collection of models.
        """


class Experiments(Protocol):
    models: Models

    async def create(self, id: Optional[UUID], name: str) -> Experiment:
        ...

    async def get(self, id: UUID) -> Optional[Experiment]:
        ...

    async def read(self, name: str) -> Optional[Experiment]:
        ...

    async def list(self) -> list[Experiment]:
        ...

    async def update(self, id: UUID, name: str) -> Experiment:
        ...

    async def delete(self, id: UUID) -> None:
        ...

    async def clear(self) -> None:
        ...