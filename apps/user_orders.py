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



import gettext
zh = gettext.translation("user_orders", locale_d(), languages=["zh_CN"])
zh.install(True)
_ = zh.gettext
def gen_id(name):
    # user module as name prefix
    s_id = g_id(__name__, name)
    return s_id

def generate_layout(orders):
    if not orders:
        return html.Div([
            html.H4(_("No orders")),
        ])
    orders_data = [{"id":item.id, "time":item.time} for item in orders]

    return html.Div([
        html.H4(_("All orders")),
        dt.DataTable(
            rows= orders_data if orders_data else [{_("No order"): _("No order")}],

            # optional - sets the order of columns
            #columns=sorted(DF_GAPMINDER.columns),
            resizable=True,
            row_selectable=True,
            filterable=True,
            sortable=True,
            editable=False,
            selected_row_indices=[0],
            id=gen_id(TABLE)
        ),
        html.Hr(),
        html.Div(_("click one order to view detail")),
        html.Div(id=gen_id("order-cards")),
        html.Hr()
    ])


def layout(user_info):
    logger.debug(user_info)

    user = app_controller.get_club_user_by_jwt(CLUB_NAME, user_info)
    if not user:
        return dcc.Link(href="/user/login",
                    className="col btn btn-warning float-left ", children=[
            html.I(className="fa fa-angle-left"),
            _("Please login firstly")
        ])

    return generate_layout(user.orders)

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
            html.Div(className="p-2", children=[_("price: {}*{}={}").format(order_detail.price,
                                                            order_detail.discount_percent_str(),
                                                            order_detail.final_price())
            ]),
            html.Div(className="p-2", children=[
                html.Span(_("Qty: {}").format(order_detail.quantity))
            ]),
            html.Div(className="p-2",children=[
                html.Div(children=[_("Subtotal:"),order_detail.calc_price()]),
            ])
        ])
    ])

def generate_order(order):
    detail = []
    header = html.Div(className="d-flex justify-content-between",children=[
            html.Div(className="p-2", children=[
                html.Span(_("order id: {}").format(order.id))
            ]),
            html.Div(className="p-2", children=[
                html.Span(_("Paid: {}").format(order.paid))
            ]),
            html.Div(className="p-2",children=[
                html.Div(children=[_("time:"),order.time]),
            ])
        ])
    detail.append(header)
    detail.append(html.Hr())
    for item in order.details:
        detail.append(generate_order_detail(item))
    detail.append(html.Hr())

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
def update_service_cards(rows, selected_row_indices):
    all_cards = []
    for i in selected_row_indices:
        logger.debug(rows[i]["id"])
        all_cards.append(generate_order_card(rows[i]["id"]))
        all_cards.append(html.Br())
    return all_cards


