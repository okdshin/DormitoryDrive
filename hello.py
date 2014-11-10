import os
import flask

app = flask.Flask(__name__)

@app.route('/')
def index():
    return flask.render_template("index.html")

@app.route('/hello')
def hello():
    return 'Hello World!'
