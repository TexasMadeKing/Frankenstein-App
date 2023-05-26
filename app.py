from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS

import os

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + os.path.join(basedir, 'app.sqlite')

db = SQLAlchemy(app)
ma = Marshmallow(app)
bcrypt = Bcrypt(app)
CORS(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(25), unique=True)
    date_created = db.Column(db.DateTime, default=datetime.datetime.now)
    completed = db.Column(db.Boolean, default=False)

    def __init__(self, title, date_created, completed):
        self.title = title
        self.date_created = date_created
        self.completed = completed

class TodoSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'date_created', 'completed')
        
todo_schema = TodoSchema()
todo_list_schema = TodoSchema(many=True)

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
