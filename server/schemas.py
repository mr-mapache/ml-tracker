from uuid import UUID
from typing import Annotated
from typing import Optional
from typing import Any
from pydantic import BaseModel
from pydantic import Field 

class Schema(BaseModel):
    ...

class Experiment(Schema):  
    id: Annotated[UUID, Field(...)]
    name: Annotated[str, Field(...)]

class Model(Schema):
    id: Annotated[UUID, Field(...)]
    hash: Annotated[Optional[str], Field(...)]
    name: Annotated[Optional[str], Field(...)]
    epoch: Annotated[int, Field(default=0)]

class Metric(Schema):
    name: Annotated[str, Field(...)]
    value: Annotated[Any, Field(...)]
    epoch: Annotated[int, Field(...)]
    phase: Annotated[str, Field(...)]

class Module(Schema):
    hash: Annotated[str, Field(...)]
    type: Annotated[str, Field(...)]
    name: Annotated[str, Field(...)]
    epoch: Annotated[int, Field(...)]
    arguments: Annotated[dict[str, Any], Field(...)]

class Iteration(Schema):
    hash: Annotated[str, Field(...)]
    phase: Annotated[str, Field(...)]
    epoch: Annotated[int, Field(...)]
    arguments: Annotated[dict[str, Any], Field(...)]