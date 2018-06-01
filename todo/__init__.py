from flask import Flask, render_template, redirect, request

app = Flask(__name__)

todos = []


@app.route('/')
def index():
    return render_template('index.html', todos=todos)


@app.route('/todos', methods=['POST'])
def add_todo():
    todos.append(request.form['description'])
    return redirect('/')


@app.route('/todos/<int:index>', methods=['DELETE'])
def delete_todo(index):
    todos.pop(index)
    return redirect('/')
