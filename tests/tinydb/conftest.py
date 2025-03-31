from os import path, makedirs
from shutil import rmtree
from pytest import fixture
from logging import getLogger
from tinydb import TinyDB

from mltracker.adapters.tinydb.experiments import Experiments

logger = getLogger(__name__)

@fixture(scope='function')
def database():
    if not path.exists('data'):
        makedirs('data')
    yield TinyDB('data/database.json')
    try:
        rmtree('data')
    except Exception:
        logger.warning('Could not remove data directory')

@fixture(scope='function')
def experiments(database: TinyDB):
    return Experiments(database)
