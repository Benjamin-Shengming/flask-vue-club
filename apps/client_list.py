import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_table_experiments as dt
import json
import pandas as pd
import numpy as np
import plotly
import filestore
from flask import redirect
from app import app
from app import app_controller
from magic_defines import *


import gettext
zh = gettext.translation("client_list", locale_d(), languages=["zh_CN"])
zh.install(True)
_ = zh.gettext

import coloredlogs, logging
logger = logging.getLogger(__name__)
coloredlogs.install(level="DEBUG", logger=logger)

def filter_and_map_dict(d):
    #change column name
    map_d = {
        "id": "ID",
        "email": _("email"),
        "email_confirm": _("email_confirm"),
        "tel": _("tel"),
        "tel_confirmed": _("tel_confirmed"),
        "activate_code": _("activate_code"),
        "last_active_time": _("last_active_time")
    }
    new_d = {}
    for k, v in d.items():
        if k in map_d.keys():
            new_key = map_d[k]
            new_d[new_key] = v
    return new_d

def generate_client_card(user_id):
  user = app_controller.get_club_user_by_id(CLUB_NAME, user_id)
  return html.Div(className="card", children=[
        html.Div(str(user.id), className="card-header"),
        html.Div(className="card-body", children=[
            html.Div(_("Email:") + str(user.email) if user.email else _("Email:")),
            html.Div(_("Tel:") + str(user.tel) if user.tel else _("Tel")),
            html.Div(_("Activate code:") + str(user.activate_code) if user.activate_code else _("Activate Code")),
        ]),
        html.Hr()
     ])

def layout():
    all_clients = app_controller.get_club_user_list(CLUB_NAME)
    logger.debug(all_clients)
    users = [item.to_dict() for item in all_clients]
    user_data = [filter_and_map_dict(item) for item in users]
    if user_data:
        return html.Div([
            html.H4(_("All registered users")),
            dt.DataTable(
                rows=user_data ,
                row_selectable=True,
                filterable=True,
                sortable=True,
                editable=False,
                selected_row_indices=[],
                id='datatable-client-list'
            ),
            html.Hr(),
            html.Div(_("choose users to view details")),
            html.Div(id="client_list_details"),
            html.Hr()
        ])
    else:
        return html.Div([
            html.H4(_("No registered users")),
        ])

@app.callback(
    Output('client_list_details', 'children'),
    [Input('datatable-client-list', 'rows'),
     Input('datatable-client-list', 'selected_row_indices')])
def update_service_cards(rows, selected_row_indices):
    all_cards = []
    for i in selected_row_indices:
        print(rows[i]["ID"])
        all_cards.append(generate_client_card(rows[i]["ID"]))
    return all_cards

if __name__ == '__main__':
    app.run_server(debug=True)
