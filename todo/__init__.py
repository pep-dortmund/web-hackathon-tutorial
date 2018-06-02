from flask import Flask, render_template, redirect, request, jsonify

from .database import ToDo

app = Flask(__name__)


@app.before_first_request
def init():
    ToDo.create_table(safe=True)


@app.route('/')
def index():
    todos = ToDo.select()
    return render_template('index.html', todos=todos)


@app.route('/todos', methods=['POST'])
def add_todo():
    ToDo.create(description=request.form['description'])
    return jsonify(status='ok')


@app.route('/todos/<int:id>', methods=['POST'])
def delete_todo(id):
    ToDo.delete().where(ToDo.id == id).execute()
    return jsonify(status='ok')


@app.route('/todos/<int:id>', methods=['PUT'])
def toggle_done(id):
    todo = ToDo.get(id=id)
    todo.done = not todo.done
    todo.save()
    return jsonify(status='ok')
