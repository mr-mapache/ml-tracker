from mltracker.ports import structure
from mltracker.ports.experiments import Experiments
from mltracker.ports.modules import Module
from mltracker.ports.metrics import Metric
from mltracker.ports.iterations import Iteration


def test_experiments(experiments: Experiments):
    experiment = experiments.create('test')
    experiment = experiments.read(name='test')
    assert experiment.name == 'test'
    
    experiment = experiments.update(id=experiment.id, name='new')
    assert experiment.name == 'new'
    assert not experiments.read(name='test')
    experiment = experiments.create('test')

    list = experiments.list()
    assert len(list) == 2

    experiments.delete(experiment.id)
    list = experiments.list()
    assert len(list) == 1

    experiments.clear()
    list = experiments.list()
    assert len(list) == 0 


def test_models(experiments: Experiments):
    experiment = experiments.create('test')
    models = experiment.models

    model = models.create(hash='12345', name='mlp')
    model = models.read(hash='12345')
    assert model.name == 'mlp'

    model = models.update(hash='12345', epoch=50)
    model = models.read(hash='12345')
    assert model.epoch == 50

    models.delete(model.id)
    assert not models.read(hash='12345')

    model = models.create(hash='123456', name='mlp')
    model = models.create(hash='123457', name='mlp')
    list = models.list()
    assert len(list) == 2

    models.clear()
    list = models.list()
    assert len(list) == 0 


def test_modules(experiments: Experiments):
    experiment = experiments.create('test')
    model = experiment.models.create('123', 'mlp')
    modules = model.modules
 
    modules.put(Module(type='optimizer', hash='hash1', name='Adam', epoch=1, arguments={'lr': 0.1}))
    modules.put(Module(type='criterion', hash='hash1', name='CrossEntropyLoss', epoch=1, arguments={}))
    modules.put(Module(type='optimizer', hash='hash1', name='Adam', epoch=10, arguments={'lr': 0.1}))
    modules.put(Module(type='optimizer', hash='hash1', name='Adam', epoch=11, arguments={'lr': 0.1}))  
    assert len(modules.list('optimizer')) == 1

    modules.put(Module(type='optimizer', hash='hash2', name='Adam', epoch=12, arguments={'lr': 0.2})) 
    assert len(modules.list('optimizer')) == 2

    modules.put(Module(type='optimizer', hash='hash1', name='Adam', epoch=13, arguments={'lr': 0.1})) 
    modules.put(Module(type='optimizer', hash='hash1', name='Adam', epoch=14, arguments={'lr': 0.1})) 
    assert len(modules.list('optimizer')) == 3
    assert len(modules.list('criterion')) == 1
 
    modules.clear()
    assert len(modules.list('optimizer')) == 0
    assert len(modules.list('criterion')) == 0


def test_metrics(experiments: Experiments):
    experiment = experiments.create('test')
    model = experiment.models.create('123', 'mlp')
    metrics = model.metrics
    
    metrics.add(Metric(name='accuracy', value=0.9, epoch=1, phase='train'))
    metrics.add(Metric(name='accuracy', value=0.2, epoch=1, phase='test'))
    metrics.add(Metric(name='accuracy', value=0.2, epoch=2, phase='train'))
    metrics.add(Metric(name='loss', value=0.3, epoch=3, phase='train'))
    
    assert len(metrics.list()) == 4
    metrics.clear()
    assert len(metrics.list()) == 0


def test_iterations(experiments: Experiments): 

    experiment = experiments.create('test')
    model = experiment.models.create('123', 'mlp')
    iterations = model.iterations

    iterations.put(Iteration(
        hash='1234',
        epoch=5,
        phase='train',
        arguments= {
            'dataset': {'hash': "1234", 'name': "MNIST", 'arguments': {'train': True}},
            'batch_size': 64,
            'shuffle': True
        }
    )) 

    assert len(iterations.list()) == 1
    
    iterations.put(Iteration(
        hash= "1234",
        epoch= 5,
        phase= 'train',
        arguments= {
            'dataset': {'hash': "1234", 'name': "MNIST", 'arguments': {'train': True}},
            'batch_size': 64,
            'shuffle': True
        }
    ))

    assert len(iterations.list()) == 1

    iterations.put(Iteration(
        hash="1234",
        epoch= 5,
        phase= 'evaluation',
        arguments= {
            'dataset': {'hash': "1234", 'name': "MNIST", 'arguments': {'train': True}},
            'batch_size': 64,
            'shuffle': True
        }
    ))
    assert len(iterations.list()) == 2

    
    iterations.put(structure({
        'hash': "1234",
        'epoch': 6,
        'phase': 'train',
        'arguments': {
            'dataset': {'hash': "1234", 'name': "MNIST", 'arguments': {'train': True}},
            'batch_size': 64,
            'shuffle': True
        }
    }, Iteration))

    assert len(iterations.list()) == 2

    iterations.put(structure({
        'hash': "12345",
        'epoch': 7,
        'phase': 'train',
        'arguments': {
            'dataset': {'hash': "1234", 'name': "MNIST", 'arguments': {'train': False}},
            'batch_size': 64,
            'shuffle': True
        }
    }, Iteration))

    assert isinstance(iterations.list()[0], Iteration)