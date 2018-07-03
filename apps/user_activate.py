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


def generate_title(user_id):
    activate_title_row = html.Div(className="row", children=[
                    html.Div(className="col-md-3"),
                    html.Div(className="col-md-6", children=[
                        html.H2("Activate User"),
                        html.Hr(),
                        html.Div(str(user_id), id="activate-user-id", style={"display":"none"})

                    ])
                ])
activate_code_row = html.Div(className="row", children=[
                html.Div(className="col-md-3 field-label-responsive", children=[
                    html.Label("Activate Code", htmlFor="activate-code")
                ]),
                html.Div(className="col-md-6", children=[
                    html.Div(className="form-group", children=[
                        html.Div(className="input-group mb-2 mr-sm-2 mb-sm-0", children=[
                            html.Div(className="input-group-addon", style={"width": "2.6rem"}, children=[
                                html.I(className="fa fa-key")
                            ]),
                            dcc.Input(type="text",
                                      className="form-control",
                                      id="activate-code",
                                      placeholder="98245",
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

activate_button_row = html.Div(className="row", children=[
                html.Div(className="col-md-3"),
                html.Div(className="col-md-6", children=[
                    html.Button(type="submit", id="activate-user", className="btn btn-success", children=[
                        "Activate", html.I(className="fa fa-user-plus")
                    ])
                ])
            ])


def layout(user_id):
    logger.debug("activate layout")
    return html.Div(className="container", children=[
            generate_title(user_id),
            activate_code_row,
            activate_button_row,
            dcc.Location(id="to-service-list", pathname="")
        #])
    ])


@app.callback(Output('to-service-list', 'pathname'),
              [Input("activate-user", "n_clicks")],
              [State("activate-code", "value"),
               State("activate-user-id", "children"),
               State("global-hiden-user-info", "children")])
def activate_user(n_clicks, code , user_id, email):
    if n_clicks <= 0:
        raise ValueError("Do nothing")

    user = app_controller.activate_club_user_by_email(CLUB_NAME, email, code)
    if user:
        return "/service/list"
