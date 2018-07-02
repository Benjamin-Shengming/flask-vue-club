#!/usr/bin/python3
from collections import OrderedDict
from uuid import uuid1
import base64
import dash
import json
import dash_core_components as dcc
import dash_html_components as html
import sd_material_ui
from dash.dependencies import Event, State, Input, Output
from pprint import pprint
from app import app
from app import app_controller
import filestore
from magic_defines import *


import coloredlogs, logging
logger = logging.getLogger(__name__)
coloredlogs.install(level='DEBUG', logger=logger)


register_title_row = html.Div(className="row", children=[
                html.Div(className="col-md-3"),
                html.Div(className="col-md-6", children=[
                    html.H2("Register New User"),
                    html.Hr()
                ])
            ])
email_row = html.Div(className="row", children=[
                html.Div(className="col-md-3 field-label-responsive", children=[
                    html.Label("E-Mail Address", htmlFor="email")
                ]),
                html.Div(className="col-md-6", children=[
                    html.Div(className="form-group", children=[
                        html.Div(className="input-group mb-2 mr-sm-2 mb-sm-0", children=[
                            html.Div(className="input-group-addon", style={"width": "2.6rem"}, children=[
                                html.I(className="fa fa-at")
                            ]),
                            dcc.Input(type="text", name="email",className="form-control",id="email", placeholder="you@example.com",required="true", autofocus="true")
                        ])
                    ])
                ]),
                html.Div(className="col-md-3", children=[
                    html.Div(className="form-control-feedback", children=[
                        html.Span(className="text-danger align-middle")
                    ])
                ])
            ])
password_row = html.Div(className="row", children=[
                html.Div(className="col-md-3 field-label-responsive", children=[
                    html.Label("Password", htmlFor="password")
                ]),
                html.Div(className="col-md-6", children=[
                    html.Div(className="form-group has-danger", children=[
                        html.Div(className="input-group mb-2 mr-sm-2 mb-sm-0", children=[
                            html.Div(className="input-group-addon", style={"width": "2.6rem"}, children=[
                                html.I(className="fa fa-key")
                            ]),
                            dcc.Input(type="password",name="password",className="form-control",id="password", placeholder="Password",required ="true")
                        ])
                    ])
                ])
            ])

confirm_pwd_row = html.Div(className="row", children=[
                    html.Div(className="col-md-3 field-label-responsive", children=[
                        html.Label("Confirm Password", htmlFor="password")
                    ]),
                    html.Div(className="col-md-6", children=[
                        html.Div(className="form-group", children=[
                            html.Div(className="input-group mb-2 mr-sm-2 mb-sm-0", children=[
                                html.Div(className="input-group-addon", style={"width": "2.6rem"}, children=[
                                    html.I(className="fa fa-repeat")
                                ]),
                                dcc.Input(type="password", name="password-confirmation", className="form-control", id="password-confirm", placeholder="Password", required="true")
                            ])
                        ])
                    ])
            ])

register_button_row = html.Div(className="row", children=[
                html.Div(className="col-md-3"),
                html.Div(className="col-md-6", children=[
                    html.Button(type="submit", id="register-user", className="btn btn-success", children=[
                        "Register", html.I(className="fa fa-user-plus")
                    ])
                ])
            ])

def login_layout():
    logger.debug("login layout")

def register_layout():
    logger.debug("register layout")
    return html.Div(className="container", children=[
        html.Form(className="form-horizontal", role="form", children=[
            register_title_row,
            email_row,
            password_row,
            confirm_pwd_row,
            register_button_row
        ])
    ])

