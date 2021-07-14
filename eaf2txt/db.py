import sqlite3
from pathlib import Path

import pandas as pd

create_processed_files_table = """
CREATE TABLE ProcessedFiles
(_id INTEGER PRIMARY KEY AUTOINCREMENT,
 filename TEXT UNIQUE);
"""

create_annotation_table = """
CREATE TABLE Annotation
(_id INTEGER PRIMARY KEY AUTOINCREMENT,
 tier_id TEXT NOT NULL,
 participant TEXT NOT NULL,
 start INTEGER NOT NULL,
 end INTEGER NOT NULL,
 duration INTEGER NOT NULL,
 value TEXT NOT NULL,
 file_id INTEGER NOT NULL,
 FOREIGN KEY (file_id) REFERENCES ProcessedFiles (_id)
 );
"""


def _open_connection(path_to_database: Path):
    connection = sqlite3.connect(path_to_database)
    connection.execute("PRAGMA foreign_keys = 1")
    cursor = connection.cursor()

    return connection, cursor


def create_database(path_to_database: Path):
    if path_to_database.exists():
        raise FileExistsError(f'Can\'t create database: file {path_to_database} already exists.')

    connection, cursor = _open_connection(path_to_database)

    cursor.execute(create_processed_files_table)
    cursor.execute(create_annotation_table)
    connection.commit()
    connection.close()


def add_annotations(path_to_database: Path, eaf_filename: str, annotations_df: pd.DataFrame):
    if not path_to_database.exists():
        raise FileNotFoundError(f'Database file {path_to_database} does not exist.')

    connection, cursor = _open_connection(path_to_database)

    try:
        cursor.execute(f'INSERT INTO ProcessedFiles (filename) VALUES("{eaf_filename}")')
        file_id = cursor.lastrowid
    except sqlite3.IntegrityError as e:
        raise type(e)(f'EAF file {eaf_filename} has been added to the database earlier')

    # We haven't committed yet, so if anything goes wrong during the insert, the transaction will be rolled back.
    annotations_df['file_id'] = file_id
    annotations_df.to_sql('Annotations', con=connection, if_exists='append', index=False)

    connection.commit()
