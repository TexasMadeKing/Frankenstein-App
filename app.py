from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
import os
import datetime

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + os.path.join(basedir, 'app.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable modification tracking

db = SQLAlchemy(app)
ma = Marshmallow(app)
CORS(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(25), unique=True)
    date_created = db.Column(db.DateTime, default=datetime.datetime.now)
    completed = db.Column(db.Boolean, default=False)

    def __init__(self, title, completed=False):
        self.title = title
        self.completed = completed

class TodoSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'date_created', 'completed')

todo_schema = TodoSchema()
todos_schema = TodoSchema(many=True)

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(25), unique=True)
    description = db.Column(db.String(300), unique=True)
    pages = db.Column(db.Integer, unique=True)

    def __init__(self, title, description, pages):
        self.title = title
        self.description = description
        self.pages = pages

class NoteSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'description', 'pages')

note_schema = NoteSchema()
notes_schema = NoteSchema(many=True)


class Calendar(db.Model):
    day = db.Column(db.Integer, primary_key=True)
    month = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200), unique=True)

    def __init__(self, day, month, year, text):
        self.day = day
        self.month = month
        self.year = year
        self.text = text
        
class CalendarSchema(ma.Schema):
    class Meta:
        fields = ('day', 'month', 'year', 'text')

calendar_schema = CalendarSchema()
calendars_schema = CalendarSchema(many=True)


# Routes
@app.route('/todos', methods=['GET'])
def get_todos():
    all_todos = Todo.query.all()
    result = todos_schema.dump(all_todos)
    return jsonify(result)

@app.route('/todos', methods=['POST'])
def add_todo():
    title = request.json['title']
    new_todo = Todo(title)
    db.session.add(new_todo)
    db.session.commit()
    return todo_schema.jsonify(new_todo)

@app.route('/todos/<int:todo_id>', methods=['PUT'])
def update_todo(todo_id):
    todo = Todo.query.get(todo_id)
    title = request.json['title']
    todo.title = title
    db.session.commit()
    return todo_schema.jsonify(todo)

@app.route('/todos/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    todo = Todo.query.get(todo_id)
    db.session.delete(todo)
    db.session.commit()
    return todo_schema.jsonify(todo)

@app.route('/notes', methods=['GET'])
def get_notes():
    all_notes = Note.query.all()
    result = notes_schema.dump(all_notes)
    return jsonify(result)

@app.route('/notes', methods=['POST'])
def add_note():
    title = request.json['title']
    description = request.json['description']
    pages = request.json['pages']
    new_note = Note(title, description, pages)
    db.session.add(new_note)
    db.session.commit()
    return note_schema.jsonify(new_note)

@app.route('/notes/<int:note_id>', methods=['PUT'])
def update_note(note_id):
    note = Note.query.get(note_id)
    title = request.json['title']
    description = request.json['description']
    pages = request.json['pages']
    note.title = title
    note.description = description
    note.pages = pages
    db.session.commit()
    return note_schema.jsonify(note)

@app.route('/notes/<int:note_id>', methods=['DELETE'])
def delete_note(note_id):
    note = Note.query.get(note_id)
    db.session.delete(note)
    db.session.commit()
    return note_schema.jsonify(note)

@app.route('/calendars', methods=['GET'])
def get_calendars():
    all_calendars = Calendar.query.all()
    result = calendars_schema.dump(all_calendars)
    return jsonify(result)

@app.route('/calendars', methods=['POST'])
def add_calendar():
    day = request.json['day']
    month = request.json['month']
    year = request.json['year']
    text = request.json['text']
    new_calendar = Calendar(day, month, year, text)
    db.session.add(new_calendar)
    db.session.commit()
    return calendar_schema.jsonify(new_calendar)

@app.route('/calendars/<int:day>/<int:month>/<int:year>', methods=['GET'])
def get_calendar(day, month, year):
    calendar = Calendar.query.filter_by(day=day, month=month, year=year).first()
    return calendar_schema.jsonify(calendar)

@app.route('/calendars/<int:day>/<int:month>/<int:year>', methods=['PUT'])
def update_calendar(day, month, year):
    calendar = Calendar.query.filter_by(day=day, month=month, year=year).first()
    text = request.json['text']
    calendar.text = text
    db.session.commit()
    return calendar_schema.jsonify(calendar)

@app.route('/calendars/<int:day>/<int:month>/<int:year>', methods=['DELETE'])
def delete_calendar(day, month, year):
    calendar = Calendar.query.filter_by(day=day, month=month, year=year).first()
    db.session.delete(calendar)
    db.session.commit()
    return calendar_schema.jsonify(calendar)

# Run the application
if __name__ == '__main__':
    app.run(debug=True)
