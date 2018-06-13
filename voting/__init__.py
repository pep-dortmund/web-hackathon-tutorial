from flask import Flask, render_template, request, jsonify
from .database import Vote, Team
from flask_socketio import SocketIO
import eventlet
from peewee import IntegrityError
from playhouse.shortcuts import model_to_dict

eventlet.monkey_patch()

app = Flask(__name__)
socket = SocketIO(app)


@app.before_first_request
def init():
    Vote.create_table(safe=True)
    Team.create_table(safe=True)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/teams')
def get_teams():
    return jsonify(status='ok', teams=list(Team.select().dicts()))


@app.route('/team', methods=['POST'])
def add_team():
    teamname = request.form.get('teamname')
    voteable = request.form.get('voteable', 'True') == 'True'
    try:
        Team.create(name=teamname, voteable=voteable)
    except IntegrityError as e:
        return jsonify(status='error', message='team already exists'), 400
    return jsonify(status='ok')


@app.route('/team/<name>', methods=['PUT'])
def update_team(name):
    team = Team.get(name=name)
    if 'teamname' in request.form:
        team.name = request.form.get('teamname')
    if 'voteable' in request.form:
        team.voteable = request.form.get('voteable', 'True') == 'True'
    if 'members' in request.form:
        team.members = int(request.form.get('members'))
    team.save()
    return jsonify(status='ok', team=model_to_dict(team))


@app.route('/votes')
def get_votes():
    return jsonify(status='ok', votes=list(Vote.select().dicts()))


@app.route('/votes/delete', methods=['DELETE'])
def delete_votes():
    hits = Vote.delete().execute()
    return jsonify(status='ok', hits=hits)


@app.route('/vote', methods=['POST'])
def add_todo():
    team = Team.get(name=request.form.get('team'))
    idea = Team.get(name=request.form.get('idea'))
    implementation = Team.get(name=request.form.get('implementation'))
    progress = Team.get(name=request.form.get('progress'))
    try:
        Vote.create(team=team, idea=idea, progress=progress,
                implementation=implementation)
    except IntegrityError as e:
        return jsonify(status='error', message='no more votes allowed'), 400
    return jsonify(status='ok')


@app.route('/winner')
def winnder():
    results = []
    for t in Team.select():
        points = len(t.progress_votes) +  len(t.idea_votes) + len(t.implementation_votes)
        if t.name == 'guido':
            points *= 3
        results.append((t.name, points))

    return jsonify(results)
