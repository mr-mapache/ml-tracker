from uuid import UUID
from typing import Annotated

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException, status
from fastapi import Path 
from fastapi import Response

from server.ports.metrics import Metrics
from server.endpoints.experiments import repository, Experiments
from server.schemas import Metric

router = APIRouter()

async def metrics(id: Annotated[UUID, Path(...)], experiments: Annotated[Experiments, Depends(repository)]) -> Metrics:
    model = await experiments.models.get(id)
    if not model:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Model with ID {id} not found")
    return model.metrics

@router.post('/models/{id}/metrics/')
async def add_metric(metric: Metric, metrics: Annotated[Metrics, Depends(metrics)]):
    await metrics.add(metric.name, metric.value, metric.epoch, metric.phase)
    return Response(status_code=status.HTTP_201_CREATED)

@router.get('/models/{id}/metrics/')
async def list_metrics(metrics: Annotated[Metrics, Depends(metrics)]):
    list = await metrics.list()
    return [Metric(name=metric.name, value=metric.value, epoch=metric.epoch, phase=metric.phase) for metric in list]