import sqlite3
import pytest

from ..db import create_database


def test_create_database(tmp_path):
    # Check database file is created
    db_path = tmp_path / 'eaf2txt.sqlite'
    create_database(db_path)
    assert db_path.exists()

    # Check for expected tables
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    tables = [row[0].lower() for row in
              cursor.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()]
    assert 'ProcessedFiles'.lower() in tables
    assert 'Annotation'.lower() in tables

    # Check that the database file won't get overwritten
    with pytest.raises(FileExistsError) as e:
        create_database(db_path)
    assert 'Can\'t create database: file ' in str(e.value)
