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
import sd_material_ui
from sd_material_ui import Snackbar
import coloredlogs, logging
from sd_material_ui import Snackbar
from magic_defines import *
from utils import *
from autolink import Redirect
from localstorage_writer import LocalStorageWriter
from localstorage_reader import LocalStorageReader

import coloredlogs, logging
logger = logging.getLogger(__name__)
coloredlogs.install(level='DEBUG', logger=logger)



import gettext
zh = gettext.translation("user_profile", locale_d(), languages=["zh_CN"])
zh.install(True)
_ = zh.gettext

def gen_id(name):
    # user module as name prefix
    s_id = g_id(__name__, name)
    return s_id

def generate_field_user_id(user):
    field_row = html.Div(className="form-group row", children=[
        html.Label(S_USER_ID, className="col-lg-3 col-form-label form-control-label"),
        html.Div(className="col-lg-9", children=[
            dcc.Input(id=gen_id(USER_ID),
                        className="form-control",
                        type="text",
                        value=user.id,
                        disabled=True)
        ])
    ])
    return field_row

def generate_field_user_email(user):
    field_row = html.Div(className="form-group row", children=[
        html.Label(S_EMAIL, className="col-lg-3 col-form-label form-control-label"),
        html.Div(className="col-lg-9", children=[
            dcc.Input(id=gen_id(EMAIL),
                        className="form-control",
                        type="text",
                        value=user.email,
                        disabled=True),
            html.Button(S_EDIT,
                        id=gen_id(EDIT + EMAIL),
                        className="btn btn-outline-info"),
            html.Span(" "),
            html.Button(S_CONFIRM,
                        id=gen_id(CONFIRM + EMAIL),
                        className="btn btn-outline-primary"),

        ])
    ])
    return field_row

def generate_field_user_tel(user):
    field_row = html.Div(className="form-group row", children=[
        html.Label(S_TEL, className="col-lg-3 col-form-label form-control-label"),
        html.Div(className="col-lg-9", children=[
            dcc.Input(id=gen_id(TEL),
                        className="form-control",
                        type="text",
                        value=user.tel,
                        disabled=True),
            html.Button(S_EDIT,
                        id=gen_id(EDIT + TEL),
                        className="btn btn-outline-info"),
            html.Span(" "),
            html.Button(S_CONFIRM,
                        id=gen_id(CONFIRM + TEL),
                        className="btn btn-outline-primary"),

        ])
    ])
    return field_row


def generate_field_user_pwd(user):
    field_row = html.Div(className="form-group row", children=[
        html.Label(S_PWD, className="col-lg-3 col-form-label form-control-label"),
        html.Div(className="col-lg-9", children=[
            dcc.Input(id=gen_id(PASSWD),
                        className="form-control",
                        type="password",
                        value=user.password_hash,
                        disabled=True)
        ])
    ])
    return field_row

def generate_field_user_pwd_confirm(user):
    field_row = html.Div(className="form-group row", children=[
        html.Label(S_PWD_CONFIRM, className="col-lg-3 col-form-label form-control-label"),
        html.Div(className="col-lg-9", children=[
            dcc.Input(id=gen_id(PASSWD_CONFIRM),
                        className="form-control",
                        type="password",
                        value=user.password_hash,
                        disabled=True),
            html.Button(S_EDIT,
                        id=gen_id(EDIT + PASSWD),
                        className="btn btn-outline-info"),
            html.Span(" "),
            html.Button(S_CONFIRM,
                        id=gen_id(CONFIRM + PASSWD),
                        className="btn btn-outline-primary"),
        ])
    ])
    return field_row

def generate_field_user_activate_status(user):
    field_row = html.Div(className="form-group row", children=[
        html.Label(S_ACTIVE_STATUS, className="col-lg-3 col-form-label form-control-label"),
        html.Div(className="col-lg-9", children=[
            dcc.Input(id=gen_id(STATUS + ACTIVATE),
                        className="form-control",
                        type="text",
                        disabled=True,
                        value= S_ACTIVE_YES if user.is_active() else S_ACTIVE_NO)
        ])
    ])
    return field_row

def generate_field_user_activate(user):
    field_row = html.Div(className="form-group row", children=[
        html.Label(S_ACTIVATE, className="col-lg-3 col-form-label form-control-label"),
        html.Div(className="col-lg-9", children=[
            dcc.Input(id=gen_id(ACTIVATE),
                        className="form-control",
                        type="text",
                        placeholder=S_INPUT_ACTIVATE_CODE),
            html.Button(S_ACTIVATE,
                        id=gen_id(CONFIRM+ACTIVATE),
                        className="btn btn-outline-info"),
            html.Button(S_LOGOUT,
                        id=gen_id(LOGOUT),
                        className="btn btn-outline-info")
        ])
    ])
    return field_row


def generate_user_fields(user):
    list_fields = []
    list_fields.append(generate_field_user_id(user))
    list_fields.append(generate_field_user_email(user))
    list_fields.append(generate_field_user_tel(user))
    list_fields.append(generate_field_user_pwd(user))
    list_fields.append(generate_field_user_pwd_confirm(user))
    list_fields.append(generate_field_user_activate_status(user))
    list_fields.append(generate_field_user_activate(user))
    return html.Div(className="tab-pane", children= list_fields)

user_info_reader = LocalStorageReader(id=gen_id(STORAGE_R),
                                      label=USER_STORAGE)

user_info_writer= LocalStorageWriter(id=gen_id(STORAGE_W),
                                      label=USER_STORAGE)

auto_link = Redirect(id=gen_id(REDIRECT), href="")

login_firstly = dcc.Link(href="/user/login",
                    className="col btn btn-warning float-left ", children=[
                    html.I(className="fa fa-angle-left"),
                    _("Please login firstly!")
                ])

def layout(jwt):
    if not jwt:
        return login_firstly
    user = app_controller.get_club_user_by_jwt(CLUB_NAME, jwt)
    if not user:
        return login_firstly

    return html.Div(id=gen_id(ROOT), children=[
        user_info_reader,
        user_info_writer,
        auto_link,
        html.Div(id=gen_id(PLACEHOLDER), children=[
            generate_user_fields(user)
        ])
    ])


@app.callback(Output(gen_id(PLACEHOLDER), 'children'),
              [Input(gen_id(CONFIRM+ACTIVATE), "n_clicks")],
              [State(gen_id(ACTIVATE), "value"),
              State(gen_id(STORAGE_R), "value")])
def activate(n_clicks, code, jwt):
    logger.debug(n_clicks)
    logger.debug(code)
    logger.debug(jwt)
    assert_button_clicks(n_clicks)
    assert_has_value(code)
    assert_has_value(jwt)
    user = app_controller.get_club_user_by_jwt(CLUB_NAME, jwt)
    if user.is_active():
        raise PreventUpdate()
    user.activate(code)
    app_controller.save(user)
    return generate_user_fields(user)

@app.callback(Output(gen_id(REDIRECT), 'href'),
              [Input(gen_id(STORAGE_R), "value")])
def redirect(jwt):
    logger.debug("redirect ")
    logger.debug(str(jwt))
    user = app_controller.get_club_user_by_jwt(CLUB_NAME, jwt)
    if user:
        raise PreventUpdate()

    return "/home"

@app.callback(Output(gen_id(STORAGE_W), 'value'),
              [Input(gen_id(LOGOUT), "n_clicks")])
def activate(n_clicks):
    assert_button_clicks(n_clicks)
    return ""


