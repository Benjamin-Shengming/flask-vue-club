#!/usr/bin/python3
import sys
import os
from random import *
from flask_cors import CORS
from flask import Flask, render_template, jsonify, abort, make_response
import requests
import cherrypy
import argparse
import dash
import local_storage
from dash.dependencies import Input, State, Output
import dash_html_components as html
import dash_core_components as dcc
import pandas as pd
from dash.exceptions import PreventUpdate
import sd_material_ui

# add current folder and lib to syspath
sys.path.append(os.path.join(os.path.dirname(__file__)))
sys.path.append(os.path.join(os.path.dirname(__file__), 'libs'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'apps'))

import coloredlogs, logging
logger = logging.getLogger(__name__)
coloredlogs.install(level='DEBUG', logger=logger)

import user_service_list
import user_service_book
import user_register
import user_login
import user_shopcart
import user_profile
from app import app
from app import app_controller
from models import init_all
from navbar import NavBarDropMenu
from magic_defines import *
from utils import *
from autolink import Redirect
from localstorage_writer import LocalStorageWriter
from localstorage_reader import LocalStorageReader

nav_bar = NavBarDropMenu("HaoDuoYu")
nav_bar.add_drop_menu("Home", ["Service","Contact"])
nav_bar.add_drop_menu("User", ["Login", "Register", "Profile"])
nav_bar.add_shop_cart_button("navbar-shopcart-button")
nav_bar.add_shop_order_button("navbar-shoporder-button")

def generate_main_layout():
    return html.Div([
        # walkalround that let client download js bundle, *bugs* in dash
        Redirect("click me to redirect", href="", style={"display": "none"}),
        LocalStorageWriter(id="global-local-storage-writer", label=USER_STORAGE),
        LocalStorageReader(id="user-local-storage-reader", label=USER_STORAGE),
        LocalStorageReader(id="cart-local-storage-reader", label=CART_STORAGE),
        sd_material_ui.Snackbar(id='snackbar', open=False, message='Polo', action='Reveal'),
        nav_bar.components_tree(),
        # This Location component represents the URL bar
        dcc.Location(id='global-url', refresh=False),
        # Each "page" will modify this element
        html.Div(id='content-container-root'),
        html.Div(id=DUMMY_ID)

    ], className="container-fluid")

app.layout = generate_main_layout


@app.callback(
    Output('content-container-root', 'children'),
    [Input('global-url', 'pathname')],
    [State('user-local-storage-reader', 'value'),
     State('cart-local-storage-reader', 'value')])
def display_page(pathname, user_info_str, cart_info_str):
    user_info = load_user_info_from_storage(user_info_str)
    cart_info = load_cart_info_from_storage(cart_info_str)

    logger.debug(user_info)
    logger.debug(cart_info)
    if not pathname:
        return user_service_list.layout()

    p = pathname.lower()
    if "/service/book/" in p:
        service_id = p.split("/")[-1]
        if service_id:
            return user_service_book.layout(service_id)
    if "/user/login" in p:
        return user_login.layout()

    if "/user/register" in p:
        return user_register.layout()

    if "/user/profile" in p:
        return user_profile.layout(user_info_str)

    if "/shop/cart" in p:
        return user_shopcart.layout(user_info, cart_info)

    return user_service_list.layout()



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run finishing app')
    parser.add_argument('-i', '--init', help="Init all databasee etc", action='store_true')
    args = parser.parse_args()
    if args.init:
        init_all()
        pass
    else:
        for rule in app.server.url_map.iter_rules():
            logger.debug(rule)
        #app.run_server(debug=True, host='0.0.0.0', port=80, ssl_context='adhoc')
        app.run_server(debug=True, host='0.0.0.0', port=80)
        '''
        cherrypy.tree.graft(app.server.wsgi_app, '/')
        cherrypy.config.update({'server.socket_host': '0.0.0.0',
                                'server.socket_port':80,
                                'engine.autoreload.on':False})
        try:
            cherrypy.engine.start()
        except KeyboardInterrupt:
            cherrypy.engine.stop()
        '''




