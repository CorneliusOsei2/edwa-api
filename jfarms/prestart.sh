#! /usr/bin/env bash

# Let the DB start
python ./app/prestart/db_start.py

alembic revision --autogenerate -m "Tables revision"

# Run migrations
alembic upgrade head

# # Create initial data in DB
python ./app/prestart/initial_data.py

uvicorn app.main:app --host 0.0.0.0 --port 8000