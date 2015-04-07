import os
import sys
from datetime import datetime
from flask import Flask, request, flash, url_for, redirect, \
     render_template, abort, send_from_directory, jsonify
from flask_sqlalchemy import SQLAlchemy
from model import db, Author, News, NewsAuthor

app = Flask(__name__)
app.config.from_pyfile('flaskapp.cfg')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/authors', methods=['GET'])
@app.route('/author/<author_id>', methods=['GET'])
def get_authors(author_id=0):

    ret = []

    if (author_id > 0):
        author = Author.query.filter(Author.id == author_id).first()

        if (isinstance(author, Author) == False):
            return jsonify(response='resource not found'), 404

        a = {
            'id': author.id,
            'name': author.name,
            'twitter': author.twitter,
            'url': author.url,
            'bio': author.bio
        }

        ret.append(a)

    else:

        authors = Author.query.all()

        for a in authors:
            ret.append({
                'id': a.id,
                'name': a.name,
                'twitter': a.twitter,
                'url': a.url,
                'bio': a.bio
            })

        return jsonify(response=ret)


@app.route('/news', methods=['GET'])
@app.route('/news/<news_id>', methods=['GET'])
def get_news(news_id=0):

    ret = []

    if (news_id > 0):
        news = News.query.filter(News.id == news_id).first()

        if (isinstance(news, News) == False):
            return jsonify(response='resource not found'), 404

        new = {
            'id': news.id,
            'title': news.title,
            'content': news.content,
            'published_on': news.published_on,
            'authors': []
        }

        for a in news.author:
            new['authors'].append({
                'id': a.id,
                'name': a.name,
                'twitter': a.twitter
            })

            ret.append(new)

    else:
        news = News.query.all()

        for n in news:

            new = {
                'id': n.id,
                'title': n.title,
                'content': n.content,
                'published_on': n.published_on,
                'authors': []
            }

            for a in n.author:
                new['authors'].append({
                    'id': a.id,
                    'name': a.name,
                    'twitter': a.twitter
                })

            ret.append(new)

    return jsonify(response=ret)

def initdb():
    db.create_all()

if __name__ == '__main__':
    app.run()
