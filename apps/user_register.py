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
from autolink import Redirect

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
                            dcc.Input(type="text", name="email",className="form-control",id="register-email", placeholder="you@example.com",required="true", autofocus="true")
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
                            dcc.Input(type="password",name="password",className="form-control",id="register-password", placeholder="Password",required ="true")
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
                                dcc.Input(type="password", name="password-confirmation", className="form-control", id="register-password-confirm", placeholder="Password", required="true")
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

auto_link = Redirect(id="user_register_autolink_home", href="")

def register_layout():
    logger.debug("register layout")
    return html.Div(className="container", children=[
            register_title_row,
            email_row,
            password_row,
            confirm_pwd_row,
            register_button_row,
            auto_link
    ])

@app.callback(Output('global-hiden-user-info', 'children'),
              [Input("register-user", "n_clicks")],
              [State("register-email", "value")])
def register_user(n_clicks, email):
    if n_clicks <= 0:
        raise ValueError("Do nothing")
    return email

@app.callback(Output('user_register_autolink_home', 'href'),
              [Input("register-user", "n_clicks")],
              [State("register-email", "value"),
               State("register-password", "value"),
               State("register-password-confirm", "value")])
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
    user = app_controller.create_club_user(CLUB_NAME, user_data)
    if user.tel:
        raise PreventUpdate()
    if user.email:
        #app_controller.resend_active_code_by_email(CLUB_NAME, user.email)
        pass
    return "/user/activate/{}".format(user.id)
