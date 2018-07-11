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


def gen_id(name):
    # user module as name prefix
    s_id = g_id(__name__, name)
    logger.debug(s_id)
    return s_id

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
err_msg_row = Snackbar(id=gen_id(SNACK_BAR), open=True, message='Polo', action='Reveal')
user_storage_w = LocalStorageWriter(id=gen_id(STORAGE_W), label=USER_STORAGE)
user_storage_r = LocalStorageReader(id=gen_id(STORAGE_R), label=USER_STORAGE)
auto_redirect = Redirect(id=gen_id(REDIRECT), href="")

def layout():
    logger.debug("login layout")
    return html.Div(className="container", children=[
        email_row,
        password_row,
        login_button_row,
        html.Div(id=gen_id(HIDDEN_DIV)),
        err_msg_row,
        user_storage_w,
        user_storage_r,
        auto_redirect
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
    user = app_controller.get_club_user_by_email(CLUB_NAME, email)
    if not user:
        return S_USER_NOT_EXIST
    if not pwd:
        logger.debug(S_INPUT_PWD)
        return S_INPUT_PWD
    return ""



@app.callback(Output(gen_id(HIDDEN_DIV), 'children'),
              [Input(gen_id(SNACK_BAR), "message")],
              [State(gen_id(EMAIL), "value"),
               State(gen_id(PASSWD), "value")])
def store_user_info(msg, email, password):
    if msg:
        raise PreventUpdate()

    user = app_controller.get_club_user_by_email(CLUB_NAME, email)
    if not user:
        raise PreventUpdate()

    jwt = app_controller.generate_user_jwt(CLUB_NAME, user)
    return [LocalStorageWriter(id=str(uuid1()), label=USER_STORAGE, value=jwt)]



@app.callback(Output(gen_id(REDIRECT), 'href'),
              [Input(gen_id(HIDDEN_DIV), "children")],
              [State(gen_id(EMAIL), "value"),
               State(gen_id(PASSWD), "value")])
def redirect(loggedin, email, password):
    if not loggedin:
        raise PreventUpdate()

    user = app_controller.get_club_user_by_email(CLUB_NAME, email)
    if not user:
        raise PreventUpdate()

    if user.is_active():
        return "/home"
    else:
        return "/user/profile"
