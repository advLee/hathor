#! /usr/bin/env python
# ^_^ coding: utf-8 ^_^

from . import db
import datetime


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(64), unique=True)
    password = db.Column(db.String(128), nullable=False)
    mail = db.Column(db.String(128))
    create_time = db.Column(db.DateTime, default=datetime.datetime.now())
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))
    articles = db.relationship('Article', backref='user', lazy='dynamic')

    def __repr__(self):
        return '<User %r>' % self.username


class Role(db.Model):
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    rolename = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role %r>' % self.rolename


class Article(db.Model):
    __tablename__ = 'article'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(64), nullable=False)
    summary = db.Column(db.String(256))
    body = db.Column(db.Text)
    create_time = db.Column(db.DateTime, default=datetime.datetime.now())
    modify_time = db.Column(db.DateTime, default=datetime.datetime.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    label_id = db.Column(db.Integer, db.ForeignKey('label.id'))
    delete_flag = db.Column(db.SmallInteger, default=0)

    def __repr__(self):
        return '<Article %r>' % self.title


class Label(db.Model):
    __tablename__ = 'label'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    labelname = db.Column(db.String(32), nullable=False)
    articles = db.relationship('Article', backref='label', lazy='dynamic')

    def __repr__(self):
        return '<Label %r>' % self.labelname


class Comment(db.Model):
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.String(256))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    article_id = db.Column(db.Integer, db.ForeignKey('article.id'))
    create_time = db.Column(db.DateTime, default=datetime.datetime.now())

    def __repr__(self):
        return '<Comment %r>' % self.content
