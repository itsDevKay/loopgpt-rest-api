FROM ubuntu:22.04

# Disable Prompt During Packages Installation
ARG DEBIAN_FRONTEND=noninteractive
RUN apt update
RUN apt-get install -y git python3-pip
RUN pip3 install python-socketio[client] flask flask-sqlalchemy flask-cors flask-wtf flask-socketio simple-websocket 
RUN git clone https://github.com/itsDevKay/loopgpt-socket-api
RUN python3 -m pip install -r /loopgpt-socket-api/requirements.txt
RUN PYTHONPATH=$PYTHONPATH:/loopgpt-socket-api/src/app

CMD ["/loopgpt-socket-api/src/app/loopgpt/run_cli_socket.py"]
ENTRYPOINT ["/usr/bin/python3"]
