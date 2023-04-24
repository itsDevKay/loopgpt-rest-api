from flask import (
	jsonify,
    redirect,
	request,
    render_template,
    url_for
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

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/chat', methods=['GET'])
def chat():
    room = request.args.get('room')
    if room:
        return render_template('chat.html', room=room)
    return redirect(url_for('index'))