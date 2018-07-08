#!/usr/bin/python3
from collections import OrderedDict
from uuid import uuid1
import dash
import json
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Event, State, Input, Output
from pprint import pprint
from magic_defines import *
from app import app
from app import app_controller
import filestore
import local_storage
from utils import *
from dash.exceptions import PreventUpdate

import coloredlogs, logging
logger = logging.getLogger(__name__)
coloredlogs.install(level='DEBUG', logger=logger)

def generate_tb_header():
    return html.Thead(
                html.Tr(children=[
                    html.Th("Product",style={"width":"50%"}),
                    html.Th("Price", style={"width":"10%"}),
                    html.Th("Quantity", style={"width":"8%"}),
                    html.Th("Subtotal", style={"width":"22%"}, className="text-center"),
                    html.Th(style={"width":"10%"})
                ])
             )

def generate_tb_footer():
    return html.Tfoot(children=[
      html.Tr(children=[
        html.Td(children=[
            dcc.Link(href="/service/list", className="btn btn-warning", children=[
                html.I(className="fa fa-angle-left"),
                "Conitnue Shopping"
            ])
        ]),
        html.Td(className="hidden-xs"),
        html.Td(className="hidden-xs text-center", children=[
            html.Strong("Total $1.99")
        ]),
        html.Td(children=[
            html.Button(id="user_shopcart_button_checkout",
                        className="btn btn-success btn-block",
                        n_clicks=0,
                        children=[
                            "Checkout",
                            html.I(className="fa fa-angle-right")
                        ])
        ])
      ])

    ])

def generate_service_del(sid):
        return html.Td(className="actions", children=[
            html.Button(id = "user_shopcart_del_service_{}".format(sid), className="btn btn-danger btn-sm", children=[
                html.I(className="fa fa-trash")
            ])
        ])

def generate_service_item(service, quantity):
      return html.Tr(children=[
        html.Td(**{"data-th": "Product"}, children=[
          html.Div(className="row", children=[
            html.Div(className="col-sm-2 hidden-xs", children =[
                html.Img(src=filestore.get_service_img_link(service.id, MAJOR_IMG),
                         width="100px",
                         height="100px",
                         alt=service.name,
                         className="img-responsive")
            ]),
            html.Div(className="col-sm-1 hidden-xs", children =[""]),
            html.Div(className="col-sm-9", children=[
              html.H4(service.name,className="nomargin"),
              html.P(service.description)
            ])
          ])
        ]),
        html.Td(**{"data-th":"Price"}, children=[service.price]),
        html.Td(**{"data-th":"Quantity"}, children=[
          dcc.Input(type="number",
                     className="form-control text-center",
                     value=quantity)

        ]),
        html.Td(**{"data-th":"Subtotal"}, className="text-center", children=["1.99"]),
        generate_service_del(service.id)
      ])

def generate_all_cart_service(cart_service):
    item_list = []
    for item in cart_service:
        quantity, service = item
        item_list.append(generate_service_item(service, quantity))
    return item_list

def generate_tb_body(cart_info):
    s_ids = cart_info.keys()
    cart_service = [(cart_info[s_id], app_controller.get_club_service(CLUB_NAME, s_id)) for s_id in s_ids]
    return html.Tbody(children= generate_all_cart_service(cart_service))


def layout(user_info, cart_info):
    logger.debug(user_info)
    logger.debug(cart_info)
    return html.Div(className="container", children=[
        local_storage.LocalStorageComponent(id="user_shopcart_user_storage", label=USER_STORAGE),
        local_storage.LocalStorageComponent(id="user_shopcart_cart_storage", label=CART_STORAGE),
        html.Table(id="cart", className="table table-hover table-condensed", children=[
            generate_tb_header(),
            generate_tb_body(cart_info),
            generate_tb_footer()
        ])
    ])




@app.callback(Output('user_shopcart_cart_storage', 'value'),
              [Input("user_shopcart_button_checkout", "n_clicks")],
              [State("user_shopcart_cart_storage", "value"),
               State("user_shopcart_user_storage", "value"),
               ])
def checkout(n_clicks, cart_info_str, user_info_str):
    logger.debug("shop cart checkout, n_clicks {}".format(n_clicks))
    logger.debug(user_info_str)
    logger.debug(cart_info_str)
    raise PreventUpdate()
    cart_info = load_cart_info_from_storage(cart_info_str)
    user_info = load_user_info_from_storage(user_info_str)
    return json.dumps({})

