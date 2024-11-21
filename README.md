### ML-Tracker

In machine learning, a model has no scientific value if it's not reproducible. In order to reproduce a model, a rigorous tracking of the model's data is needed. This not only includes the model's metrics but also it's parameters, the data used to train the model, how data was fed into the model, what criterions or optimizers were used, etc. This is a tedious task that can be automated with the help of a tool that helps you track your machine learning aggregates, their metrics and their parameters. This is what ML-Tracker does.

ML-Tracker is a tool that helps you track your machine learning aggregates, their metrics and their parameters, using the aggregate pattern. It has a TinyDB backend as default that stores the data in a JSON file, but more backends can be added in the future. This is posible thanks to the ports and adapters architecture that decouples the interface of the data access objects from their implementation.


## Installation

```bash
pip install mltracker
```

## Usage

### Create an experiment

Experiments are simple identifiers that help you group your aggregates. You can create an experiment by calling the get_experiment function with the name of the experiment you want to create. If the experiment already exists, it will return the existing experiment, otherwise it will create a new one.

```python

from mltracker import get_experiment
from mltracker import get_aggregates_collection

# Create an experiment
experiment = get_experiment('experiment_name') #This will read an existing experiment or create a new one if it doesn't exist

```

You can also access the experiments collection directly to manage the experiments in a CRUD way.

```python

from mltracker import get_experiments_collection

# Get the experiments collection
experiments = get_experiments_collection()
experiment = experiments.create('experiment_name') #This will create a new experiment
experiment.name = 'new_experiment_name'
experiments.update(experiment) #This will update the experiment
experiment_list = experiments.list() #This will return a list with all the experiments
experiment = experiments.read('new_experiment_name') #This will return the experiment
experiments.delete('new_experiment_name') #This will delete the experiment
```

### Create an aggregate

In domain driven design, an aggregate cluster of related objects that should be treated as a single unit. In machine learning we can think of an aggregate as a model and it's data. You can have multiple aggregates within an experiment. An aggregate store data about the models that it contains, their metrics and the iterations that it passed through.

When you retrieve an aggregate, it's metrics are not loaded directly, instead a data access object is instantiated within the aggregate that allows you to load the metrics on demand.  The same with it's iterations.

Let's create an aggregate:

```python
from mltracker import get_aggregates_collectio
from mltracker import Module

# Get an instance of the aggregates collection
aggregates = get_aggregates_collection()

# Create an aggregate
aggregate = aggregates.create(
    id='1', 
    modules=[Module(type='model', hash='1234', name='Perceptron', parameters={'input_size': 784, 'output_size': 10})]
)# Where hash is the identifier of the model.

# Add metrics to the aggregate
aggregate.metrics.add(Metric(name='accuracy', value=0.98, epoch=1, phase='train'))
all_metrics = aggregate.metrics.list() # This should print the list of metrics added to the aggregate
```

You can create your own data access objects using the ports provided in the ports module. You just need to implement the abstract methods of the data access object and pass it to the aggregate when you create it.

```python
from mltracker.ports import Aggregates

class MyCustomAggregateStorage(Aggregates):
    def __init__(self,...):
        ...

    def create(self, *args, **kwargs):
        ...

    def read(self, *args, **kwargs):
        ...

    def update(self, *args, **kwargs):
        ...
    ...
```