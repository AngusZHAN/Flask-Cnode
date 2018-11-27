from . import main
from flask import render_template


@main.route('/')
@main.route('/index/')
def index():
    return render_template('index.html')


@main.route('/detail/')
def detail():
    return render_template('detail.html')
