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
import local_storage
from magic_defines import *
import sd_material_ui
from sd_material_ui import Snackbar
import coloredlogs, logging
from utils import *
from autolink import Redirect
from localstorage_writer import LocalStorageWriter
from localstorage_reader import LocalStorageReader

import coloredlogs, logging
logger = logging.getLogger(__name__)
coloredlogs.install(level='DEBUG', logger=logger)

def gen_id(name):
    # user module as name prefix
    s_id = g_id(__name__, name)
    logger.debug(s_id)
    return s_id


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
                html.Span("  "),
                dcc.Input(type="button",className="btn btn-primary", value="Save Changes")
            ])
        ])
    ])
])


timer = dcc.Interval(
            id=gen_id(TIMER),
            interval=1*1000, # in milliseconds
            n_intervals=0)
user_info_reader = LocalStorageReader(id=gen_id(STORAGE_R), label=USER_STORAGE)


def layout():
    return html.Div(id=gen_id(ROOT), children=[
        timer,
        user_info_reader,
        html.Div(id=gen_id(PLACEHOLDER))
    ])


###
@app.callback(Output(gen_id(PLACEHOLDER), 'children'),
              [Input(gen_id(TIMER), 'n_intervals')],
              [State(gen_id(STORAGE_R), 'value')])
def update_profile(interval, jwt):
    logger.debug("update profile, jwt is {}".format(jwt))
    if not jwt:
        return [dcc.Link("Please login firstly!", href="/user/login")]

    user = app_controller.get_club_user_by_jwt(CLUB_NAME, jwt)
    if not user:
        return [html.H1("Login expires, relogin again!")]

    return profile_layout

