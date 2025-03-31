from uuid import UUID
from typing import Annotated

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException, status
from fastapi import Path
from fastapi import Query
from fastapi import Body
from fastapi import Response

from server.ports.models import Models
from server.endpoints.experiments import repository, Experiments
from server.schemas import Model

router = APIRouter()

async def models(id: Annotated[UUID, Path(...)], experiments: Annotated[Experiments, Depends(repository)]) -> Models:
    experiment = await experiments.get(id) 
    if not experiment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Experiment with ID {id} not found")
    return experiment.models

@router.post('/experiments/{id}/models/', status_code=status.HTTP_201_CREATED)
async def create_model(hash: Annotated[str, Body(...)], name: Annotated[str, Body(...)], models: Annotated[Models, Depends(models)]) -> Model:
    if await models.read(hash=hash):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Model with hash {hash} already exists")
    
    created = await models.create(hash=hash, name=name)
    return Model(id=created.id, hash=created.hash, name=created.name, epoch=created.epoch)

@router.get('/experiments/{id}/models/')
async def list_models(models: Annotated[Models, Depends(models)]) -> list[Model]:
    return [Model(id=model.id, hash=model.hash, name=model.name, epoch=model.epoch) for model in await models.list()]

@router.get('/experiments/{id}/models')
async def query_model(hash: Annotated[str, Query(...)], models: Annotated[Models, Depends(models)]) -> Model:
    model = await models.read(hash=hash)
    if not model: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Model with hash {hash} not found")
    return Model(id=model.id, hash=model.hash, name=model.name, epoch=model.epoch)

@router.get('/models/{id}/')
async def get_model(id: Annotated[UUID, Path(...)], experiments: Annotated[Experiments, Depends(repository)]) -> Model:
    model = await experiments.models.get(id)
    if not model: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Model with ID {id} not found")
    return Model(id=model.id, hash=model.hash, name=model.name, epoch=model.epoch)

@router.patch('/models/{id}/')
async def update_model(id: Annotated[UUID, Path(...)], epoch: Annotated[int, Body(embed=True)], experiments: Annotated[Experiments, Depends(repository)]):
    model = await experiments.models.get(id)
    if not model: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Model with ID {id} not found")
    await experiments.models.update(id=id, epoch=epoch)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.delete('/models/{id}/')
async def delete_model(id: Annotated[UUID, Path(...)], experiments: Annotated[Experiments, Depends(repository)]):
    model = await experiments.models.get(id)
    if not model: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Model with ID {id} not found")
    await experiments.models.delete(id=id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)