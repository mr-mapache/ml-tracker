from pytest import fixture, raises
from mltracker.adapters.tinydb.experiments import Experiments, Experiment

@fixture
def experiments(database):
    return Experiments(database)

def test_experiments(experiments: Experiments):
    experiment = experiments.create('test')
    assert experiment.name == 'test'
    experiment = experiments.read('test')
    assert experiment.name == 'test'
    assert experiments.read('test2') is None
    assert len(experiments.list()) == 1

    experiment = experiments.create('test2')
    assert experiment.name == 'test2'
    assert len(experiments.list()) == 2

    experiments.delete('test')
    experiment.name = 'test'
    experiments.update(experiment)

    experiment = experiments.read('test')
    assert experiment.name == 'test'
    with raises(ValueError):
        experiments.create('test')