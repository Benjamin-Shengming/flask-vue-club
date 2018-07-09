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

def generate_service_card(service_id):
  major_img_link = filestore.get_service_img_link(service_id, MAJOR_IMG)
  print(major_img_link)
  service = app_controller.get_club_service(CLUB_NAME, service_id)
  ref_link = "/service/edit/{}".format(service.id)
  return dcc.Link(href=ref_link, children=[
    html.Div(className="card", style={"cursor":"pointer"}, children=[
        html.Img(className="card-img-top",
                 src=major_img_link,
                 alt="service major image"),
        html.Div(className="card-body", children=[
            html.H5(service.name, className="card-title"),
            html.P(service.description, className="card-text")
        ]),
        html.Hr()
     ])
  ])

def layout():
    all_services = app_controller.get_club_service_list(CLUB_NAME)
    services_data = [item.to_dict() for item in all_services]
    return html.Div([
        html.H4('All services'),
        dt.DataTable(
            rows= services_data if services_data else [{"No service":"No Service"}],

            # optional - sets the order of columns
            #columns=sorted(DF_GAPMINDER.columns),

            row_selectable=True,
            filterable=True,
            sortable=True,
            editable=False,
            selected_row_indices=[],
            id='datatable-gapminder'
        ),
        html.Hr(),
        html.Div("click one service to edit"),
        html.Div(id="service_list_service_cards"),
        html.Hr()
    ])


@app.callback(
    Output('service_list_service_cards', 'children'),
    [Input('datatable-gapminder', 'rows'),
     Input('datatable-gapminder', 'selected_row_indices')])
def update_service_cards(rows, selected_row_indices):
    all_cards = []
    for i in selected_row_indices:
        print(rows[i]["id"])
        all_cards.append(generate_service_card(rows[i]["id"]))
    return all_cards

if __name__ == '__main__':
    app.run_server(debug=True)
