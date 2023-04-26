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

@socketio.on('list_agents')
def list_active_agents():
    socketio.emit('list_agents_response', agents, room='agent_manager')

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
    socket_server = 'http://192.168.0.222:8000'
    room = data['room']
    agent_name = data['agent_name']
    agent_description = data['agent_description']
    goals = data['goals']
    str_goals = ''
    for g in goals: str_goals += f'{str(g)}/;'

    agent_continuous = data['agent_continuous']
    openai_api_key = data['OPENAI_API_KEY']

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
    resp = dmanager.run_image(
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
        'container': resp['response'].__dict__,
        'initiated_at': datetime.datetime.utcnow()
    }
    app.logger.info(agent_info)
    agents.append(agent_info)

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

@socketio.on('kill_container')
def kill_container(data):
    room = data['room']
    container_id = data['container_id']
    container = dmanager.get_container(container_id)
    if container['status'] != 200:
        socketio.emit('kill_response', f'No container found with id: {container_id}', room=room)
        return
    container.kill()
    socketio.emit('kill_response', f'Container [ {container_id} ] has been killed.', room=room)