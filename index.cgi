#!/usr/local/bin/python3
from wsgiref.handlers import CGIHandler
from helloFlask import app
CGIHandler().run(app)