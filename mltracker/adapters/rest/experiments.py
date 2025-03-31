from uuid import uuid4, UUID
from typing import override
from typing import Optional
from requests import post, get, put, delete, patch

from mltracker.ports.owner import Owner
from mltracker.ports.experiments import Experiment
from mltracker.ports.experiments import Experiments as Repository 
from mltracker.adapters.rest.models import Models


class Experiments(Repository):
    def __init__(self, uri: str):
        self.uri = uri
    
    @override
    def create(self, name: str) -> Experiment:
        response = post(f'{self.uri}/experiments/', json={'name': name}) 
        if response.status_code == 409:
            raise ValueError(f"Experiment with name {name} already exists") 
        data = response.json()
        return Experiment(
            id=data['id'], 
            name=name, 
            models=Models(self.uri, owner=Owner(id=data['id']))
        )

    @override    
    def read(self, *, name) -> Optional[Experiment]: 
        response = get(f'{self.uri}/experiments?name={name}')
        if response.status_code == 404:
            return None
        data = response.json()
        return Experiment(
            id=UUID(data['id']),
            name=data['name'], 
            models=Models(self.uri, owner=Owner(id=UUID(data['id'])))
        )
    

    @override
    def update(self, id: UUID, name: str) -> Experiment:
        response = patch(f'{self.uri}/experiments/{str(id)}/', json={'name': name})
        return Experiment(
            id=id,
            name=name, 
            models=Models(self.uri, owner=Owner(id=id))
        )
    
    @override
    def delete(self, id: UUID): 
        delete(f'{self.uri}/experiments/{str(id)}')

    @override
    def clear(self) -> None:
        delete(f'{self.uri}/experiments/')

    @override
    def list(self) -> list[Experiment]:
        response = get(f'{self.uri}/experiments/')
        return [Experiment(
            id=UUID(data['id']), 
            name=data['name'], 
            models=Models(self.uri, owner=Owner(id=UUID(data['id'])))
        ) for data in response.json()]