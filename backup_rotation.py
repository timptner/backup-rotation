#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2023 Aiven Timptner

from argparse import ArgumentParser
from pathlib import Path
from datetime import date, timedelta


def main() -> None:
    config = get_config()
    path: Path = config['path']
    today = date.today()
    daily = today - timedelta(days=7)
    weekly = today - timedelta(weeks=4)
    monthly = today - timedelta(days=365)
    for file in path.glob('*.tar.gz'):
        stem = file.name.split('.')[0]
        created_at = date.fromisoformat(stem)

        if created_at > daily:
            continue

        if created_at.isoweekday() == 1 and created_at > weekly:
            continue

        if created_at.day == 1 and created_at > monthly:
            continue

        file.unlink()
        print(f"Backup deleted. [name={file.name}]")


def get_config() -> dict:
    parser = ArgumentParser('Backup Rotation')
    parser.add_argument('path', help="Directory of backup files", type=Path)
    args = parser.parse_args()
    return {
        'path': args.path,
    }


if __name__ == '__main__':
    main()
