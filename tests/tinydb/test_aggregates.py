from pytest import fixture, raises
from mltracker.adapters.tinydb.aggregates import Module, Aggregates

@fixture
def aggregates(database):
    return Aggregates('test', database)

def test_aggregates(aggregates: Aggregates):
    aggregate = aggregates.create('test', [Module('test', 'test', 'test', {'test': 'test'})])
    assert aggregate.id == 'test'
    assert aggregate.modules == [Module('test', 'test', 'test', {'test': 'test'})]

    aggregate = aggregates.get('test')
    assert aggregate.id == 'test'
    assert aggregates.get('test2') is None
    assert len(aggregates.list()) == 1

    aggregate = aggregates.create('test2', [])
    assert aggregate.id == 'test2'
    assert len(aggregates.list()) == 2

    aggregate = aggregates.get('test')
    aggregates.remove(aggregate)
    assert aggregates.get('test') is None
    with raises(ValueError):
        aggregates.create('test2', [])