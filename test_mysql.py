from __future__ import absolute_import, division, print_function

import pytest

MySQLdb = pytest.importorskip('MySQLdb')
import subprocess
ps = subprocess.Popen("ps aux | grep '[m]ysqld'",shell=True, stdout=subprocess.PIPE)
output = ps.stdout.read()
print(output)
print(len(output.split('\n')) < 6)


# pytestmark = pytest.mark.skipif(len(output.split('\n')) < 6, reason="No MySQL Installation")

import sqlalchemy
from sqlalchemy import Table, Column, Integer
import os
import csv as csv_module
import getpass

username = getpass.getuser()
url = 'mysql://{}@localhost:3306/test'.format(username)
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

def test_csv_mysql_load():

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
    inline_cmd = "SHOW GLOBAL VARIABLES LIKE 'local_infile';"
    cursor.execute(inline_cmd)
    conn.commit()
    print(cursor.fetchall())

    set_inline_on = "SET GLOBAL local_infile = 'ON';"
    cursor.execute(set_inline_on)
    conn.commit()


    full_path = os.path.abspath(file_name)
    load = '''LOAD DATA LOCAL INFILE '{}' INTO TABLE {} FIELDS TERMINATED BY ','
        lines terminated by '\n'
        '''.format(full_path, tbl)
    cursor.execute(load)
    conn.commit()
