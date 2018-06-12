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
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend/libs'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend/app'))

import coloredlogs, logging
logger = logging.getLogger(__name__)
coloredlogs.install(level='DEBUG', logger=logger)

from app import app_controller
from app.models import init_all
from navbar import NavBarDropMenu


nav_bar = NavBarDropMenu("HaoDuoYu")
nav_bar.add_drop_menu("Home", ["Contact"])
nav_bar.add_drop_menu("Service", ["List", "New"])
nav_bar.add_drop_menu("Users", ["List"])


app = dash.Dash()
#app.scripts.config.serve_locally=True

app.config.supress_callback_exceptions = True

# append css
#app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})

app.css.append_css({"external_url":
                    "https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css"})
app.scripts.append_script({"external_url":
                    "https://code.jquery.com/jquery-3.2.1.slim.min.js"})
app.scripts.append_script({"external_url":
                    "https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js"})
app.scripts.append_script({"external_url":
                    "https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js"})

app.layout = html.Div([
    # This "header" will persist across pages

    # Each "page" will modify this element
    nav_bar.components_tree(),
    # This Location component represents the URL bar
    dcc.Location(id='url', refresh=False),

    # Each "page" will modify this element
    html.Div(id='content-container-root'),


], className="container")



@app.callback(
    Output('content-container-root', 'children'),
    [Input('url', 'pathname')])
def display_page(pathname):
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
        cherrypy.tree.graft(app.server.wsgi_app, '/')
        cherrypy.config.update({'server.socket_host': '0.0.0.0',
                                'server.socket_port':80,
                                'engine.autoreload.on':False})
        try:
            cherrypy.engine.start()
        except KeyboardInterrupt:
            cherrypy.engine.stop()





