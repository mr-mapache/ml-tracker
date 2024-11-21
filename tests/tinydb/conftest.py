from os import path, makedirs
from shutil import rmtree
from pytest import fixture
from logging import getLogger
from tinydb import TinyDB

logger = getLogger(__name__)

@fixture(scope='session')
def database():
    if not path.exists('data'):
        makedirs('data')
    yield TinyDB('data/database.json')
    try:
        rmtree('data')
    except PermissionError:
        logger.warning('Could not remove data directory')