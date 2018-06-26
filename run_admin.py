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
#from navbar import NavBar


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
                    "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.css"})
app.css.append_css({"external_url":
                    "https://use.fontawesome.com/releases/v5.1.0/css/all.css"})
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


sider_bar = html.Div(className="col-md-3 float-left col-1 pl-0 pr-0 collapse width show", id="sidebar", children=[
                html.Div(className="list-group border-0 card text-center text-md-left", children=[
                    dcc.Link(href="/home", className="list-group-item d-inline-block collapsed", style={"cursor":"pointer"}, children=[
                        html.I(**{"aria-hidden":"true"},className="fa fa-home"),
                        html.Span("Home", className="d-none d-md-inline")
                    ]),
                    html.A(**{"data-toggle": "collapse", "aria-expanded": "false"}, href="#menu1", className="list-group-item d-inline-block collapsed", children=[
                        html.I(**{"aria-hidden":"true"},className="fa fa-home"),
                        html.Span("Home", className="d-none d-md-inline")
                    ]),
                    html.Div(**{"data-parent":"#sidebar"}, className="collapse", id="menu1", children=[
                        html.A("Subitem 1", **{"data-toggle":"collapse", "aria-expanded":"false"}, href="#menu1sub1", className="list-group-item"),
                        html.Div(className="collapse", id="menu1sub1", **{"data-parent":"#menu1"}, children=[
                            html.A("subitem a", **{"data-parent":"#menu1sub1"}, href="#", className="list-group-item"),
                            html.A("subitem b", **{"data-parent":"#menu1sub1"}, href="#", className="list-group-item"),
                            html.A("subitem c", **{"data-toggle":"collapse","aria-expanded":"false"}, href="#menu1sub1sub1", className="list-group-item"),
                            html.Div(className="collapse", id="menu1sub1sub1", children=[
                                html.A("Subitem c.1", **{"data-parent": '#menu1sub1sub1'}, href="#", className="list-group-item"),
                                html.A("subitme c.2", **{"data-parent":"#menu1sub1sub1"}, href="#", className="list-group-item")
                            ])
                        ]),
                        html.A("SubItem 3", href="#", className="list-group-item")
                    ]),
                    html.A(href="#", className="list-group-item d-inline-block collapsed", children=[
                        html.I(className="fa fa-film"),
                        html.Span("item 2", className="d-none d-md-inline")
                    ]),
                    html.A(**{"data-toggle":"collapse","aria-expanded":"false"}, href="#menu3", className="list-group-item d-inline-block collapsed", children=[
                        html.I(className="fa fa-book"),
                        html.Span("Item 3", className="d-none d-md-inline")
                    ]),
                    html.Div(**{"data-parent":'#sidebar'}, className="collapse", id="menu3", children=[
                        html.A("3.1", **{"data-parent":'#menu3'}, href="#", className="list-group-item"),
                        html.A("3.2", **{"data-toggle":"collapse","aria-expanded":"false"}, href="#menu3sub2",className="list-group-item"),
                        html.Div(className="collapse", id="menu3sub2", children=[
                        html.A("3.2.a", **{"data-parent":"#menu3sub2"}, href="#", className="list-group-item"),
                        html.A("3.2.b", **{"data-parent":"#menu3sub2"}, href="#", className="list-group-item"),
                        html.A("3.2.c", **{"data-parent":"#menu3sub2"}, href="#", className="list-group-item"),
                        ]),
                        html.A("3.3",**{"data-parent":"#menu3"}, href="#", className="list-group-item")
                    ])
                ])

])


main_area = html.Main(className="col-md-9 float-left col px-5 pl-md-2 pt-2 main", children=[
                html.A(**{"data-target":"#sidebar", "data-toggle":"collapse"}, href="#", children=[
                    html.I(className="fa fa-navicon fa-2x py-2 p-1")
                ]),
                html.Div(id="content-container-root", className="page-header", children=[
                    html.H2("Bootstrap 4 Sidebar Menu")
                ]),
])

total = html.Div(className="container-fluid", children=[
    html.Div(className="row d-flex d-md-block flex-nowrap wrapper", children=[
        sider_bar,
        main_area
    ])
])

app.layout = html.Div(children=[
    total,
    # This Location component represents the URL bar
    dcc.Location(id='url', refresh=False),
])

@app.callback(
    Output('content-container-root', 'children'),
    [Input('url', 'pathname')])
def display_page(pathname):
    print(pathname)
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




