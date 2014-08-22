from __future__ import absolute_import, division, print_function

import pytest

psycopg2 = pytest.importorskip('psycopg2')
import subprocess
ps = subprocess.Popen("ps aux | grep postgres",shell=True, stdout=subprocess.PIPE)
output = ps.stdout.read()
pytestmark = pytest.mark.skipif(len(output.split('\n')) < 6, reason="No Postgres Installation")

import sqlalchemy
from sqlalchemy import Table, Column, Integer
import os
import csv as csv_module

url = 'postgresql://localhost/postgres'
file_name = 'test.csv'

# @pytest.fixture(scope='module')
def setup_function(function):
    data = [(1, 2), (10, 20), (100, 200)]

    with open(file_name, 'w') as f:
        csv_writer = csv_module.writer(f)
        for row in data:
            csv_writer.writerow(row)

def teardown_function(function):
    os.remove(file_name)
    engine = sqlalchemy.create_engine(url)
    metadata = sqlalchemy.MetaData()
    metadata.reflect(engine)

    # for t in metadata.tables:
        # if 'travisci' in t:
            # metadata.tables[t].drop(engine)

def test_csv_postgres_load():

    tbl = 'travisci_postgres'

    engine = sqlalchemy.create_engine(url)
    conn = engine.raw_connection()

    m = sqlalchemy.MetaData()
    t = Table(tbl, m,
        Column('a', Integer),
        Column('c', Integer)
    )

    m.create_all(engine)

    cursor = conn.cursor()
    full_path = os.path.abspath(file_name)
    load = '''copy {} from '{}'(FORMAT CSV, DELIMITER ',', NULL '');'''.format(tbl, full_path)
    cursor.execute(load)
    conn.commit()
