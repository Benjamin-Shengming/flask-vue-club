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
from autolink import Redirect
import sd_material_ui
from sd_material_ui import Snackbar
from localstorage_reader import LocalStorageReader
from localstorage_writer import LocalStorageWriter
from utils import *

import coloredlogs, logging
logger = logging.getLogger(__name__)
coloredlogs.install(level='DEBUG', logger=logger)



import gettext
zh = gettext.translation("user_register", locale_d(), languages=["zh_CN"])
zh.install(True)
_ = zh.gettext
def gen_id(name):
    # user module as name prefix
    s_id = g_id(__name__, name)
    return s_id


register_title_row = html.Div(className="row", children=[
                html.Div(className="col-md-3"),
                html.Div(className="col-md-6", children=[
                    html.H2(_("Register New User")),
                    html.Hr()
                ])
            ])
email_row = html.Div(className="row", children=[
                html.Div(className="col-md-3 field-label-responsive", children=[
                    html.Label(_("E-Mail Address"), htmlFor="email")
                ]),
                html.Div(className="col-md-6", children=[
                    html.Div(className="form-group", children=[
                        html.Div(className="input-group mb-2 mr-sm-2 mb-sm-0", children=[
                            html.Div(className="input-group-addon", style={"width": "2.6rem"}, children=[
                                html.I(className="fa fa-at")
                            ]),
                            dcc.Input(type="text", name="email",className="form-control",id=gen_id(EMAIL), placeholder="you@example.com",required="true", autofocus="true")
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
                    html.Label(_("Password"), htmlFor="password")
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
                                      placeholder=_("Password"),
                                      required ="true")
                        ])
                    ])
                ])
            ])

confirm_pwd_row = html.Div(className="row", children=[
                    html.Div(className="col-md-3 field-label-responsive", children=[
                        html.Label(_("Confirm Password"), htmlFor="password")
                    ]),
                    html.Div(className="col-md-6", children=[
                        html.Div(className="form-group", children=[
                            html.Div(className="input-group mb-2 mr-sm-2 mb-sm-0", children=[
                                html.Div(className="input-group-addon", style={"width": "2.6rem"}, children=[
                                    html.I(className="fa fa-repeat")
                                ]),
                                dcc.Input(type="password",
                                          name="password-confirmation",
                                          className="form-control",
                                          id=gen_id(PASSWD_CONFIRM),
                                          placeholder=_("Password"),
                                          required="true")
                            ])
                        ])
                    ])
            ])

register_button_row = html.Div(className="row", children=[
                html.Div(className="col-md-3"),
                html.Div(className="col-md-6", children=[
                    html.Button(type="submit", id=gen_id(REGISTER), className="btn btn-success", children=[
                        _("Register"), html.I(className="fa fa-user-plus")
                    ])
                ])
            ])

auto_link = Redirect(id=gen_id(REDIRECT), href="")

snack_bar_msg =sd_material_ui.Snackbar(id=gen_id(SNACK_BAR), open=True, message='')


def layout():
    logger.debug("register layout")
    return html.Div(className="container", children=[
            register_title_row,
            email_row,
            password_row,
            confirm_pwd_row,
            register_button_row,
            snack_bar_msg,
            auto_link,
            html.Div(id=gen_id(HIDDEN_DIV))
    ])

###
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
              [Input(gen_id(REGISTER), "n_clicks")],
              [State(gen_id(EMAIL), "value"),
               State(gen_id(PASSWD), "value"),
               State(gen_id(PASSWD_CONFIRM), "value")])
def show_message(n_clicks, email, pwd, pwd_confirm):
    logger.debug("change message")
    if not email:
        logger.debug(S_INPUT_EMAIL)
        return S_INPUT_EMAIL
    user = app_controller.get_club_user_by_email(CLUB_NAME, email)
    if user:
        return S_USER_EXIST
    if not pwd:
        logger.debug(S_INPUT_PWD)
        return S_INPUT_PWD
    if not pwd_confirm:
        logger.debug(S_INPUT_PWD_CONFIRM)
        return S_INPUT_PWD_CONFIRM
    if pwd != pwd_confirm:
        logger.debug(S_INPUT_PWD_NOT_MATCH)
        return S_INPUT_PWD_NOT_MATCH
    logger.debug("return nothing")
    return ""

@app.callback(Output(gen_id(REDIRECT), 'href'),
              [Input(gen_id(REGISTER), "n_clicks")],
              [State(gen_id(EMAIL), "value"),
               State(gen_id(PASSWD), "value"),
               State(gen_id(PASSWD_CONFIRM), "value")])
def register_user(n_clicks, email, password, password_confirm):
    if not n_clicks or n_clicks <= 0:
        raise PreventUpdate()
    if password != password_confirm:
        raise PreventUpdate()
    user_data = {
        'email': email,
        'tel':None,
        'password': password,
        'roles': None
    }
    try:
        user = app_controller.create_club_user(CLUB_NAME, user_data)
    except:
        raise PreventUpdate()
    if user.tel:
        raise PreventUpdate()
    if user.email:
        pass
        #app_controller.resend_active_code_by_email(CLUB_NAME, user.email)
    return "/user/login"
