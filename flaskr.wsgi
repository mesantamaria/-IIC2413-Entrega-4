#!/usr/bin/python3
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/Entrega4/")
from flaskr import app as application
application.secret_key = '123'

