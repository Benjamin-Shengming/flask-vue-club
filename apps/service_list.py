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



import coloredlogs, logging
logger = logging.getLogger(__name__)
coloredlogs.install(level="DEBUG", logger=logger)

import gettext
zh = gettext.translation("service_list", locale_d(), languages=["zh_CN"])
zh.install(True)
_ = zh.gettext

def filter_and_map_dict(d):
    #change column name
    map_d = {
        "id": "ID",
        "name": _("name"),
        "price": _("service_price"),
        "discount": _("service_discount"),
        "user_view": _("user_view")
    }
    new_d = {}
    for k, v in d.items():
        if k in map_d.keys():
            new_key = map_d[k]
            new_d[new_key] = v
    return new_d

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
    logger.debug(all_services)
    s_data = [item.to_dict() for item in all_services]
    services_data = [filter_and_map_dict(item) for item in s_data]
    if services_data:
        return html.Div([
            html.H4(_('All services')),
            dt.DataTable(
                rows= services_data,
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
            html.Div(_("click one service to edit")),
            html.Div(id="service_list_service_cards"),
            html.Hr()
        ])
    else:
        return html.Div([
            html.H4(_('No services')),
        ])


@app.callback(
    Output('service_list_service_cards', 'children'),
    [Input('datatable-gapminder', 'rows'),
     Input('datatable-gapminder', 'selected_row_indices')])
def update_service_cards(rows, selected_row_indices):
    all_cards = []
    for i in selected_row_indices:
        print(rows[i]["ID"])
        all_cards.append(generate_service_card(rows[i]["ID"]))
    return all_cards

