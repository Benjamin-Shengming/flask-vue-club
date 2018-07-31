#!/usr/bin/python3
import dash_core_components as dcc
import dash_html_components as html
from dash.exceptions import PreventUpdate
from dash.dependencies import State, Input, Output
from app import app
from app import app_controller
from sd_material_ui import Snackbar
from autolink import Redirect
from localstorage_writer import LocalStorageWriter
from localstorage_reader import LocalStorageReader
import gettext
import coloredlogs
import logging
from utils import g_id
from magic_defines import (locale_d, EMAIL, LOGIN,
                           PASSWD, SNACK_BAR, HIDDEN_DIV,
                           STORAGE_R, STORAGE_W,
                           S_INPUT_PWD, S_INPUT_EMAIL, REDIRECT,
                           S_USER_NOT_EXIST, CLUB_NAME,
                           USER_STORAGE, MOBILE_EMAIL
                           )


logger = logging.getLogger(__name__)
coloredlogs.install(level='DEBUG', logger=logger)

zh = gettext.translation("user_login", locale_d(), languages=["zh_CN"])
zh.install(True)
_ = zh.gettext


def gen_id(name):
    # user module as name prefix
    s_id = g_id(__name__, name)
    return s_id


login_title_row = html.Div(className="row", children=[
    html.Div(className="col-md-3"),
    html.Div(className="col-md-6", children=[
        html.H2(_("User Login")),
        html.Hr()
    ])
])
tel_email_row = html.Div(className="row", children=[
    html.Div(className="col-md-3 field-label-responsive", children=[
        html.Label(_("Mobile or E-Mail Address"), htmlFor="tel_email")
    ]),
    html.Div(className="col-md-6", children=[
        html.Div(className="form-group", children=[
            html.Div(className="input-group mb-2 mr-sm-2 mb-sm-0", children=[
                html.Div(className="input-group-addon", style={"width": "2.6rem"}, children=[
                    html.I(className="fa fa-at")
                ]),
                dcc.Input(type="text",
                          name="tel_email",
                          className="form-control",
                          id=gen_id(MOBILE_EMAIL),
                          placeholder=_("mobile or email"),
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
                          required="true")
            ])
        ])
    ])
])


login_button = html.Button(type="submit",
                           id=gen_id(LOGIN),
                           className="btn btn-success",
                           children=[
                                _("Login"),
                                html.I(className="fa fa-user-plus")
                           ])

login_button_row = html.Div(className="row",
                            children=[
                                html.Div(className="col-md-3"),
                                html.Div(className="col-md-3", children=[
                                    login_button,
                                ]),
])
err_msg_row = Snackbar(id=gen_id(SNACK_BAR), open=False, message=_("fill login information"))
user_storage_w = LocalStorageWriter(id=gen_id(STORAGE_W), label=USER_STORAGE)
auto_redirect = Redirect(id=gen_id(REDIRECT))

user_storage_r = LocalStorageReader(id=gen_id(STORAGE_R), label=USER_STORAGE)


def layout():
    logger.debug("login layout")
    return html.Div(className="container", children=[
        login_title_row,
        tel_email_row,
        password_row,
        login_button_row,
        html.Div(id=gen_id(HIDDEN_DIV)),
        err_msg_row,
        auto_redirect,
        user_storage_w,
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
              [State(gen_id(MOBILE_EMAIL), "value"),
               State(gen_id(PASSWD), "value")])
def change_message(n_clicks, mobile_email, pwd):
    logger.debug("change message")
    if not mobile_email:
        logger.debug("input email is {}".format(mobile_email))
        return S_INPUT_MOBILE_EMAIL
    if not pwd:
        return S_INPUT_PWD

    user = app_controller.get_club_user_by_tel_or_email(CLUB_NAME, mobile_email)
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
    logger.debug("store jwt " + jwt)
    return jwt


@app.callback(Output(gen_id(REDIRECT), 'href'),
              [Input(gen_id(STORAGE_R), "value")])
def redirect(jwt):
    if not jwt:
        raise PreventUpdate()

    user = app_controller.get_club_user_by_jwt(CLUB_NAME, jwt)
    if not user:
        raise PreventUpdate()

    return "/user/profile"
