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
    user_data = [item.to_dict() for item in all_clients]
    return html.Div([
        html.H4(_("All registered users")),
        dt.DataTable(
            rows=user_data,

            # optional - sets the order of columns
            #columns=sorted(DF_GAPMINDER.columns),

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


@app.callback(
    Output('client_list_details', 'children'),
    [Input('datatable-client-list', 'rows'),
     Input('datatable-client-list', 'selected_row_indices')])
def update_service_cards(rows, selected_row_indices):
    all_cards = []
    for i in selected_row_indices:
        print(rows[i]["id"])
        all_cards.append(generate_client_card(rows[i]["id"]))
    return all_cards

if __name__ == '__main__':
    app.run_server(debug=True)
