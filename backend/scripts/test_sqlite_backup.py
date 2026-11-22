import sqlite3
import tempfile
import unittest
from contextlib import closing
from pathlib import Path

from scripts.sqlite_backup import copy_database, restore, verify


def create_database(path, value):
    with closing(sqlite3.connect(path)) as connection:
        connection.execute('CREATE TABLE sample (value TEXT NOT NULL)')
        connection.execute('INSERT INTO sample(value) VALUES (?)', (value,))
        connection.commit()


def read_value(path):
    with closing(sqlite3.connect(path)) as connection:
        return connection.execute('SELECT value FROM sample').fetchone()[0]


class SQLiteBackupTests(unittest.TestCase):
    def test_copy_creates_a_valid_backup(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / 'source.sqlite3'
            backup = root / 'backups' / 'backup.sqlite3'
            create_database(source, 'preserved')

            copy_database(source, backup)

            self.assertEqual(read_value(backup), 'preserved')
            verify(backup)

    def test_copy_rejects_the_same_source_and_destination(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / 'source.sqlite3'
            create_database(source, 'preserved')

            with self.assertRaises(ValueError):
                copy_database(source, source)

    def test_restore_preserves_previous_target_database(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            backup = root / 'backup.sqlite3'
            target = root / 'db.sqlite3'
            create_database(backup, 'from-backup')
            create_database(target, 'previous-data')

            restore(backup, target)

            self.assertEqual(read_value(target), 'from-backup')
            safety_copies = list(root.glob('db.sqlite3.before-restore-*'))
            self.assertEqual(len(safety_copies), 1)
            self.assertEqual(read_value(safety_copies[0]), 'previous-data')


if __name__ == '__main__':
    unittest.main()
