import sqlite3
from pathlib import Path

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


def create_database(path_to_database: Path):
    if path_to_database.exists():
        raise FileExistsError(f'Can\'t create database: file {path_to_database} already exists.')

    connection = sqlite3.connect(path_to_database)
    connection.execute("PRAGMA foreign_keys = 1")
    cursor = connection.cursor()

    cursor.execute(create_processed_files_table)
    cursor.execute(create_annotation_table)

    connection.commit()
    connection.close()
