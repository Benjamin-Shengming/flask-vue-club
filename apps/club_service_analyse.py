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
from pyorbital.orbital import Orbital
import plotly.plotly as py
import plotly.graph_objs as go
import numpy as np

logger = logging.getLogger(__name__)
coloredlogs.install(level='DEBUG', logger=logger)

def gen_id(name):
    # user module as name prefix
    s_id = g_id(__name__, name)
    return s_id

def get_order_detail_quantity_and_value():
    all_orders = app_controller.get_club_order_list(CLUB_NAME)
    all_order_detail = []
    for order in all_orders:
        all_order_detail.extend(order.details)
    pie_dict = {}
    labels = []
    quantity_values = []
    price_values = []
    for s in all_order_detail:
       quantity =  s.quantity
       price = s.calc_price()
       name = s.name
       if (name) not in pie_dict.keys():
           pie_dict[name] = [quantity, price]

       else:
           pie_dict[name][0] += pie_dict[name][0] + quantity
           pie_dict[name][1] += pie_dict[name][1] + price

    for k, v in pie_dict.items():
        labels.append(k)
        quantity_values.append(v[0])
        price_values.append(v[1])
    return labels, quantity_values, price_values


def generate_layout():
    labels, quantities, values = get_order_detail_quantity_and_value()
    data_quantity = [
        {
            'labels':labels,
            'values': quantities,
            'type': 'pie',
        },
    ]

    data_value = [{
        'labels':labels,
        'values': values,
        'type': 'pie',
        }]

    return html.Div([
        html.Div("service quantity percentage"),
        dcc.Graph(id=gen_id("quantity-pie"),
                  figure={
                    'data': data_quantity,
                    'layout': {
                        'margin': {
                            'l': 30,
                            'r': 0,
                            'b': 30,
                            't': 0
                        }
                    },
                      'textfont':dict(size=20),
                  }),
        html.Hr(),
        html.Div("service value percentage"),
        dcc.Graph(id=gen_id("money-pie"),
                  figure={
                    'data': data_value,
                    'layout': {
                        'margin': {
                            'l': 30,
                            'r': 0,
                            'b': 30,
                            't': 0
                        }
                    }
                    }
                  )
    ])

def layout():
    return generate_layout()



