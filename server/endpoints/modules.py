from uuid import UUID
from typing import Annotated
from typing import Any
from typing import Optional

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException, status
from fastapi import Path
from fastapi import Query
from fastapi import Body
from fastapi import Response

from server.ports.modules import Modules
from server.endpoints.experiments import repository, Experiments
from server.schemas import Module

router = APIRouter() 

async def module(
    hash: Annotated[str, Path(...)], 
    type: Annotated[str, Body(...)], 
    name: Annotated[str, Body(...)], 
    epoch: Annotated[int, Body(...)],
    arguments: Annotated[dict[str, Any], Body(...)]
)-> Module:
    return Module(hash=hash, type=type, name=name, epoch=epoch, arguments=arguments)

async def modules(id: Annotated[UUID, Path(...)], experiments: Annotated[Experiments, Depends(repository)]) -> Modules:
    model = await experiments.models.get(id) 
    if not model:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Model with ID {id} not found")
    return model.modules

@router.put('/models/{id}/modules/{hash}/')
async def put_module(module: Annotated[Module, Depends(module)], modules: Annotated[Modules, Depends(modules)]):
    await modules.put(module.hash, module.type, module.name, module.epoch, module.arguments)
    return Response(status_code=status.HTTP_204_NO_CONTENT) 


# Annotated[Optional[str], Query(default=None)] won't work because of fastapi unsolved bug.
#@router.get('/models/{id}/modules/')
#async def list_modules(type: Annotated[Optional[str], Query(default=None)], modules: Annotated[Modules, Depends(modules)]) -> list[Module]:
#    list = await modules.list(type)
#    return [Module(hash=module.hash, type=module.type, name=module.name, arguments=module.arguments) for module in list]

@router.get('/models/{id}/modules/')
async def list_modules(modules: Annotated[Modules, Depends(modules)]) -> list[Module]:
    list = await modules.list()
    return [Module(hash=module.hash, type=module.type, name=module.name, epoch=module.epoch, arguments=module.arguments) for module in list]


@router.get('/models/{id}/modules')
async def query_modules(modules: Annotated[Modules, Depends(modules)], type: Optional[str] = Query(default=None)) -> list[Module]:
    list = await modules.list(type)
    return [Module(hash=module.hash, type=module.type, name=module.name, epoch=module.epoch, arguments=module.arguments) for module in list]