from flask import (
	jsonify,
	request
)
from sqlalchemy import desc
from sqlalchemy.orm import load_only
from werkzeug.exceptions import NotFound

from app.helpers import *
from app.models import *
from app import db, csrf

from pprint import pprint

import os
import json
import time
import datetime

from flask_wtf.csrf import CSRFError
@app.errorhandler(CSRFError)
def handle_csrf_error(e):
    return jsonify(message='This request is invalid.', reason=e.description), 400

@app.route('/status')
@csrf.exempt
def status():
    return jsonify(status='running')