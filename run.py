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

@app.after_request
def after_request(response):
    response.headers.set('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response
'''
@app.route('/api/random')
def random_number():
    response = {
        'randomNumber': randint(1, 100)
    }
    return jsonify(response)
'''
@app.route('/<club_name>')
def catch_index(club_name):
    '''
    if app.debug:
        logger.debug("request frontend page!")
        return requests.get('http://localhost:8080/{}'.format(path)).text
    '''
    logger.debug(club_name)
    club =  app_controller.get_club_by_name(club_name)
    if not club:
       abort(404) 
    logger.debug(club)
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
        '''
        cherrypy.tree.graft(app.wsgi_app, '/')
        cherrypy.config.update({'server.socket_host': '0.0.0.0',
                                'server.socket_port':5000,
                                'engine.autoreload.on':False})
        try:
            cherrypy.engine.start()
        except KeyboardInterrupt:
            cherrypy.engine.stop()
        '''
        app.run(host='0.0.0.0', debug=True)
    
