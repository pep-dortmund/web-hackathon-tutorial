from flask import Flask, render_template, request, jsonify, redirect, abort
from flask_login import login_required, current_user, login_user, logout_user

from datetime import datetime
import os

from .database import database, ToDo, User
from .auth import authenticate_user, login_manager

app = Flask(__name__)
app.config['DATABASE'] = os.getenv('TODO_DB', 'todo.sqlite')
app.config['SECRET_KEY'] = 'ABCD'

login_manager.init_app(app)


@app.before_first_request
def init():
    database.init(app.config['DATABASE'])
    database.create_tables([User, ToDo], safe=True)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/todos', methods=['GET'])
@login_required
def get_todo():
    todos = list(ToDo.select().where(ToDo.user_id == current_user.id).dicts())
    return jsonify(status="success", todos=todos)


@app.route('/todos', methods=['POST'])
@login_required
def add_todo():
    todo = ToDo(description=request.form['description'], user_id=current_user.id)

    if request.form['due_time']:
        date_str = request.form['due_date'] + 'T' + request.form['due_time']
        todo.due_date = datetime.strptime(date_str, '%Y-%m-%dT%H:%M')
    elif request.form['due_date']:
        todo.due_date = datetime.strptime(request.form['due_date'], '%Y-%m-%d')

    todo.save()
    return jsonify(status="success")


@app.route('/todos/<int:id>', methods=['DELETE'])
@login_required
def remove_todo(id):
    ToDo.delete().where(ToDo.id == id).execute()
    return jsonify(status="success")


@app.route('/todos/<int:id>', methods=['PUT'])
@login_required
def toggle_done(id):
    todo = ToDo.get(id=id)
    todo.done = not todo.done
    todo.save()
    return jsonify(status="success")


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    username = request.form['username']
    password = request.form['password']

    user = authenticate_user(username, password)

    if user is not None:
        login_user(user)
        return redirect('/')
    else:
        abort(404)


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    return redirect('/')
