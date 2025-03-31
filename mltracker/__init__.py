from tinydb import TinyDB
from mltracker.ports.experiments import Experiments
from mltracker.ports.experiments import Experiment
from mltracker.ports.models import Models

from mltracker.adapters.tinydb.experiments import Experiments as TinyDBExperiments

def getallexperiments() -> Experiments:
    return TinyDBExperiments(database=TinyDB('data/database.json'))

def getexperiment(experiment: str) -> Experiment:
    experiments = getallexperiments() 
    return experiments.read('name', name=experiment) or experiments.create(experiment)

def getallmodels(experiment: str) -> Models:
    return getexperiment(experiment).models