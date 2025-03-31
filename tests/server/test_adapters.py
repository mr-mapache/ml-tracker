from pytest import mark
from server.ports.experiments import Experiments

@mark.asyncio
async def test_experiments(repository: Experiments):
    experiment = await repository.create(id=None, name='test')
    assert experiment.name == 'test'
    experiment = await repository.get(experiment.id)
    experiment = await repository.update(experiment.id, name='new')
    experiment = await repository.read(name='test')
    assert not experiment

    experiment = await repository.read(name='new')
    assert experiment
    
    experiment = await repository.create(id=None, name='other')
    list = await repository.list()
    assert len(list) == 2

    await repository.delete(experiment.id)
    list = await repository.list()
    assert len(list) == 1
    
    experiment = await repository.create(id=None, name='test-1')
    experiment = await repository.create(id=None, name='test-2')
    experiment = await repository.create(id=None, name='test-3')
    await repository.clear()
    
    list = await repository.list()
    assert len(list) == 0 


@mark.asyncio
async def test_models(repository: Experiments):
    experiment = await repository.create(id=None, name='test')
    models = experiment.models
    model = await models.create(hash='12345', name='llama3')
    assert model.hash == '12345'
    assert model.name == 'llama3'
    model = await models.read(hash='12345')
    assert model.name == 'llama3'
    assert model.epoch == 0
    model = await models.update(model.id, epoch=5)
    assert model.epoch == 5
    
    model = await models.create(hash='12346', name='llama3.2')
    list = await models.list()
    assert len(list) == 2

    model = await models.get(model.id)
    assert model.hash == '12346'

    await models.delete(id=model.id)
    list = await models.list()
    assert len(list) == 1

    await models.clear()
    list = await models.list()
    assert len(list) == 0


@mark.asyncio
async def test_modules(repository: Experiments):
    experiment = await repository.create(id=None, name='test')
    models = experiment.models
    model = await models.create(hash='12345', name='llama3')
    modules = model.modules

    await modules.put(hash='12345', type='nn', name='mlp', epoch=0, arguments={'in_size':784, 'out_size':10}) 
    await modules.put(hash='12345', type='nn', name='mlp', epoch=10, arguments={'in_size':784, 'out_size':10})

    list = await modules.list()
    assert len(list) == 1


    await modules.put(hash='123456', type='nn', name='mlp', epoch=0, arguments={'in_size':28, 'out_size':10}) 
    await modules.put(hash='123457', type='nn', name='mlp', epoch=10, arguments={'in_size':54, 'out_size':10})

    list = await modules.list()
    assert len(list) == 3

    await modules.clear()
    list = await modules.list()
    assert len(list) == 0


    
@mark.asyncio
async def test_metrics(repository: Experiments):
    experiment = await repository.create(id=None, name='test')
    models = experiment.models
    model = await models.create(hash='12345', name='llama3')
    metrics = model.metrics

    await metrics.add(name='accuracy', value=0.88, epoch=0, phase='train')
    await metrics.add(name='accuracy', value=0.87, epoch=1, phase='train')
    await metrics.add(name='accuracy', value=0.86, epoch=2, phase='train')
    await metrics.add(name='accuracy', value=0.85, epoch=3, phase='train')
    await metrics.add(name='accuracy', value=0.88, epoch=0, phase='test')
    await metrics.add(name='accuracy', value=0.87, epoch=1, phase='test')
    await metrics.add(name='accuracy', value=0.86, epoch=2, phase='test')
    await metrics.add(name='accuracy', value=0.85, epoch=3, phase='test')

    list = await metrics.list()
    assert len(list) == 8

    await metrics.clear()
    list = await metrics.list()
    assert len(list) == 0


@mark.asyncio
async def test_iterations(repository: Experiments):
    experiment = await repository.create(id=None, name='test')
    models = experiment.models
    model = await models.create(hash='12345', name='llama3')
    iterations = model.iterations

    await iterations.put(hash='12345', phase='train', epoch=0, arguments={'in_size': 784, 'out_size':10})
    await iterations.put(hash='12345', phase='train', epoch=10, arguments={'in_size': 784, 'out_size':10})

    list = await iterations.list()
    assert len(list) == 1


