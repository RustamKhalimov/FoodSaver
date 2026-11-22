"""Create and restore verified SQLite backups for the FoodSaver backend."""

import argparse
import sqlite3
from contextlib import closing
from datetime import datetime
from pathlib import Path


BACKEND_DIR = Path(__file__).resolve().parents[1]
DATABASE_PATH = BACKEND_DIR / 'db.sqlite3'


def integrity_check(connection):
    result = connection.execute('PRAGMA integrity_check').fetchone()[0]
    if result != 'ok':
        raise RuntimeError(f'SQLite integrity check failed: {result}')


def copy_database(source_path, destination_path):
    if source_path.resolve() == destination_path.resolve():
        raise ValueError('Source and destination must be different files.')
    destination_path.parent.mkdir(parents=True, exist_ok=True)
    with closing(sqlite3.connect(str(source_path))) as source:
        integrity_check(source)
        with closing(sqlite3.connect(str(destination_path))) as destination:
            source.backup(destination)
            integrity_check(destination)


def backup(output_path):
    if not DATABASE_PATH.exists():
        raise FileNotFoundError(f'Database not found: {DATABASE_PATH}')

    copy_database(DATABASE_PATH, output_path)
    print(f'Backup created and verified: {output_path}')


def verify(database_path):
    if not database_path.is_file():
        raise FileNotFoundError(f'Database not found: {database_path}')
    with closing(sqlite3.connect(str(database_path))) as connection:
        integrity_check(connection)
    print(f'SQLite integrity check passed: {database_path}')


def restore(source_path, target_path):
    if not source_path.is_file():
        raise FileNotFoundError(f'Backup not found: {source_path}')
    if source_path.resolve() == target_path.resolve():
        raise ValueError('Restore source and target must be different files.')

    temporary_path = target_path.with_name(target_path.name + '.restore-tmp')
    copy_database(source_path, temporary_path)

    if target_path.exists():
        timestamp = datetime.now().strftime('%Y%m%d-%H%M%S-%f')
        safety_path = target_path.with_name(
            f'{target_path.name}.before-restore-{timestamp}'
        )
        copy_database(target_path, safety_path)
        print(f'Previous database preserved: {safety_path}')

    temporary_path.replace(target_path)
    print(f'Restored and verified database: {target_path}')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='command', required=True)

    backup_parser = commands.add_parser('backup', help='create a verified backup')
    backup_parser.add_argument(
        '--output',
        type=Path,
        help='backup file path (defaults to backend/backups with a timestamp)',
    )

    commands.add_parser('verify', help='check a database or backup').add_argument(
        '--source', required=True, type=Path
    )

    commands.add_parser('restore', help='restore a verified backup').add_argument(
        '--source', required=True, type=Path
    )
    commands.choices['restore'].add_argument(
        '--target',
        type=Path,
        default=DATABASE_PATH,
        help='database path to replace (defaults to backend/db.sqlite3)',
    )

    args = parser.parse_args()
    if args.command == 'backup':
        output_path = args.output or (
            BACKEND_DIR / 'backups' /
            f"foodsaver-{datetime.now().strftime('%Y%m%d-%H%M%S-%f')}.sqlite3"
        )
        backup(output_path.resolve())
    elif args.command == 'verify':
        verify(args.source.resolve())
    else:
        restore(args.source.resolve(), args.target.resolve())


if __name__ == '__main__':
    main()
