from mltracker.adapters.tinydb.getters import get_experiments_collection, get_experiment, get_aggregates_collection
from mltracker.adapters.tinydb.experiments import Experiment
from mltracker.adapters.tinydb.aggregates import Aggregate
from mltracker.adapters.tinydb.metrics import Metric
from mltracker.adapters.tinydb.iterations import Iteration
from mltracker.adapters.tinydb.aggregates import Module

#TODO: Fix this to support other adapters. For now only tinydb is supported.