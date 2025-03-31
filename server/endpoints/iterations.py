from uuid import UUID
from typing import Annotated
from typing import Any 

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException, status
from fastapi import Path 
from fastapi import Body
from fastapi import Response

from server.ports.iterations import Iterations
from server.endpoints.experiments import repository, Experiments
from server.schemas import Iteration

router = APIRouter() 

async def iteration( 
    hash: Annotated[str, Path(...)], 
    phase: Annotated[str, Body(...)],
    epoch: Annotated[int, Body(...)],
    arguments: Annotated[dict[str, Any], Body(...)]
)-> Iteration:
    return Iteration(hash=hash, phase=phase, epoch=epoch, arguments=arguments)

async def iterations(id: Annotated[UUID, Path(...)], experiments: Annotated[Experiments, Depends(repository)]) -> Iterations:
    model = await experiments.models.get(id)
    if not model:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Model with ID {id} not found")
    return model.iterations

@router.put('/models/{id}/iterations/{hash}/')
async def add_or_replace_iteration(iteration: Annotated[Iteration, Depends(iteration)], iterations: Annotated[Iterations, Depends(iterations)]):
    await iterations.put(iteration.hash, iteration.phase, iteration.epoch, iteration.arguments)
    return Response(status_code=status.HTTP_204_NO_CONTENT) 

@router.get('/models/{id}/iterations/')
async def list_iterations(iteration: Annotated[Iterations, Depends(iteration)]) -> list[Iteration]:
    list = await iteration.list()
    return [Iteration(hash=iteration.hash, phase=iteration.phase, epoch=iteration.epoch, arguments=iteration.arguments) for iteration in list]