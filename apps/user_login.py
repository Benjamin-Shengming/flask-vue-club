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
import sd_material_ui
from sd_material_ui import Snackbar
import coloredlogs, logging
from utils import *
from autolink import Redirect
from localstorage_writer import LocalStorageWriter
from localstorage_reader import LocalStorageReader

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


login_button  = html.Button(type="submit",
                            id="user_login_button_login",
                            className="btn btn-success",
                            children=[
                                "Login",
                                html.I(className="fa fa-user-plus")
                             ])

login_button_row = html.Div(id="user_login_button_row",
                            className="row",
                            children= [
                                html.Div(className="col-md-3"),
                                html.Div(className="col-md-3", children=[
                                    login_button,
                                ]),
                            ])
err_msg_row = Snackbar(id='user_login_snackbar', open=True, message='Polo', action='Reveal')
user_storage = LocalStorageWriter(id="user_login_user_storage", label=USER_STORAGE)
auto_redirect = Redirect(href="/home")
def layout():
    logger.debug("login layout")
    return html.Div(className="container", children=[
        email_row,
        password_row,
        login_button_row,
        html.Div(id="user_login_button_target")
    ])



@app.callback(Output('user_login_snackbar', 'message'),
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


@app.callback(Output('user_login_button_target', 'children'),
              [Input("user_login_button_login", "n_clicks")],
              [State("user_login_email", "value"),
               State("user_login_password", "value")])
def store_user_info(n_clicks, email, password):
    assert_button_clicks(n_clicks)
    print("store user info called")
    user_data = {
        'email': email,
        'tel':None,
        'password': password,
    }
    user = app_controller.verify_club_user(CLUB_NAME, user_data)
    if not user:
        return [err_msg_row]
    jwt = app_controller.generate_user_jwt(CLUB_NAME, user)
    return [
            user_storage,
            err_msg_row,
            #auto_redirect
            ]

