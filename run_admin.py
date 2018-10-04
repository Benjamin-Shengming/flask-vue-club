#!/usr/bin/python3
import sys
import os
import flask
import cherrypy
import argparse
import dash
from dash.dependencies import Input, State, Output
import dash_html_components as html
import sd_material_ui
import dash_core_components as dcc
import pandas as pd
import dash_table_experiments as dt
import sd_material_ui
from dash.dependencies import Event, State, Input, Output
from pprint import pprint
from magic_defines import *
import json
import pandas as pd
import numpy as np
import plotly
from sd_material_ui import Snackbar
import dash_table_experiments as dt
# add current folder and lib to syspath
sys.path.append(os.path.join(os.path.dirname(__file__)))
sys.path.append(os.path.join(os.path.dirname(__file__), "libs"))
sys.path.append(os.path.join(os.path.dirname(__file__), "apps"))
from utils import *
from autolink import Redirect
from localstorage_writer import LocalStorageWriter
from localstorage_reader import LocalStorageReader

import coloredlogs, logging
logger = logging.getLogger(__name__)
coloredlogs.install(level="DEBUG", logger=logger)

from app import app
from app import app_controller
from models import init_all
import service_new
import service_list
import service_detail
import client_list
import filestore
import club_monitor
import club_order
import club_service_analyse
import club_user_analyse

import gettext
print(locale_d())
#catalogs = gettext.find("run_user", locale_d(), all=True)
zh = gettext.translation("run_admin", locale_d(), languages=["zh_CN"])
zh.install(True)

def gen_id(name):
    # user module as name prefix
    s_id = g_id(__name__, name)
    return s_id

sider_bar = html.Div(className="col-md-3 float-left col-1 pl-0 pr-0 collapse width show", id="sidebar", children=[
                html.Div(className="list-group border-0 card text-center text-md-left", children=[
                    dcc.Link(href="/home/monitor",
                             className="list-group-item d-inline-block collapsed",
                             style={"cursor": "pointer"},
                             children=[
                                html.I(**{"aria-hidden":"true"},className="fa fa-home"),
                                html.Span(_("Home"), className="d-none d-md-inline")
                    ]),
                    html.A(**{"data-toggle": "collapse", "aria-expanded": "false"}, href="#serviceMenu", className="list-group-item d-inline-block collapsed", children=[
                        html.I(**{"aria-hidden":"true"},className="fab fa-servicestack"),
                        html.Span(_("Service"), className="d-none d-md-inline")
                    ]),
                    html.Div(**{"data-parent":"#sidebar"}, className="collapse", id="serviceMenu", children=[
                        dcc.Link(_("List"), href="/service/list", className="list-group-item", style={"cursor":"pointer"}),
                        dcc.Link(_("New"), href="/service/new", className="list-group-item", style={"cursor":"pointer"}),
                    ]),
                    dcc.Link(href="/client/list", className="list-group-item d-inline-block collapsed", style={"cursor": "pointer"}, children=[
                        html.I(className="fas fa-user"),
                        html.Span(_("Users"), className="d-none d-md-inline")
                    ]),
                    dcc.Link(href="/order/list", className="list-group-item d-inline-block collapsed", style={"cursor": "pointer"}, children=[
                        html.I(className="fas fa-shipping-fast"),
                        html.Span(_("Orders"), className="d-none d-md-inline")
                    ]),
                    html.A(**{"data-toggle":"collapse","aria-expanded":"false"}, href="#menu3", className="list-group-item d-inline-block collapsed", children=[
                        html.I(className="fas fa-chart-pie"),
                        html.Span(_("Analyse & Report"), className="d-none d-md-inline")
                    ]),
                    html.Div(**{"data-parent":"#sidebar"}, className="collapse", id="menu3", children=[
                        dcc.Link(_("Service Analyse"),
                                 href="/service/analyse",
                                 className="list-group-item",
                                 style={"cursor":"pointer"},
                                 refresh=False),
                        dcc.Link(_("User Analyse"), href="/user/analyse", className="list-group-item", style={"cursor":"pointer"})
                    ])
                ])

])

fig = plotly.tools.make_subplots(rows=2, cols=1, vertical_spacing=0.2)
fig["layout"]["margin"] = {
    "l": 30, "r": 10, "b": 30, "t": 10
}
fig["layout"]["legend"] = {"x": 0, "y": 1, "xanchor": "left"}

main_area = html.Main(id="main-area", className="col-md-9 float-left col px-5 pl-md-2 pt-2 main", children=[
                html.A(**{"data-target":"#sidebar", "data-toggle":"collapse"}, href="#",  children=[
                    html.I(className="fa fa-navicon fa-2x py-2 p-1")
                ]),
                html.Div(id="content-container-root", className="page-header", children=[
                    #service_list.layout,
                ]),
                html.Div(id="walk-around", style={"display": "none"}, children=[service_list.layout()])
])

total = html.Div(className="container-fluid", children=[
    html.Div(className="row d-flex d-md-block flex-nowrap wrapper", children=[
        html.Div(style={"display":"none"}, children=[]),
        sider_bar,
        main_area
    ])
])

app.layout = html.Div(children=[
    # walkalround that let client download js bundle, *bugs* in dash
    html.Div(style={"display":"none"}, children=[
        dt.DataTable(
            id='global-datatable-component',
            rows=[{"No": "No"}],
            row_selectable=True,
            filterable=True,
            sortable=True,
            editable=False,
            selected_row_indices=[]
        )
    ]),
    Redirect("click me to redirect", href="", style={"display": "none"}),
    LocalStorageReader(id="user-local-storage-reader", label=USER_STORAGE),
    LocalStorageReader(id="cart-local-storage-reader", label=CART_STORAGE),
    sd_material_ui.Snackbar(id="snackbar", open=False, message="Polo", action="Reveal"),
    LocalStorageWriter(id="global-local-storage-writer", label=USER_STORAGE),
    html.Div(style={"display":"none"}, children=[
    ]),
    total,
    # This Location component represents the URL bar
    dcc.Location(id="url", refresh=False),
])

@app.callback(
    Output("content-container-root", "children"),
    [Input("url", "pathname")])
def display_page(pathname):
    logger.debug(pathname)
    if not pathname:
        pathname = "/"

    p = pathname.lower()
    if p == "/service/new":
        return service_new.layout()
    elif p == "/service/list":
        return service_list.layout()
    elif "/service/edit" in p:
        service_id = p.split("/")[-1]
        layout = service_detail.layout(service_id)
        return layout
    elif "/client/list" in p:
        return client_list.layout()
    elif "/order/list" in p:
        return club_order.layout()
    elif "/service/analyse" in p:
        return club_service_analyse.layout()

    elif "user/analyse" in p:
        return club_user_analyse.layout()

    return club_monitor.layout()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run finishing app")
    parser.add_argument("-i", "--init", help="Init all databasee etc", action="store_true")
    args = parser.parse_args()
    if args.init:
        init_all()
    else:
        for rule in app.server.url_map.iter_rules():
            logger.debug(rule)
        #app.run_server(debug=True, host="0.0.0.0", port=8080)
        cherrypy.tree.graft(app.server.wsgi_app, "/")
        cherrypy.config.update({"server.socket_host": "0.0.0.0",
                                "server.socket_port":8080,
                                "engine.autoreload.on":False})
        try:
            cherrypy.engine.start()
        except KeyboardInterrupt:
            cherrypy.engine.stop()


