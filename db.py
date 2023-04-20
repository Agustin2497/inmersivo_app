from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
engine = create_engine('postgresql://postgres:memoria1@localhost:5433/proyecto')
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()