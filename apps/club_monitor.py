#!/usr/bin/python3
from collections import OrderedDict
from uuid import uuid1
import dash
import json
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Event, State, Input, Output
from pprint import pprint
from app import app
from app import app_controller
import filestore
from utils import *
from dash.exceptions import PreventUpdate
from magic_defines import *
import json
from localstorage_writer import LocalStorageWriter
from localstorage_reader import LocalStorageReader
from autolink import Redirect
import dash_table_experiments as dt
import coloredlogs, logging
import datetime
import plotly
import plotly.plotly as py
import plotly.graph_objs as go
import numpy as np

logger = logging.getLogger(__name__)
coloredlogs.install(level='DEBUG', logger=logger)

import gettext
zh = gettext.translation("club_monitor", locale_d(), languages=["zh_CN"])
zh.install(True)
_ = zh.gettext

def gen_id(name):
    # user module as name prefix
    s_id = g_id(__name__, name)
    return s_id

def generate_x_axis_24_hours():
    axis = ["{:02d}".format(item) for item in range(0, 24)]
    logger.debug(axis)
    return axis
hour_x_axis = generate_x_axis_24_hours()

def get_today_24_hour_hit():
    c_time = local_time_day()
    logger.debug(c_time)
    all_histories = app_controller.get_remote_ip_activity()
    today_hits = [item for item in all_histories if item.local_time() >= c_time]
    hour_list = []
    for hour in range(0, 24):
       hour_hits = len([item for item in today_hits if item.local_time().hour == hour])
       hour_list.append(hour_hits)
    #logger.debug(hour_list)
    return hour_list

def generate_layout():
    return html.Div([
        html.Div(id=gen_id("34 hours activity")),
        dcc.Graph(id=gen_id("24hours-activity")),
        dcc.Graph(id=gen_id("popular-service")),
        dcc.Interval(
            id='interval-component',
            interval=1*1000, # in milliseconds
            n_intervals=0
        )
    ])

def layout():
    return generate_layout()


def generate_x_axis_24_hours():
    axis = ["{:02d}".format(item) for item in range(0, 24)]
    logger.debug(axis)
    return axis

def get_today_24_hour_hit():
    c_time = local_time_day()
    logger.debug(c_time)
    all_histories = app_controller.get_remote_ip_activity()
    today_hits = [item for item in all_histories if item.local_time() >= c_time]
    hour_list = []
    for hour in range(0, 24):
       hour_hits = len([item for item in today_hits if item.local_time().hour == hour])
       hour_list.append(hour_hits)
    #logger.debug(hour_list)
    return hour_list

def get_top_10_service_by_view():
    all_service = app_controller.get_club_service_list(CLUB_NAME)
    top = sorted(all_service, key=lambda s:s.user_view, reverse=True)
    if len(top) > 10:
        return top[:10]
    else:
        return top



# Multiple components can update everytime interval gets fired.
@app.callback(Output(gen_id("24hours-activity"), 'figure'),
              [Input('interval-component', 'n_intervals')])
def update_activity_graph(n):
    trace = go.Bar(
        x= generate_x_axis_24_hours(),
        y= get_today_24_hour_hit(),
        name="Hourly activity",
    )

    layout = go.Layout(
        title = _("Hourly user activity"),
        xaxis = dict(
                    title=_("HOUR"),
                    tickangle=-45,
                    ticks='outside',
                    tick0=0,
                    dtick=2,
                    tickfont=dict(
                        size=7
                    )
                ),
        yaxis = dict(
                     title=_("ACTIVITY"),
                     ticks='outside',
                     tick0=0,
                     rangemode='nonnegative'
                     )
    )
    return go.Figure(data=[trace], layout=layout)



# Multiple components can update everytime interval gets fired.
@app.callback(Output(gen_id("popular-service"), 'figure'),
              [Input('interval-component', 'n_intervals')])
def update_popular_graph(n):
    top_10  = get_top_10_service_by_view()
    x_data = []
    y_data = []
    for s in top_10:
        x_data.append(s.name)
        y_data.append(s.user_view)
    logger.debug(x_data)
    logger.debug(y_data)
    trace = go.Bar(
        x= x_data,
        y= y_data,
        name=_("Popular service"),
        marker=dict(
            color='orange'
        )
    )

    layout = go.Layout(
        title = _("Popular service"),
        xaxis = dict(
                    title=_("Service"),
                    tickangle=-45,
                    ticks='outside',
                    ),
        yaxis = dict(
                     title=_("Viewed"),
                     ticks='outside',
                     tick0=0,
                     rangemode='nonnegative'
                     )
    )
    return go.Figure(data=[trace], layout=layout)
