#!/usr/bin/python
import sys
import os
from flask import Flask, render_template, jsonify, abort
from random import *
from flask_cors import CORS
import requests 
import cherrypy
import argparse

# add current folder and lib to syspath
sys.path.append(os.path.join(os.path.dirname(__file__)))
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend/libs'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend/app'))

import coloredlogs, logging
logger = logging.getLogger(__name__)
coloredlogs.install(level='DEBUG', logger=logger)

from app import app, app_controller
from app.models import init_all

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    '''
    if app.debug:
        logger.debug("request frontend page!")
        return requests.get('http://localhost:8080/{}'.format(path)).text
    '''
    logger.debug(path)
    return render_template("index.html")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run finishing app') 
    parser.add_argument('-i', '--init', help="Init all databasee etc", action='store_true')
    args = parser.parse_args()
    if args.init:
        init_all()
        pass
    else:
        for rule in app.url_map.iter_rules():
            logger.debug(rule)
        #'''
        cherrypy.tree.graft(app.wsgi_app, '/')
        cherrypy.config.update({'server.socket_host': '0.0.0.0',
                                'server.socket_port':80,
                                'engine.autoreload.on':False})
        try:
            cherrypy.engine.start()
        except KeyboardInterrupt:
            cherrypy.engine.stop()
        #'''
        #app.run(host='0.0.0.0', port=80, debug=True)
    
