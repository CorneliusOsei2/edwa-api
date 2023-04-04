#! /usr/bin/env bash

# Let the DB start
python ./app/prestart/db_start.py

# Run migrations
alembic upgrade head

# Create initial data in DB
python ./app/prestart/initial_data.py