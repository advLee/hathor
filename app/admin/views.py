#! /usr/bin/env python
# ^_^ coding: utf-8 ^_^

from . import admin
from .. import db
from flask import request, render_template
from ..models import User, Role, Article, Label, Comment
from flask import jsonify
from datetime import datetime


@admin.route('/', methods=['GET'])
def index():
    return 'this is admin index page'


@admin.route('/article', methods=['GET', 'POST', 'UPDATE'])
def article():
    response_data = []
    article_id = request.args.get('article_id')
    if request.method == 'GET':
        article = Article.query.filter_by(article_id=article_id).first()
        username = User.query.filter_by(id=article.user_id).first().username
        label = Label.query.filter_by(id=article.lable_id)
        response_data.append(dict(id=article.id, title=article.title, summary=article.summary, body=article.body,
                                  create_time=article.create_time, user=username, label=label))
        return jsonify(response_data)

    title = request.args.get('title')
    body = request.args.get('body')
    summary = request.args.get('summary') or body[:100]
    create_time = datetime.now()
    modify_time = create_time
    user_id = request.args.get('user_id')
    label_id = request.args.get('label_id')
    if request.method == 'POST':
        new_article = Article(title=title, summary=summary, body=body, create_time=create_time, modify_time=modify_time,
                              user_id=user_id, label_id=label_id)
        db.session.add(new_article)
        db.session.commit()
        return 'ok'

    if request.method == 'UPDATE':
        modify_time = datetime.now()
        Article.query.filter_by(id=article_id).update(title=title, summary=summary, body=body, create_time=create_time,
                                modify_time=modify_time, user_id=user_id, label_id=label_id)


