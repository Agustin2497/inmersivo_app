from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship

from run import db

from slugify import slugify
from sqlalchemy.exc import IntegrityError
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from flask import url_for

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

engine = create_engine('postgresql+psycopg2://postgres:memoria1@localhost:5433/proyecto')

#Base = declarative_base()
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'blog_user'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(256), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    posters = relationship("post")




class Post(Base):
    __tablename__ = 'post'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('blog_user.id', ondelete='CASCADE'), nullable=False)
    title = db.Column(db.String(256), nullable=False)
    title_slug = db.Column(db.String(256), unique=True, nullable=False)
    content = db.Column(db.Text)




def run():
    pass

Session = sessionmaker(bind=engine)
session = Session()



if __name__ == '__main__':
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    run()