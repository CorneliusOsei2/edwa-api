from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String

# Inherit from this class to create each of the database models or classes (the ORM models):
Base = declarative_base()
