from app import app, db
from app.models import *

from flask import request
from itsdangerous import Signer
from itsdangerous.url_safe import URLSafeTimedSerializer
from itsdangerous.exc import SignatureExpired, BadTimeSignature, BadData

# Default Libraries
import os
import re
import string
import hashlib
import requests
import datetime

from random import choice, shuffle
from pprint import pprint
from uuid import uuid4
	
def get_username(current_user):
	username = (
        current_user.first_name.capitalize() + ' ' + current_user.last_name.capitalize()
    )
	return username

def find_user_by_uuid(u_uuid):
	u = db.session.query(Users).filter(
		Users.uuid == u_uuid
	).first()
	if u:
		return u
	return None

def find_uuid_by_email(email):
    u = Users.query.filter(
        Users.email == email
    ).first()
    return u.uuid

def find_user_by_email(email):
	u = db.session.query(Users).filter(
		Users.email == email
	).first()
	if u:
		return u
	return None

def add_to_db(obj):
	db.session.add(obj)
	db.session.commit()

def delete_item_from_db(item):
	db.session.delete(item)
	db.session.commit()
	return 200

def contains_proper_characters(string, regex):
	string_check = re.compile(regex)
	if string_check.search(string) == None:
		return False
	return True

def check_password_validation(password):
	# special_characters = contains_proper_characters(password, f'[{string.punctuation}]')
	# contains_digits = any(char.isdigit() for char in password)
	# contains_capitals = contains_proper_characters(password, '[A-Z]')
	# contains_lowercase = contains_proper_characters(password, '[a-z]')

	# if (special_characters and contains_digits and 
	# 	contains_capitals and contains_lowercase
	# 	and len(password) >= 8):
	if (len(password) >= 8):
		return True
	return False

def request_visitor_ip_address():
	if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
		visitor_ip = request.environ['REMOTE_ADDR']
	else:
		visitor_ip = request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)
	return visitor_ip

def log_ip_to_database(user_id, status):
	visitor_ip = request_visitor_ip_address()
	ip_address = IPAddresses(
		ip_address = visitor_ip, # create function to get ip address
		user_id = user_id,
		user_status = status
	)
	db.session.add(ip_address)
	db.session.commit()

def change_user_status(u_uuid, status):
	u = find_user_by_uuid(u_uuid)
	if u: u.status = status
	else: return 'No user found'
	db.session.commit()
	return f'User status changed for [ {u.email} ] to [ {u.status} ]'

def find_chat_participants_by_uuid(uuid, participant):
    cp = ChatParticipants.query.filter(
        ChatParticipants.chatroom == uuid
    ).filter(
        ChatParticipants.user == participant
    ).first()
    if cp: 
        print(f'ChatParticipant ID: {cp.id}') 
        return cp
    print('No ChatParticipant found')
    return None

def find_chatroom_by_uuid(c_uuid):
    c = Chatrooms.query.filter(
        Chatrooms.uuid == c_uuid
    ).first()
    if c: return c
    return None

def create_chatroom(host_uuid):
    print('creating chatroom')
    c_uuid = str(uuid4())
    chat_exists = find_chatroom_by_uuid(c_uuid)
    if chat_exists:
        print('chat exists')
        create_chatroom(host_uuid)
    else:
        print('no chat found. Making new room.')
        chatroom = Chatrooms(
        uuid = c_uuid,
        host = host_uuid,
        )
        db.session.add(chatroom)
        participant = ChatParticipants(
            user_uuid = host_uuid,
            chatroom = c_uuid
        )
        db.session.add(participant)
        db.session.commit()
        return chatroom.uuid

def get_time_since(last_updated):
    current = datetime.datetime.utcnow()
    duration = current - last_updated
    duration_in_s = duration.total_seconds()

    days = divmod(duration_in_s, 86400)
    hours = divmod(days[1], 3600)
    minutes = divmod(hours[1], 60)
    seconds = divmod(minutes[1], 1)

    if int(days[0]) > 0: return f'{int(days[0])}days ago'
    if int(days[0]) == 0 and int(hours[0]) > 0:
        return f'{int(hours[0])}hr ago'
    if int(hours[0]) == 0 and int(minutes[0]) > 0:
        return f'{int(minutes[0])} mins ago'
    return 'now'

def generate_random_string(length):
    random_string = ''
    characters = [c for c in f'{string.ascii_letters}{string.digits}']
    shuffle(characters)
    shuffle(characters)

    for _ in range(0, length):
        char = choice(
            [characters[c] for c in range(0, len(characters))]
        )
        random_string += str(char)
    return random_string.upper()

def get_username_by_email(email):
    u = find_user_by_email(email)
    if u:
        u = f'{u.first_name} {u.last_name}'
        return u
    return None

def get_user_fullname_by_id(uuid):
    u = Users.query.get(uuid)
    if not u: return None
    return f'{u.first_name} {u.last_name}'
