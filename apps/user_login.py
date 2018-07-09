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
from flask import redirect

import coloredlogs, logging
logger = logging.getLogger(__name__)
coloredlogs.install(level='DEBUG', logger=logger)


#register_storage = local_storage.LocalStorageComponent(id="global-local-storage", label="user_info")
login_title_row = html.Div(className="row", children=[
                html.Div(className="col-md-3"),
                html.Div(className="col-md-6", children=[
                    html.H2("Login"),
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
                            dcc.Input(type="text",
                                      name="email",
                                      className="form-control",
                                      id="user_login_email",
                                      placeholder="you@example.com",
                                      required="true",
                                      autofocus="true")
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
                            dcc.Input(type="password",
                                      name="password",
                                      className="form-control",
                                      id="user_login_password",
                                      placeholder="Password",
                                      required ="true")
                        ])
                    ])
                ])
            ])


back_button  = html.Button(type="submit",
                            id="user_login_button_home",
                            className="btn btn-success",
                            children=[
                                "Home",
                                html.I(className="fa fa-user-plus")
                             ])
back_home_link =  dcc.Link( href="/home",
                           children=[back_button]
                           )

back_button_row = html.Div(id="user_login_button_row",
                            className="row",
                            children= [
                                html.Div(className="col-md-3"),
                                html.Div(className="col-md-3", children=[
                                    back_home_link,
                                ]),
                            ])

err_msg_row= html.Div(className="row", children=[
                html.Div(className="col-md-3"),
                html.Div(id = "user_login_err_msg", className="col-md-6", children=[])
            ])


def layout():
    logger.debug("login layout")
    return html.Div(className="container", children=[
            local_storage.LocalStorageComponent(id="user_login_storage", label=USER_STORAGE),
            email_row,
            password_row,
            err_msg_row,
            back_button_row,

    ])

@app.callback(Output('user_login_err_msg', 'children'),
              [Input("user_login_email", "value"),
               Input("user_login_password", "value")])
def check_user(email, password):
    if not email:
        return "Pleaes input email"
    if not password:
        return "Please input password"

    user_data = {
        'email': email,
        'tel':None,
        'password': password,
    }
    if not app_controller.verify_club_user(CLUB_NAME, user_data):
        return "You email, tel or password does not match"

    return "You have logged in"

@app.callback(Output('user_login_redirect_link', 'children'),
              [Input("user_login_email", "value"),
               Input("user_login_password", "value")])
def check_user(email, password):
    user_data = {
        'email': email,
        'tel':None,
        'password': password,
    }
    if not app_controller.verify_club_user(CLUB_NAME, user_data):
        return "back to Home (not login)"
    return "Back to Home (login)"

@app.callback(Output('user_login_storage', 'value'),
              [Input("user_login_email", "value"),
               Input("user_login_password", "value")])
def store_user_info(email, password):
    print("store user info called")
    user_data = {
        'email': email,
        'tel':None,
        'password': password,
    }
    user = app_controller.verify_club_user(CLUB_NAME, user_data)
    if not user:
        return ""
    jwt = app_controller.generate_user_jwt(CLUB_NAME, user)
    return jwt

