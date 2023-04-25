from app import db, csrf, socketio
from app.helpers import *
from app.models import *

from flask_socketio import send, emit, join_room, leave_room

from dotenv import load_dotenv
# from app.loopgpt import Agent

load_dotenv()
agents = []

@socketio.on('join_room')
def handle_join_room(data):
    join_room(data['room'])
    socketio.emit('join_room_announcement', data, room=data['room'])
    app.logger.info(f'[✅] Room: {data["room"]} was joined successfully.')

@socketio.on('room_left')
def room_left_handler(data):
    leave_room(data['room'])
    app.logger.info(f'[✅] Room: {data["room"]} was left successfully.')

@socketio.on('query_gpt')
def query_gpt(data):
    room = data['room']
    goals = data['goals']
    app.logger.info(f'[✅] Goals Received: "{goals}"')

    # START DOCKER CONTAINER WITH ENV VARIABLES
    # ...
    app.logger.info(f'[✅] Docker container started. Agent loading.."')
    socketio.emit(
        'docker_container_started',
        f'[✅] Docker container started. Agent loading.."',
        room=room
    )

@socketio.on('gpt_response')
def gpt_response(data):
    room = data['room']
    message = data['message']
    socketio.emit('gpt_response', message, room=room)
    app.logger.info(f'[✅] GPT Responded successfully to room [ {room} ] with message.')