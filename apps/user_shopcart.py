#!/usr/bin/python3
import json
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import State, Input, Output
from app import app
from app import app_controller
from dash.exceptions import PreventUpdate
from localstorage_writer import LocalStorageWriter
from localstorage_reader import LocalStorageReader
from autolink import Redirect
import gettext
import coloredlogs
import logging
from sd_material_ui import Snackbar
from magic_defines import (CLUB_NAME, S_CONTINUE_SHOP,
                           locale_d, CHECKOUT, S_CHECKOUT,
                           REDIRECT, STORAGE_R, STORAGE_R2,
                           STORAGE_W, USER_STORAGE, CART,
                           CART_STORAGE, PLACEHOLDER, MAJOR_IMG,
                           SNACK_BAR
                           )
from utils import (assert_has_value, assert_button_clicks,
                   load_cart_info_from_storage, calc_cart_total_price,
                   g_id,
                   )

logger = logging.getLogger(__name__)
coloredlogs.install(level='DEBUG', logger=logger)

zh = gettext.translation("user_shopcart", locale_d(), languages=["zh_CN"])
zh.install(True)
_ = zh.gettext

MAX_ITEMS = 100


def gen_del_button_id(i):
    return gen_id("del_service_{}".format(i))


def gen_quantity_input_id(i):
    return gen_id("quantity_input{}".format(i))


def generate_del_button(idx):
    return html.Button(id=gen_del_button_id(idx),
                       className="btn btn-danger btn-sm float-right",
                       children=[html.I(className="fa fa-trash")])


def generate_quantity_input(idx, quantity):
    return dcc.Input(id=gen_quantity_input_id(idx),
                     type="number",
                     min=1,
                     value=quantity,
                     size="5")


def gen_id(name):
    # user module as name prefix
    s_id = g_id(__name__, name)
    return s_id


err_msg_row = Snackbar(id=gen_id(SNACK_BAR), open=False, message=_("checkout"))
class ShoppingCart(object):
    def __init__(self, cart_info_str, controller):
        logger.debug(cart_info_str)
        self.cart_dict = None
        self.controller = controller
        self.cart_service = []
        try:
            logger.debug("loading cart_info_str")
            self.cart_dict = load_cart_info_from_storage(cart_info_str)
        except Exception as e:
            logger.debug(e)
            pass
        logger.debug("cart dict")
        logger.debug(self.cart_dict)
        if self.cart_dict:
            for s_id, quantity in self.cart_dict.items():
                service = self.controller.get_club_service(CLUB_NAME, s_id)
                if service and int(quantity) > 0:
                    self.cart_service.append((quantity, service))

    def total_price(self):
        total = 0
        for item in self.cart_service:
            quantity, service = item
            total += service.calc_price(int(quantity))
        return total

    def header(self):
        return html.Div(children=[
            html.H3(_("Your Shopping Cart")),
            html.Hr()
        ])

    def footer(self):
        return html.Div(className="container-fluid", children=[
            html.Div(className="row", children=[
                html.Div(className="col-12", children=[
                    html.Strong(_("Total {}").format(self.total_price()),
                                className="float-right")
                ])
            ]),
            html.Div(className="row", children=[
                html.Div(className="col-7", children=[
                    dcc.Link(href="/service/list",
                             className="col btn btn-warning float-left ", children=[
                                 html.I(className="fa fa-angle-left"),
                                 S_CONTINUE_SHOP
                             ]),
                ]),
                html.Div(className="col", children=[
                    html.Button(id=gen_id(CHECKOUT),
                                className="btn btn-success btn-block float-right",
                                n_clicks=0,
                                children=[
                                    S_CHECKOUT,
                                    html.I(className="fa fa-angle-right")
                    ])
                ])
            ])
        ])

    def service_item(self, idx, service, quantity):
        return html.Div(className="container-fluid border border-info", children=[
            html.Div(className="d-flex", children=[
                html.Div(className="p-2", children=[
                    html.Img(src=service.get_img_link(MAJOR_IMG),
                             width="100px",
                             height="100px",
                             alt=service.name,
                             className="img-responsive")
                ]),
                html.Div(className="p-2", children=[
                    html.H5(service.name, className="nomargin"),
                    html.P(service.description)
                ])
            ]),
            html.Div(className="d-flex justify-content-between", children=[
                html.Div(className="p-2", children=[_("price: {}*{}={}").format(service.price,
                                                                                service.discount_percent_str(),
                                                                                service.final_price())
                                                    ]),
            ]),
            html.Div(className="d-flex justify-content-between", children=[
                html.Div(className="p-2", children=[
                    html.Span(_("Qty: ")),
                    generate_quantity_input(idx, quantity)
                ]),
            ]),
            html.Div(className="d-flex justify-content-between", children=[
                html.Div(className="p-2", children=[
                    html.Div(children=[_("Subtotal:"), service.calc_price(quantity)]),
                ]),
                html.Div(className="", children=[
                    generate_del_button(idx)
                ])
            ])
        ])

    def all_cart_service(self, cart_service):
        item_list = []
        for idx, item in enumerate(cart_service):
            quantity, service = item
            item_list.append(self.service_item(idx, service, quantity))
            item_list.append(html.Br())
        return item_list

    def body(self):
        return html.Div(children=self.all_cart_service(self.cart_service))

    def layout(self):
        all_left_buttons = [generate_del_button(i) for i in range(len(self.cart_service), MAX_ITEMS)]
        all_left_inputs = [generate_quantity_input(i, 0) for i in range(len(self.cart_service), MAX_ITEMS)]
        return html.Div(id=gen_id(PLACEHOLDER), children=[
            self.header(),
            self.body(),
            html.Hr(),
            self.footer(),
            html.Div(style={"display": "none"}, children=all_left_buttons + all_left_inputs)
        ])


