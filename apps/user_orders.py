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
import dash_table_experiments as dt
import coloredlogs, logging
logger = logging.getLogger(__name__)
coloredlogs.install(level='DEBUG', logger=logger)

def gen_id(name):
    # user module as name prefix
    s_id = g_id(__name__, name)
    return s_id

def generate_layout(orders):
    orders_data = [item.to_dict() for item in orders]
    return html.Div([
        html.H4('All orders'),
        dt.DataTable(
            rows= orders_data if orders_data else [{"No order": "No order"}],

            # optional - sets the order of columns
            #columns=sorted(DF_GAPMINDER.columns),

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


def layout(user_info):
    logger.debug(user_info)

    user = app_controller.get_club_user_by_jwt(CLUB_NAME, user_info)
    if not user:
        return dcc.Link("Please login firstly!",
                        href="/user/login",
                        style={"cursor":"pointer"})

    return generate_layout(user.orders)

    return html.Div(className="container", children=[
        LocalStorageReader(id=gen_id(STORAGE_R), label=USER_STORAGE),
        html.Table(id=gen_id(CART), className="table table-hover table-condensed", children=[
            shop_cart.layout()
        ])
    ])




@app.callback(Output(gen_id(STORAGE_W), 'value'),
              [Input(gen_id(CHECKOUT), "n_clicks")],
              [State(gen_id(STORAGE_R), "value"),
               State(gen_id(STORAGE_R2), "value"),
               ])
def checkout(n_clicks, cart_info_str, jwt):
    assert_button_clicks(n_clicks)
    assert_has_value(jwt)
    shop_cart = ShoppingCart(cart_info_str, app_controller)
    order = app_controller.create_club_user_order(CLUB_NAME,
                                          jwt,
                                          shop_cart.cart_service)
    if order:
        return ""
    raise PreventUpdate()

