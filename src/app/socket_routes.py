from app import db, csrf, socketio
from app.helpers import *
from app.models import *
from app.docker_manager.DockerController import DockerController

from flask_socketio import send, emit, join_room, leave_room
from dotenv import load_dotenv

import datetime

load_dotenv()
agents = []
dmanager = DockerController()

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
    socket_server = '127.0.0.1:8000'
    room = data['room']
    agent_name = data['name']
    agent_description = data['description']
    goals = data['goals']
    str_goals = ''
    for g in goals: str_goals += f'{str(g)}/;'

    agent_continuous = data['continuous']
    openai_api_key = data['openai_api_key']

    app.logger.info(f'[✅] Goals Received: "{goals}"')

    env_variables = {
        'agent_name': agent_name,
        'agent_description': agent_description,
        'agent_goals': str_goals,
        'agent_continuous': agent_continuous,
        'OPENAI_API_KEY': openai_api_key,
        'socket_server': socket_server,
        'socket_room': room
    }

    # START DOCKER CONTAINER WITH ENV VARIABLES
    # ...
    resp = dmanager.run(
        image = 'turbogpt',
        environment = env_variables
    )
    if resp['status'] != 200:
        socketio.emit(
            'image_failed_to_run',
            resp['response'],
            room=room    
        )
        return
    
    agent_info = {
        'room': room,
        'container': resp['response'][0],
        'initiated_at': datetime.datetime.utcnow()
    }
    app.logger.info(agent_info)
    agents.push(agent_info)

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