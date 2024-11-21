from os import path, makedirs
from tinydb import TinyDB
from mltracker.adapters.tinydb.experiments import Experiment, Experiments
from mltracker.adapters.tinydb.aggregates import Aggregates

def get_experiments_collection(database_location: str) -> Experiments:
    if not path.exists(database_location):
        makedirs(database_location)
    database = TinyDB(path.join(database_location, 'database.json'))
    return Experiments(database)

def get_experiment(name: str, database_location: str) -> Experiment:
    experiments = get_experiments_collection(database_location)
    experiment = experiments.read(name)
    if not experiment:
        experiment = experiments.create(name)
    return experiment

def get_aggregates_collection(experiment_name: str, database_location: str) -> Aggregates:
    experiment = get_experiment(experiment_name, database_location)
    return Aggregates(experiment.id, database_location)