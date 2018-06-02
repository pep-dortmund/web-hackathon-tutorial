# hackathon tutorial

What really happenend


Install software:

```
$ pip install pipenv
```

In the root of this project, do

```
$ pipenv install
$ pipenv shell
(venv) $ gunicorn -k eventlet -b 0.0.0.0:5000 todo:app
```
