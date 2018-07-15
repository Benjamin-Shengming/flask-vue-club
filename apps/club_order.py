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
logger = logging.getLogger(__name__)
coloredlogs.install(level='DEBUG', logger=logger)
from dateutil.relativedelta import *

def gen_id(name):
    # user module as name prefix
    s_id = g_id(__name__, name)
    return s_id

def generate_order_data(orders):
    orders_data = [{"id":item.id,
                    "paid": item.paid,
                    "total": item.total_price(),
                    "time":item.time} for item in orders]
    return orders_data

def generate_layout(orders):
    orders_data = generate_order_data(orders)
    return html.Div([
        html.H4('All orders'),
        dcc.Dropdown(
                id=gen_id('all-day-month-year'),
                options=[
                    {'label': 'All', 'value': 'all'},
                    {'label': 'Today', 'value': 'day'},
                    {'label': 'This Month', 'value': 'month'},
                    {'label': 'This year', 'value': 'year'}
                ],
                value='all'
        ),
        dt.DataTable(
            rows= orders_data if orders_data else [{"No order": "No order"}],

            # optional - sets the order of columns
            #columns=sorted(DF_GAPMINDER.columns),
            resizable=True,
            row_selectable=True,
            filterable=True,
            sortable=True,
            editable=False,
            selected_row_indices=[],
            id=gen_id(TABLE)
        ),
        html.Hr(),
        html.Div("click one order to view detail"),
        html.Div(id=gen_id("order-cards")),
        html.Hr()
    ])


def layout():
    club = app_controller.get_club_by_name(CLUB_NAME)

    if not club or not club.orders:
        return html.H1("No orders!")
    return generate_layout(club.orders)

def generate_order_detail(order_detail):
    return  html.Div(className="container-fluid", children = [
        html.Div(className="d-flex",children=[
            html.Div(className="p-2",children =[
                html.Img(src=order_detail.get_img_link(MAJOR_IMG),
                        width="100px",
                        height="100px",
                        alt=order_detail.name,
                        className="img-responsive")
            ]),
            html.Div(className="p-2",children=[
                html.H5(order_detail.name,className="nomargin"),
                html.P(order_detail.description)
            ])
        ]),
        html.Div(className="d-flex justify-content-between",children=[
            html.Div(className="p-2", children=["price: {}*{}={}".format(order_detail.price,
                                                            order_detail.discount_percent_str(),
                                                            order_detail.final_price())
            ]),
            html.Div(className="p-2", children=[
                html.Span("Qty: {}".format(order_detail.quantity))
            ]),
            html.Div(className="p-2",children=[
                html.Div(children=["Subtotal:",order_detail.calc_price()]),
            ])
        ])
    ])

def generate_order(order):
    detail = []
    header = html.Div(className="d-flex justify-content-between",children=[
            html.Div(className="p-2", children=[
                html.Span("order id: {}".format(order.id))
            ]),
            html.Div(className="p-2", children=[
                html.Span("Total: {}".format(order.total_price()))
            ]),
            html.Div(className="p-2", children=[
                html.Span("Paid: {}".format(order.paid))
            ]),
            html.Div(className="p-2",children=[
                html.Div(children=["time:",order.time]),
            ])
        ])
    detail.append(header)
    detail.append(html.Hr())
    for item in order.details:
        detail.append(generate_order_detail(item))
    detail.append(html.Hr())

    user = order.user
    footer = html.Div(className="d-flex justify-content-between",children=[
            html.Div(className="p-2", children=[
                html.Span("user id: {}".format(user.id))
            ]),
            html.Div(className="p-2", children=[
                html.Span("Email: {}".format(user.email))
            ])
        ])
    detail.append(footer)
    return html.Div(children=detail)

def generate_order_card(order_id):
    order = app_controller.get_club_order_by_id(order_id)
    return html.Div(className='container-fluid border border-info', children=[
        generate_order(order)
    ])


@app.callback(
    Output(gen_id("order-cards"), 'children'),
    [Input(gen_id(TABLE), 'rows'),
     Input(gen_id(TABLE), 'selected_row_indices')])
def update_order_cards(rows, selected_row_indices):
    all_cards = []
    for i in selected_row_indices:
        logger.debug(rows[i]["id"])
        all_cards.append(generate_order_card(rows[i]["id"]))
        all_cards.append(html.Br())
    return all_cards


@app.callback(
    Output(gen_id(TABLE), 'rows'),
    [Input(gen_id('all-day-month-year'), 'value')]
)
def update_order_table(value):
    logger.debug(value)
    all_order = app_controller.get_club_order_list(CLUB_NAME)
    ret_order = None
    first_day = None
    last_day = None
    if value.lower() == "all":
        ret_order = all_order
    elif value.lower() == "day":
        first_day = datetime.datetime.utcnow().replace(day=1, hour=0, minute=0, second=0)
        last_day = first_day + relativedelta(days=1)
    elif value.lower() == 'month':
        first_day = datetime.datetime.utcnow().replace(day=1, hour=0, minute=0, second=0)
        last_day = first_day + relativedelta(months=1)
    elif value.lower() == 'year':
        first_day = datetime.datetime.utcnow().replace(day=1, hour=0, minute=0, second=0)
        last_day = first_day + relativedelta(years=1)

    ret_order = [item for item in all_order if item.between_time(first_day, last_day)]
    return generate_order_data(ret_order)

