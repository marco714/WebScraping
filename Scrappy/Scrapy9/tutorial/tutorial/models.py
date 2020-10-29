from sqlalchemy import create_engine, Column, Table, ForeignKey, MetaData
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (Integer, String, Date, DateTime, Float, Boolean, Text)
from scrapy.utils.project import get_project_settings

Base = declarative_base()

def db_connect():

    '''
    Performs database connection using database settings from settings.py
    Return sqlalchemy engine instance
    '''

    return create_engine(get_project_settings().get("CONNECTION_STRING"))

def create_table(engine):

    Base.metadata.create_all(engine)

#Association Table For Many To Many Relationship between Quote and tag
quote_tag = Table('quote_tag', Base.metadata,
    Column('quote_id', Integer, ForeignKey('quote.id')),
    Column('tag_id', Integer, ForeignKey('tag.id'))
)

class Quote(Base):

    __tablename__ = "quote"

    id = Column(Integer, primary_key=True)
    quote_content = Column('quote_content', Text())
    author_id = Column(Integer, ForeignKey('author.id'))#Many Quotes to one author
    tags = relationship('Tag', secondary='quote_tag', lazy='dynamic', backref="quote") # Many to many for quote and tag

class Author(Base):

    __tablename__ = "author"


    id = Column(Integer, primary_key=True)
    name = Column('name', String(50), unique=True)
    birthday = Column('birthday', DateTime)
    bornlocation = Column('bornlocation', String(150))
    bio = Column('bio', Text())
    quotes = relationship('Quote', backref='author')#One Author to many Quotes

class Tag(Base):

    __tablename__ = "tag"

    id = Column(Integer, primary_key=True)
    name = Column('name', String(30), unique=True)
    quote = relationship('Quote', secondary="quote_tag", lazy='dynamic', backref="tag")
