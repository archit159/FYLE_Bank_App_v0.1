from application import application, Config, manage
from flask import render_template, redirect, request, make_response, send_from_directory, abort
import json
from functools import wraps

@application.route('/')
def hello_world():
    return "Hello World!"

@application.route('/db')
def init_db():
    if(manage.init_db()):
        return 'Done'
    else:
        return 'Error'
