import sqlite3
from pathlib import Path

import pandas as pd
import pytest

from ..db import create_database, add_annotations, _open_connection
from ..eaf2txt import convert_eaf_to_data_frame


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


def test_add_annotations(tmp_path, request):
    # TODO: move the path definition to tests/config.py or somewhere
    source_eaf = Path(request.fspath.dirpath('5959-0GS0.eaf'))
    annotations_df = convert_eaf_to_data_frame(source_eaf)
    db_path = tmp_path / 'eaf2txt.sqlite'

    # Fails reasonably when the database file does not exist
    with pytest.raises(FileNotFoundError) as e:
        add_annotations(path_to_database=db_path,
                        eaf_filename=source_eaf.name, annotations_df=annotations_df)
    assert str(e.value).startswith('Database file ') and str(e.value).endswith(' does not exist.')

    # Create the database
    create_database(db_path)

    # Add and check annotations
    add_annotations(path_to_database=db_path,
                    eaf_filename=source_eaf.name, annotations_df=annotations_df)
    connection, cursor = _open_connection(db_path)
    select_query = """
    SELECT * 
    FROM ProcessedFiles
    INNER JOIN Annotations on ProcessedFiles._id = Annotations.file_id;
    """
    annotations_from_db = pd.read_sql(select_query, con=connection)
    assert (annotations_from_db.drop(columns=['_id', 'filename']) == annotations_df).all().all()
    assert (annotations_from_db['filename'] == source_eaf.name).all()

    # Check that they won't be inserted twice (as long as the filename is the same)
    with pytest.raises(sqlite3.IntegrityError) as e:
        add_annotations(path_to_database=db_path,
                        eaf_filename=source_eaf.name, annotations_df=annotations_df)
    assert str(e.value) == f'EAF file {source_eaf.name} has been added to the database earlier'
