#!/usr/bin/python3
import sys
import os
from random import *
import flask
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
from navbar import NavBar


app = dash.Dash(__name__, static_folder='assets')
#app.scripts.config.serve_locally=True
app.config.supress_callback_exceptions = True

# css logical
css_directory = os.path.dirname(__name__) + "/assets/css/"
stylesheets_local =  ['sidebar.css']   # local style sheet need to use
def serve_stylesheet(stylesheet):
    if stylesheet not in stylesheets_local:
        raise Exception(
                    '"{}" is excluded from the allowed static files'.format(
                        stylesheet
                    )
                )
    return flask.send_from_directory(css_directory, stylesheet)

# append other css
#app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})
app.css.append_css({"external_url":
                    "https://use.fontawesome.com/releases/v5.0.13/css/all.css"})
app.css.append_css({"external_url":
                    "https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css"})
app.scripts.append_script({"external_url":
                    "https://code.jquery.com/jquery-3.2.1.slim.min.js"})
app.scripts.append_script({"external_url":
                    "https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js"})
app.scripts.append_script({"external_url":
                    "https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js"})

# append local css
for stylesheet in stylesheets_local:
    app.css.append_css({"external_url": "/assets/css/{}".format(stylesheet)})


total = html.Div(className="container-fluid h-100", children=[
    html.Div(className="row d-flex flex-lg-column flex-row",children=[
        html.Aside(className="col-2 col-lg-12 h-md-100 p-0 bg-dark fixed-top",children=[
            html.Nav(className="navbar navbar-expand navbar-dark bg-dark py-2 px-0 px-lg-2", children=[
                html.Div(className="collapse navbar-collapse", id="nav", children=[
                    html.Ul(className="flex-column flex-lg-row navbar-nav w-100 justify-content-center align-items-center align-items-sm-start text-left text-lg-center", children=[
                        html.Li(className="nav-item w-100",children=[
                            dcc.Link(className="nav-link active text-nowrap",
                                   href="/main",
                                   children=[
                                       html.I(className="fa fa-bullseye fa-fw"),
                                       html.Span("Brand", className="d-none d-sm-inline font-weight-bold")
                                   ],
                                   style={"cursor":"pointer"})
                        ]),

                        html.Li(className="nav-item w-100",children=[
                            dcc.Link(className="nav-link active text-nowrap",
                                   href="/link",
                                   children=[
                                       html.I(className="fa fa-heart fa-fw"),
                                       html.Span("Link", className="d-none d-sm-inline")
                                   ],
                                   style={"cursor":"pointer"})
                        ]),
                    ])
                ])
            ])
        ]),
        html.Main(className="col offset-2 offset-lg-0 bg-faded py-2",
                  id="main",
                  children=[
                    html.H1("A Bootstrap 4 example")
                  ])
    ])
])

major_area = html.Div(**{"data-spy": "scroll",
                         "data-target: "#nav",
                         "data-offset":"5"},
                         className="pt-lg-5 pt-1", children=[total])


app.layout = html.Div(children=[
    major_area,
    # This Location component represents the URL bar
    dcc.Location(id='url', refresh=False),
])

@app.callback(
    Output('main', 'children'),
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
        '''
        else:
            for rule in app.server.url_map.iter_rules():
                logger.debug(rule)
            app.run_server(debug=True)
        '''
    else:
        for rule in app.server.url_map.iter_rules():
            logger.debug(rule)
        cherrypy.tree.graft(app.server.wsgi_app, '/')
        cherrypy.config.update({'server.socket_host': '0.0.0.0',
                                'server.socket_port':8080,
                                'engine.autoreload.on':False})
        try:
            cherrypy.engine.start()
        except KeyboardInterrupt:
            cherrypy.engine.stop()




