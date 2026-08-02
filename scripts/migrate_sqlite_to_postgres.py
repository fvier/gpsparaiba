#!/usr/bin/env python3
"""Copy the current SQLite application data into an empty PostgreSQL schema."""

import argparse
import os
from pathlib import Path

from sqlalchemy import MetaData, create_engine, func, select, text


TABLES = ('users', 'carousel_images')


def parse_args():
    parser = argparse.ArgumentParser(
        description='Copy GPS Paraíba data from SQLite to an empty PostgreSQL database.'
    )
    parser.add_argument(
        '--source',
        default=str(Path(__file__).resolve().parents[1] / 'apps' / 'db.sqlite3'),
        help='Path to the source SQLite file.',
    )
    parser.add_argument(
        '--target',
        default=os.getenv('DATABASE_URL') or os.getenv('POSTGRES_URL'),
        help='PostgreSQL SQLAlchemy URL; defaults to DATABASE_URL.',
    )
    return parser.parse_args()


def normalize_postgres_url(url):
    if url and url.startswith('postgres://'):
        return url.replace('postgres://', 'postgresql+psycopg2://', 1)
    return url


def main():
    args = parse_args()
    source_path = Path(args.source).expanduser().resolve()
    target_url = normalize_postgres_url(args.target)

    if not source_path.is_file():
        raise SystemExit(f'Source SQLite database not found: {source_path}')
    if not target_url:
        raise SystemExit('Define DATABASE_URL or provide --target.')
    if not target_url.startswith(('postgresql://', 'postgresql+psycopg2://')):
        raise SystemExit('The target must be a PostgreSQL URL.')

    source_engine = create_engine(f'sqlite:///{source_path}')
    target_engine = create_engine(target_url, pool_pre_ping=True)
    source_metadata = MetaData()
    target_metadata = MetaData()
    source_metadata.reflect(bind=source_engine, only=TABLES)
    target_metadata.reflect(bind=target_engine, only=TABLES)

    missing = [name for name in TABLES if name not in target_metadata.tables]
    if missing:
        raise SystemExit(
            'Target schema is incomplete. Run `flask db upgrade` first. '
            f'Missing: {", ".join(missing)}'
        )

    with target_engine.connect() as connection:
        nonempty = {
            name: connection.scalar(select(func.count()).select_from(target_metadata.tables[name]))
            for name in TABLES
        }
    occupied = {name: count for name, count in nonempty.items() if count}
    if occupied:
        details = ', '.join(f'{name}={count}' for name, count in occupied.items())
        raise SystemExit(f'Target is not empty; migration cancelled ({details}).')

    copied = {}
    with source_engine.connect() as source, target_engine.begin() as target:
        for name in TABLES:
            source_table = source_metadata.tables[name]
            target_table = target_metadata.tables[name]
            rows = [dict(row) for row in source.execute(select(source_table)).mappings()]
            if rows:
                target.execute(target_table.insert(), rows)
            copied[name] = len(rows)

        for name in TABLES:
            target.execute(
                text(
                    "SELECT setval(pg_get_serial_sequence(:table_name, 'id'), "
                    "COALESCE(MAX(id), 1), MAX(id) IS NOT NULL) FROM " + name
                ),
                {'table_name': name},
            )

    print('Migration completed successfully.')
    for name, count in copied.items():
        print(f'{name}: {count} row(s)')


if __name__ == '__main__':
    main()
