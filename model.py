import os
from flask import Flask, request, flash, url_for, redirect, render_template, abort, send_from_directory
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import orm
from sqlalchemy.ext.declarative import declarative_base

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config.from_pyfile('flaskapp.cfg')
app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
db = SQLAlchemy(app)

class NewsAuthor(db.Model):
    __tablename__ = 'news_author'
    news_id = db.Column(db.Integer, db.ForeignKey('news.id'), primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'), primary_key=True)

class News(db.Model):
    __tablename__ = 'news'
    id = db.Column('id', db.Integer, primary_key=True)
    url = db.Column(db.String)
    title = db.Column(db.String)
    content = db.Column(db.Text)
    published_on = db.Column(db.DateTime())
    author = orm.relationship('Author', secondary='news_author', backref=db.backref('news', lazy='dynamic'))

class Author(db.Model):
    __tablename__ = 'author'
    id = db.Column('id', db.Integer, primary_key=True)
    url = db.Column(db.String)
    name = db.Column(db.String(100))
    twitter = db.Column(db.String)
    bio = db.Column(db.Text())