def layout(user_info, cart_info):
    logger.debug(user_info)
    logger.debug(cart_info)
    shop_cart = ShoppingCart(cart_info, app_controller)
    return html.Div(className="container", children=[
        LocalStorageWriter(id=gen_id(STORAGE_W), label=CART_STORAGE),
        LocalStorageWriter(id=gen_id("STORAGE_CHANGE_DELETE"), label=CART_STORAGE),
        LocalStorageWriter(id=gen_id("STORAGE_CHANGE_QUANTITY"), label=CART_STORAGE),
        LocalStorageReader(id=gen_id(STORAGE_R), label=CART_STORAGE),
        LocalStorageReader(id=gen_id(STORAGE_R2), label=USER_STORAGE),
        Redirect(id=gen_id(REDIRECT), href=""),
        html.Div(id=gen_id(CART), className="container-fluid", children=[
            shop_cart.layout()
        ]),
        err_msg_row,
    ])


buttons_list = [Input(gen_del_button_id(i), "n_clicks_timestamp") for i in range(0, MAX_ITEMS)]
inputs_list = [Input(gen_quantity_input_id(i), "value") for i in range(0, MAX_ITEMS)]


def determine_which_button(click_timestamp):
    if not click_timestamp:
        return None
    pos = 0
    largest = 0
    for idx, item in enumerate(click_timestamp):
        if largest < item:
            largest = item
            pos = idx
    return pos


@app.callback(Output(gen_id("STORAGE_CHANGE_DELETE"), 'value'),
              buttons_list,
              [State(gen_id(STORAGE_R), "value")]
              )
def delete_cart_item(*args):
    cart_info_str = args[MAX_ITEMS]
    cart = load_cart_info_from_storage(cart_info_str)
    button_clicks = args[:len(cart)]
    if not cart:
        raise PreventUpdate()

    items = list(cart.items())
    del_key_pos = determine_which_button(button_clicks)
    del_key, _ = items[del_key_pos]
    del cart[del_key]
    return json.dumps(cart)


@app.callback(Output(gen_id(CART), 'children'),
              [Input(gen_id(STORAGE_R), "value")],
              [State(gen_id(REDIRECT), 'href')]
              )
def refresh_cart(cart_info_str, href):
    if href:
        raise PreventUpdate()
    cart = load_cart_info_from_storage(cart_info_str)
    shop_cart = ShoppingCart(cart_info_str, app_controller)
    return shop_cart.layout()


@app.callback(Output(gen_id("STORAGE_CHANGE_QUANTITY"), 'value'),
              inputs_list,
              [State(gen_id(STORAGE_R), "value")]
              )
def change_quantity_cart(*args):
    input_values = args[:MAX_ITEMS]
    cart_info_str = args[MAX_ITEMS]
    logger.debug(cart_info_str)
    cart = load_cart_info_from_storage(cart_info_str)
    count = len(cart)
    items = list(cart.items())
    for i in range(0, count):
        key, value = items[i]
        cart[key] = input_values[i]

    if len(cart):
        return json.dumps(cart)
    raise PreventUpdate()


@app.callback(Output(gen_id(REDIRECT), 'href'),
              [Input(gen_id(STORAGE_R), "value")],
              [State(gen_id(CHECKOUT), "n_clicks")])
def redirect_to_order(cart_info_str, n_clicks):
    assert_button_clicks(n_clicks)
    if cart_info_str == "/shop/order":
        return "/shop/order"
    raise PreventUpdate()


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
        return "/shop/order"
    raise PreventUpdate()


@app.callback(Output(gen_id(SNACK_BAR), 'message'),
              [Input(gen_id(CHECKOUT), "n_clicks")],
              [State(gen_id(STORAGE_R), "value"),
               State(gen_id(STORAGE_R2), "value")]
              )
def change_message(n_clicks, cart_info_str, jwt):
    assert_button_clicks(n_clicks)
    if not jwt:
        return _("Please login firstly!")
    user = app_controller.get_club_user_by_jwt(CLUB_NAME, jwt)
    if not user:
        return _("Please login firstly!")
    cart = load_cart_info_from_storage(cart_info_str)
    if not cart or calc_cart_total_price(cart) <= 0:
        return _("Nothing in your shopping cart")

    return ""


@app.callback(Output(gen_id(SNACK_BAR), 'open'),
              [Input(gen_id(SNACK_BAR), "message")]
              )
def show_message(msg):
    if msg:
        return True
    else:
        return False
