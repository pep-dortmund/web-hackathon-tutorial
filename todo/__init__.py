from flask import Flask, render_template, request, jsonify

from .database import database, ToDo
from datetime import datetime
import os


app = Flask(__name__)
app.config['DATABASE'] = os.getenv('TODO_DB', 'todo.sqlite')


@app.before_first_request
def init():
    database.init(app.config['DATABASE'])
    ToDo.create_table(safe=True)


@app.route('/')
def index():
    todos = list(ToDo.select().dicts())
    return render_template('index.html', todos=todos)


@app.route('/todos', methods=['GET'])
def get_todo():
    todos = list(ToDo.select().dicts())
    return jsonify(status="success", todos=todos)


@app.route('/todos', methods=['POST'])
def add_todo():
    todo = ToDo(description=request.form['todo'])

    if request.form['due_time']:
        date_str = request.form['due_date'] + 'T' + request.form['due_time']
        todo.due_date = datetime.strptime(date_str, '%Y-%m-%dT%H:%M')
    elif request.form['due_date']:
        todo.due_date = datetime.strptime(request.form['due_date'], '%Y-%m-%d')

    todo.save()
    return jsonify(status="success")


@app.route('/todos/<int:id>', methods=['DELETE'])
def remove_todo(id):
    ToDo.delete().where(ToDo.id == id).execute()
    return jsonify(status="success")


@app.route('/todos/<int:id>', methods=['PUT'])
def toggle_done(id):
    todo = ToDo.get(id=id)
    todo.done = not todo.done
    todo.save()
    return jsonify(status="success")
