from flask import Flask, render_template, request, jsonify
from .database import ToDo
from flask_socketio import SocketIO
import eventlet

eventlet.monkey_patch()

app = Flask(__name__)
socket = SocketIO(app)


@app.before_first_request
def init():
    ToDo.create_table(safe=True)


@app.route('/')
def index():
    todos = ToDo.select()
    return render_template('index.html', todos=todos)


@app.route('/todos')
def get_todos():
    todos = list(ToDo.select().dicts())
    return jsonify(status='ok', todos=todos)


@app.route('/todos', methods=['POST'])
def add_todo():
    description = request.form.get('description')
    if not description:
        return jsonify(message='Missing description'), 400
    ToDo.create(description=description)
    socket.emit('update')
    return jsonify(status='ok')


@app.route('/todos/<int:id>', methods=['DELETE'])
def delete_todo(id):
    try:
        ToDo.delete().where(ToDo.id == id).execute()
    except ToDo.DoesNotExist:
        return jsonify(status='error', message='Todo {} does not exist'.format(id)), 400
    socket.emit('update')
    return jsonify(status='ok')


@app.route('/todos/<int:id>', methods=['PUT'])
def toggle_done(id):
    todo = ToDo.get(id=id)
    todo.done = not todo.done
    todo.save()
    socket.emit('update')
    return jsonify(status='ok')
