from flask import Flask, render_template, request, redirect


app = Flask(__name__)

todos = [
    'HTML erklären',
    'Flask / HTTP erklären',
    'CSS / Bootstrap erklären',
    'Datenbanken / ORM erklären',
    'Javascript / Vue erklären',
]


@app.route('/')
def index():
    return render_template('index.html', todos=todos)


@app.route('/todos', methods=['POST'])
def add_todo():
    todos.append(request.form['todo'])
    return redirect('/')
