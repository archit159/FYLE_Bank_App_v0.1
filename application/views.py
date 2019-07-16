from application import application, Config, manage
from flask import render_template, redirect, request, make_response, send_from_directory, abort
import json, requests
import datetime
from functools import wraps
from flask_jwt_extended import create_access_token, create_refresh_token, fresh_jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt

@application.route('/')
def hello_world():
    return "Hello World!"

@application.route('/db')
def init_db():
    if(manage.init_db()):
        return 'Done'
    else:
        return 'Error'

@application.route('/create_jwt_token', methods=['GET'])
def create_jwt_token():
    access_token = create_access_token(identity='flask_app',fresh=datetime.timedelta(days=5))
    return access_token

@application.route('/bank_details', methods=['GET'])
@fresh_jwt_required
def bank_details():
    ifsc = request.args.get('ifsc')
    limit = request.args.get('limit')
    offset = request.args.get('offset')
    if ifsc is not None:
        return manage._find_from_ifsc(ifsc,limit,offset)
    else:
        return 'IFSC code not provided...'


@application.route('/branch_details', methods=['GET'])
@fresh_jwt_required
def branch_details():
    name = request.args.get('name')
    city = request.args.get('city')
    limit = request.args.get('limit')
    offset = request.args.get('offset')
    if name is not None and city is not None:
        return manage._find_from_name(name,city,limit,offset)
    else:
        return 'Bank Name and/or City not provided...'
