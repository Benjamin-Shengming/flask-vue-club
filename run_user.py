#!/usr/bin/python3
import sys
import os
from random import *
from flask_cors import CORS
from flask import Flask, render_template, jsonify, abort, make_response
import requests
import cherrypy
import argparse
import dash
from dash.dependencies import Input, State, Output
import dash_html_components as html
import dash_core_components as dcc
import pandas as pd

# add current folder and lib to syspath
sys.path.append(os.path.join(os.path.dirname(__file__)))
sys.path.append(os.path.join(os.path.dirname(__file__), 'libs'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'apps'))

import coloredlogs, logging
logger = logging.getLogger(__name__)
coloredlogs.install(level='DEBUG', logger=logger)

import user_service_list
import user_service_book
import user_register
import user_activate
from app import app
from app import app_controller
from models import init_all
from navbar import NavBarDropMenu

nav_bar = NavBarDropMenu("HaoDuoYu")
nav_bar.add_drop_menu("Home", ["Contact"])
nav_bar.add_drop_menu("Service", ["List", "New"])
nav_bar.add_drop_menu("User", ["Login", "Register", "Profile"])



app.layout = html.Div([

    # hidden div used to store data
    html.Div(id='global-hiden-user-info', style={"display":"None"}),
    nav_bar.components_tree(),
    # This Location component represents the URL bar
    dcc.Location(id='global-url', refresh=False),
    # Each "page" will modify this element
    html.Div(id='content-container-root'),

], className="container-fluid")



@app.callback(
    Output('content-container-root', 'children'),
    [Input('global-url', 'pathname')])
def display_page(pathname):
    if not pathname:
        return user_service_list.layout()

    p = pathname.lower()
    if p == "/service/list":
        return user_service_list.layout()

    if "/service/book/" in p:
        service_id = p.split("/")[-1]
        if service_id:
            return user_service_book.layout(service_id)
    if p == "/user/login":
        return user_login.login_layout()

    if p == "/user/register":
        return user_register.register_layout()

    if "/user/activate" in p:
        user_id = p.split("/")[-1]
        if user_id:
            return user_activate.layout(user_id)

    return pathname



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run finishing app')
    parser.add_argument('-i', '--init', help="Init all databasee etc", action='store_true')
    args = parser.parse_args()
    if args.init:
        init_all()
        pass
    else:
        for rule in app.server.url_map.iter_rules():
            logger.debug(rule)
        app.run_server(debug=True, host='0.0.0.0', port=80)
        '''
        cherrypy.tree.graft(app.server.wsgi_app, '/')
        cherrypy.config.update({'server.socket_host': '0.0.0.0',
                                'server.socket_port':80,
                                'engine.autoreload.on':False})
        try:
            cherrypy.engine.start()
        except KeyboardInterrupt:
            cherrypy.engine.stop()
        '''




