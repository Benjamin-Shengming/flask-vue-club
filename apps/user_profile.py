#!/usr/bin/python3
from collections import OrderedDict
from uuid import uuid1
import base64
import dash
import json
import dash_core_components as dcc
import dash_html_components as html
from dash.exceptions import PreventUpdate
from dash.dependencies import Event, State, Input, Output
from pprint import pprint
from app import app
from app import app_controller
import filestore
from magic_defines import *
import local_storage

import coloredlogs, logging
logger = logging.getLogger(__name__)
coloredlogs.install(level='DEBUG', logger=logger)

profile_layout = html.Div(className="tab-pane", id="edit", children=[
    html.Form(role="form", children=[
        html.Div(className="form-group row", children=[
            html.Label("First name", className="col-lg-3 col-form-label form-control-label"),
            html.Div(className="col-lg-9", children=[
                dcc.Input(className="form-control", type="text", value="Jane")
            ])
        ]),
        html.Div(className="form-group row", children=[
            html.Label("First name", className="col-lg-3 col-form-label form-control-label"),
            html.Div(className="col-lg-9", children=[
                dcc.Input(className="form-control", type="text", value="Jane")
            ])
        ]),
        html.Div(className="form-group row", children=[
            html.Label(className="col-lg-3 col-form-label form-control-label"),
            html.Div(className="col-lg-9", children=[
                dcc.Input(type="reset",className="btn btn-secondary", value="Cancel"),
                dcc.Input(type="button",className="btn btn-primary", value="Save Changes")
            ])
        ])
    ])
])


def layout():
    logger.debug("profile layout")
    return html.Div(className="container", children=[
        profile_layout
    ])

