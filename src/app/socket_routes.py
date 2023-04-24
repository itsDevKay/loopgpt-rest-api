from app import db, csrf, socketio
from app.helpers import *
from app.models import *

from flask_socketio import send, emit, join_room, leave_room

from dotenv import load_dotenv
from app.loopgpt import Agent

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
    query = data['query']
    app.logger.info(f'[✅] Query Received: "{query}"')

    a = Agent()
    a.name = 'Quazimoto'
    a.description = 'Lorem ipsum dolor isom'
    a.goals = [
        "Search for the best headphones on Google",
        "Analyze specs, prices and reviews to find the top 5 best headphones",
        "Write the list of the top 5 best headphones and their prices to a file",
        "Summarize the pros and cons of each headphone and write it to a different file called 'summary.txt'",
    ]
    app.logger.info(f'[✅] Agent [{a.name}] Started. Description: "{a.description}"')
    a.cli_socket(socketio, data, continuous=True)