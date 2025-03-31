from uuid import UUID
from typing import Any

from attrs import define 

from server.ports.models import Models
from server.ports.modules import Modules
from server.ports.metrics import Metrics
from server.ports.iterations import Iterations

@define
class Owner:
    id: UUID

@define
class Experiment:
    id: UUID
    name: str 
    models: Models

@define
class Model:
    id: UUID
    hash: str
    name: str
    epoch: int
    metrics: Metrics
    modules: Modules
    iterations: Iterations

@define
class Module:
    type: str
    hash: str
    name: str
    epoch: int
    arguments: dict[str, Any]

@define
class Metric:
    name: str
    value: float
    phase: str
    epoch: int

@define
class Iteration:
    hash: str
    phase: str
    epoch: int
    arguments: dict[str, Any]