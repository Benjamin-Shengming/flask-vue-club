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


def gen_id(name):
    # user module as name prefix
    s_id = g_id(__name__, name)
    logger.debug(s_id)
    return s_id

login_title_row = html.Div(className="row", children=[
                html.Div(className="col-md-3"),
                html.Div(className="col-md-6", children=[
                    html.H2("User Login"),
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
                                      id=gen_id(EMAIL),
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
                                      id=gen_id(PASSWD),
                                      placeholder="Password",
                                      required ="true")
                        ])
                    ])
                ])
            ])


login_button  = html.Button(type="submit",
                            id=gen_id(LOGIN),
                            className="btn btn-success",
                            children=[
                                "Login",
                                html.I(className="fa fa-user-plus")
                             ])

login_button_row = html.Div(id=gen_id(LOGIN),
                            className="row",
                            children= [
                                html.Div(className="col-md-3"),
                                html.Div(className="col-md-3", children=[
                                    login_button,
                                ]),
                            ])
err_msg_row = Snackbar(id=gen_id(SNACK_BAR), open=False, message='fill login information')
user_storage_w = LocalStorageWriter(id=gen_id(STORAGE_W), label=USER_STORAGE)
auto_redirect = Redirect(id=gen_id(REDIRECT))

timer = dcc.Interval(
            id=gen_id(TIMER),
            interval=1*1000, # in milliseconds
            n_intervals=0)
user_storage_r = LocalStorageReader(id=gen_id(STORAGE_R), label=USER_STORAGE)

def layout():
    logger.debug("login layout")
    return html.Div(className="container", children=[
        login_title_row,
        email_row,
        password_row,
        login_button_row,
        html.Div(id=gen_id(HIDDEN_DIV)),
        err_msg_row,
        auto_redirect,
        user_storage_w,
        timer,
        user_storage_r
    ])



# callbacks
@app.callback(Output(gen_id(SNACK_BAR), 'open'),
              [Input(gen_id(SNACK_BAR), "message")])
def show_snackbar(msg):
    if msg:
        logger.debug("show snackbar")
        return True
    else:
        logger.debug("hide snackbar")
        return False


@app.callback(Output(gen_id(SNACK_BAR), 'message'),
              [Input(gen_id(LOGIN), "n_clicks")],
              [State(gen_id(EMAIL), "value"),
               State(gen_id(PASSWD), "value")])
def change_message(n_clicks, email, pwd):
    logger.debug("change message")
    if not email:
        logger.debug(S_INPUT_EMAIL)
        return S_INPUT_EMAIL
    if not pwd:
        return S_INPUT_PWD

    user = app_controller.get_club_user_by_email(CLUB_NAME, email)
    if not user:
        return S_USER_NOT_EXIST
    if not pwd:
        logger.debug(S_INPUT_PWD)
        return S_INPUT_PWD
    return ""



@app.callback(Output(gen_id(STORAGE_W), 'value'),
              [Input(gen_id(SNACK_BAR), "message")],
              [State(gen_id(EMAIL), "value"),
               State(gen_id(PASSWD), "value")])
def store_user_info(msg, email, password):
    logger.debug("store user info")
    if msg:
        raise PreventUpdate()

    user = app_controller.get_club_user_by_email(CLUB_NAME, email)
    if not user:
        raise PreventUpdate()

    jwt = app_controller.generate_user_jwt(CLUB_NAME, user)
    return jwt


@app.callback(Output(gen_id(REDIRECT), 'href'),
              [Input(gen_id(TIMER), "n_intervals")],
              [State(gen_id(STORAGE_R), "value")])
def redirect(interval, jwt):
    if not jwt:
        raise PreventUpdate()

    user = app_controller.get_club_user_by_jwt(CLUB_NAME, jwt)
    if not user:
        raise PreventUpdate()

    if user.is_active():
        return "/home"
    else:
        return "/user/profile"
