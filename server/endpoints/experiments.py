from uuid import UUID
from typing import Annotated

from fastapi import APIRouter
from fastapi import Depends
from fastapi import Response
from fastapi import HTTPException, status
from fastapi import Path
from fastapi import Query
from fastapi import Body

from server.schemas import Experiment
from server.ports.experiments import Experiments

router = APIRouter()

async def repository() -> Experiments:
    raise NotImplementedError("Overrides this dependency with a concrete implementation")

@router.post('/experiments/', status_code=status.HTTP_201_CREATED)
async def add_experiment(name: Annotated[str, Body(embed=True)], experiments: Annotated[Experiments, Depends(repository)]) -> Experiment: 
    if await experiments.read(name=name):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Experiment with name {name} already exists")
    model = await experiments.create(None, name)
    return Experiment(id=model.id, name=model.name)

@router.get('/experiments/{id}/')
async def get_experiment(id: Annotated[UUID, Path(...)], experiments: Annotated[Experiments, Depends(repository)]):
    model = await experiments.get(id)
    if not model:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Experiment already exists")
    return Experiment(id=model.id, name=model.name)

@router.get('/experiments/')
async def list_experiments(experiments: Annotated[Experiments, Depends(repository)]) -> list[Experiment]:
    models = await experiments.list()
    return [Experiment(id=model.id, name=model.name) for model in models]

@router.get('/experiments')
async def query_experiment(name: Annotated[str, Query(...)], experiments: Annotated[Experiments, Depends(repository)]) -> Experiment:
    model = await experiments.read(name=name)
    if not model:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Experiment with name {name} not found")
    return Experiment(id=model.id, name=model.name)

@router.patch('/experiments/{id}/')
async def update_experiment(id: Annotated[UUID, Path(...)], name: Annotated[str, Body(embed=True)], experiments: Annotated[Experiments, Depends(repository)]):
    if not await experiments.get(id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Experiment not found")
    await experiments.update(id, name)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.delete('/experiments/{id}/')
async def delete_experiment(id: Annotated[UUID, Path(...)], experiments: Annotated[Experiments, Depends(repository)]):
    if not await experiments.get(id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Experiment not found")
    await experiments.delete(id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.delete('/experiments/')
async def delete_experiment(experiments: Annotated[Experiments, Depends(repository)]):
    await experiments.clear()
    return Response(status_code=status.HTTP_204_NO_CONTENT)