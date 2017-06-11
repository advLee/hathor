#! /usr/bin/env python
# ^_^ coding: utf-8 ^_^

from . import main
from .. import db
from flask import request, render_template
from ..models import User, Role, Article, Label, Comment
from flask import jsonify
from datetime import datetime


@main.route('/', methods=['GET'])
def index():
    return 'hello main index'


@main.route('/default', methods=['GET'])
def default():
    response_data = []
    try:
        page = int(request.args.get('page'))
    except Exception as e:
        page = 0
    step = 10
    offset = 0 if page == 0 else (page-1)*step
    articales = Article.query.order_by(Article.create_time).offset(offset).limit(step).all()
    for articale in articales:
        response_data.append(dict(title=articale.title, summary=articale.summary, create_time=articale.create_time))
    return jsonify(response_data)


@main.route('/comment', methods=['GET', 'POST'])
def comment():
    if request.method == 'GET':
        response_data = []
        try:
            article_id = int(request.args.get('article'))
        except Exception as e:
            return jsonify(response_data)
        try:
            page = int(request.args.get('start'))
        except Exception as e:
            page = 0
        step = 10
        offset = 0 if page == 0 else (page-1)*10
        comments = Comment.query.filter_by(article_id=article_id).order_by(Comment.create_time).offset(offset).limit(step).all()
        for comment in comments:
            user = User.query.filter_by(id=comment.user_id).first().username
            response_data.append(dict(user=user, content=comment.content, create_time=comment.create_time))
        return jsonify(response_data)
    if request.method == 'POST':
        user_id = request.form.get('user_id')
        content = request.form.get('content')
        article_id = request.form.get('article_id')
        create_time = datetime.now()
        comment = Comment(user_id=user_id, content=content, article_id=article_id, create_time=create_time)
        db.session.add(comment)
        db.session.commit()
        return 'ok'




