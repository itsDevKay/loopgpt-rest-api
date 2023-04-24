#!/var/www/html/digicar/venv/bin/python
import sys
import os
sys.path.insert(0, '/var/www/html/digicar')

def application(req_environ, start_response):
    os.environ['SECRET_KEY'] = req_environ['SECRET_KEY']
    os.environ['OPENAPI_KEY'] = req_environ['OPENAPI_KEY]

    from app import app as _application

    return _application(req_environ, start_response)