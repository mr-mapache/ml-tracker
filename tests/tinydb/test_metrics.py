from pytest import fixture
from mltracker.adapters.tinydb.metrics import Metrics, Metric

@fixture
def metrics(database):
    return Metrics('test', database)

def test_metrics(metrics: Metrics):
    metrics.add(Metric('accuracy', value=0.9, batch=100, epoch=1, phase='train'))
    metrics.add(Metric('accuracy', value=0.2, batch=100, epoch=2, phase='train'))
    metrics.add(Metric('accuracy', value=0.2, batch=100, epoch=2, phase='test'))
    metrics.add(Metric('loss', value=0.3, batch=100, epoch=1, phase='train'))
    assert len(metrics.list()) == 4
    metrics.clear()
    assert len(metrics.list()) == 0