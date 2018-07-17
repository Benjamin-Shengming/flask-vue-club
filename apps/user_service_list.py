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
import math

import coloredlogs, logging
logger = logging.getLogger(__name__)
coloredlogs.install(level='DEBUG', logger=logger)


import gettext
zh = gettext.translation("user_service_list", locale_d(), languages=["zh_CN"])
zh.install(True)
_ = zh.gettext


def generate_carousel():
    headline_services = app_controller.get_club_headline_service(CLUB_NAME)
    if not headline_services:
        print("no headline")
        return html.Div()
    service_count = len(headline_services)
    carousel = html.Div(**{"data-ride":"carousel"},
                        id="carouselExampleIndicators",
                        className="carousel slide",
                        children=[
        html.Ol(className="carousel-indicators", children=[
            html.Li(**{"data-target":"#carouselExampleIndicators", "data-slide-to":str(i)}, className="active" if i ==0 else "") for i in range(service_count)
        ]),
        html.Div(className="carousel-inner", children=[
            html.Div(className="carousel-item active" if i ==0 else "carousel-item", children=[
                html.Div(className="d-flex", children=[
                    dcc.Link(className="col",href="/service/book/{}".format(service.id), children=[
                        html.Img(className="img-fluid",
                                src=filestore.get_service_img_link(service.id, MAJOR_IMG),
                                alt="Second slide")
                    ]),

                    dcc.Link(className="col",href="/service/book/{}".format(service.id), children=[
                        html.Img(className="img-fluid",
                                src=filestore.get_service_img_link_alt(service.id),
                                alt="Second slide")
                    ])
                ])
            ]) for i, service in enumerate(headline_services)
        ]),
        html.A(**{"data-slide":"prev"}, className="carousel-control-prev", href="#carouselExampleIndicators", role="button", children=[
            html.Span(**{"aria-hidden":"true"}, className="carousel-control-prev-icon"),
            html.Span("Previous", className="sr-only")
        ]),
        html.A(**{"data-slide":"next"}, className="carousel-control-next", href="#carouselExampleIndicators", role="button", children=[
            html.Span(**{"aria-hidden":"true"}, className="carousel-control-next-icon"),
            html.Span("Next", className="sr-only")
        ]),
    ])
    return carousel

def generate_cards():
    logger.debug("generate cards")
    club_services = app_controller.get_club_service_list(CLUB_NAME)
    if not club_services:
        return html.Div()
    cards = []
    for service in club_services:
        card =  html.Div(className="card col-sm-4", children=[
            dcc.Link(href="/service/book/{}".format(service.id), children=[
                html.Div(service.name, className="card-header"),
                html.Img(className="card-img-top",
                        src=filestore.get_service_img_link(service.id, MAJOR_IMG),
                        alt=service.name),
                html.Div(className="card-body", children=[
                    html.P(service.description, className="card-text")
                ]),
                html.Div(className="card-footer", children=[
                    html.Small(service.last_update_time, className="text-muted")
                ])
            ])
        ])
        cards.append(card)

    row_list = []
    count = len(cards)
    logger.debug("number of cards {}".format(count))
    idx = 0
    while idx < count:
        r1 = cards[idx]
        r2 = cards[idx + 1]  if (idx + 1) < count else None
        r3 = cards[idx + 2]  if (idx + 2) < count else None
        row_child = []
        if r1:
            row_child.append(r1)
        if r2:
            row_child.append(r2)
        if r3:
            row_child.append(r3)
        row_list.append(html.Div(className="row", children=row_child))
        idx += 3

    return html.Div(children=row_list)


def layout():
    return  html.Div(children=[
        html.Hr(),
        generate_carousel(),
        html.Hr(),
        html.H4(_("All services")),
        generate_cards()
    ])
