from pytest import fixture
from mltracker.adapters.tinydb.iterations import Iteration, Iterations
from mltracker.ports.iterations import Dataset
from mltracker.ports.modules import Module

@fixture
def iterations(database):
    return Iterations('test', database)

def test_iterations(iterations: Iterations):
    iteration = Iteration(
        hash='1',
        epoch=1,
        phase='train',
        dataset=Dataset(
            hash='123',
            name='mnist',
            arguments={'train': True, 'normalize': True}
        ),
        arguments={'batch_size': 32, 'shuffle': True},
        modules=[
            Module(
                type='criterion',
                hash='123',
                name='CrossEntropyLoss',
                arguments={'reduction': 'mean'}
            ),

            Module(
                type='optimizer',
                hash='123',
                name='SGD',
                arguments={'lr': 0.01}
            )
        ]
    )


    iteration2 = Iteration(
        hash='2',
        epoch=1,
        phase='train',
        dataset=Dataset(
            hash='123',
            name='mnist',
            arguments={'train': True, 'normalize': True}
        ),
        arguments={'batch_size': 32, 'shuffle': True},
        modules=[
            Module(
                type='criterion',
                hash='123',
                name='CrossEntropyLoss',
                arguments={'reduction': 'mean'}
            ),

            Module(
                type='optimizer',
                hash='123',
                name='SGD',
                arguments={'lr': 0.01}
            )
        ]
    )


    iteration3 = Iteration(
        hash='2',
        epoch=1,
        phase='train',
        dataset=Dataset(
            hash='123',
            name='mnist',
            arguments={'train': True, 'normalize': True}
        ),
        arguments={'batch_size': 32, 'shuffle': True},
        modules=[
            Module(
                type='criterion',
                hash='123',
                name='CrossEntropyLoss',
                arguments={'reduction': 'mean'}
            ),

            Module(
                type='optimizer',
                hash='123',
                name='SGD',
                arguments={'lr': 0.01}
            )
        ]
    )

    iterations.put(iteration)
    iterations.put(iteration2)
    iterations.put(iteration3) #overriding iteration2 since hash is the same
    assert iterations.list() == [iteration, iteration3]