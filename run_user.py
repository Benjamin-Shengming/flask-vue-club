#!/usr/bin/python3
import sys
import os
from random import *
from flask_cors import CORS
from flask import Flask, render_template, jsonify, abort, make_response, request
import requests
import cherrypy
import argparse
import dash
from dash.dependencies import Input, State, Output
import dash_html_components as html
import dash_core_components as dcc
import pandas as pd
from dash.exceptions import PreventUpdate
import sd_material_ui
from wechatpy.utils import check_signature
from wechatpy.exceptions import InvalidSignatureException
from wechatpy import parse_message
from wechatpy.replies import TextReply, VoiceReply, create_reply, ImageReply, ArticlesReply
from wechatpy.crypto import WeChatCrypto

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
import user_orders
from app import app, server
from app import app_controller
from models import init_all
from navbar import NavBarDropMenu
from magic_defines import *
from utils import *
from autolink import Redirect
from localstorage_writer import LocalStorageWriter
from localstorage_reader import LocalStorageReader
import dash_table_experiments as dt
nav_bar = NavBarDropMenu(CLUB_NAME)
nav_bar.add_drop_menu("Home", ["Service","Contact"])
nav_bar.add_drop_menu("User", ["Login", "Register", "Profile"])
nav_bar.add_shop_cart_button("navbar-shopcart-button")
nav_bar.add_shop_order_button("navbar-shoporder-button")

def gen_id(name):
    # user module as name prefix
    s_id = g_id(__name__, name)
    return s_id

def generate_main_layout():
    return html.Div([
        # walkalround that let client download js bundle, *bugs* in dash
        Redirect("click me to redirect", href="", style={"display": "none"}),
        LocalStorageWriter(id="global-local-storage-writer", label=USER_STORAGE),
        LocalStorageReader(id="user-local-storage-reader", label=USER_STORAGE),
        LocalStorageReader(id=gen_id("main_cart_reader"), label=CART_STORAGE),
        html.Div(style={"display": "none"}, children=[
            dt.DataTable(id="global-table-hiden",
                        rows= [{"No data":"no data"}],
                        row_selectable=True,
                        filterable=True,
                        sortable=True,
                        editable=False,
                        selected_row_indices=[]),

        ]),
        sd_material_ui.Snackbar(id='snackbar', open=False, message='Polo', action='Reveal'),
        nav_bar.components_tree(),
        # This Location component represents the URL bar
        dcc.Location(id='global-url', refresh=False),
        # Each "page" will modify this element
        html.Div(id='content-container-root'),
        html.Div(id=DUMMY_ID)

    ], className="container-fluid")

app.layout = generate_main_layout

@server.route('/api_v1/<club_name>/wechat', methods=['GET', 'POST'])
def wechat(club_name):
    logger.debug(club_name)
    query = request.args
    logger.debug(query)
    signature = query.get('signature', '')
    timestamp = query.get('timestamp', '')
    nonce = query.get('nonce', '')
    logger.debug(request.args)
    try:
        check_signature(TOKEN, signature, timestamp, nonce)
    except Exception as e:
        logger.debug("invalid request!")
        abort(403)

    if request.method == 'GET':
        return make_response(request.args.get('echostr', ''))
    else:
        logger.debug("start make response")
        encrypt_type = request.args.get('encrypt_type', 'raw')
        xml = request.data
        msg = None
        if encrypt_type == 'raw':
            # plain mode
            logger.debug("plain mode")
            msg = parse_message(xml)
        else:
            try:
                # encrypt mode
                crypto = WeChatCrypto(TOKEN, AES_KEY, APP_ID)
                msg = parse_message(crypto.decrypt_message(xml, signature, timestamp, nonce))
            except Exception as e:
                abort(403)

        reply_xml = None
        if msg.type == 'text':
            key_words = [item.strip() for item in str(msg.content).split(" ")]
            articles = app_controller.search_club_service_article(club_name, key_words)
            for article in articles:
                article['image'] = "{}{}".format(get_host(), article['image'])
                article['url'] = "{}{}".format(get_host(), article['url'])
            reply =  ArticlesReply(articles=articles, message=msg)
            reply_xml = reply.render()
        else:
            reply = TextReply(content='Not supported!', message=msg)
            reply_xml = reply.render()

        logger.debug("xml:" + reply_xml)
        if encrypt_type == "raw":
            return reply_xml
        else:
            return crypto.encrypt_message(reply_xml, nonce, timestamp)

@app.callback(
    Output('content-container-root', 'children'),
    [Input('global-url', 'pathname')],
    [State('user-local-storage-reader', 'value'),
     State(gen_id("main_cart_reader"), 'value')])
def display_page(pathname, user_info_str, cart_info_str):
    logger.debug("print path")
    logger.debug(pathname)
    app_controller.create_remote_ip_activity(request.remote_addr)
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
        return user_shopcart.layout(user_info_str, cart_info_str)
    if "/shop/order" in p:
        return user_orders.layout(user_info_str)

    if "/api_v1" in p and "wechat" in p:
        return wechat(CLUB_NAME)


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
        #app.run_server(debug=True, host='0.0.0.0', port=80)
        cherrypy.tree.graft(app.server.wsgi_app, '/')
        cherrypy.config.update({'server.socket_host': '0.0.0.0',
                                'server.socket_port':80,
                                'engine.autoreload.on':False})
        try:
            cherrypy.engine.start()
        except KeyboardInterrupt:
            cherrypy.engine.stop()




