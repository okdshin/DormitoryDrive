import os
from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return 'this is index page'

@app.route('/hello')
def hello():
    return 'Hello World!'
