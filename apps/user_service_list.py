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


def generate_carousel():
    print("carousel")
    headline_services = app_controller.get_club_headline_service(CLUB_NAME)
    if not headline_services:
        print("no headline")
        return html.Div()
    service_count = len(headline_services)
    carousel = html.Div(**{"data-ride":"carousel"}, id="carouselExampleIndicators", className="carousel slide", children=[
        html.Ol(className="carousel-indicators", children=[
            html.Li(**{"data-target":"#carouselExampleIndicators", "data-slide-to":str(i)}, className="active" if i ==0 else "") for i in range(service_count)
        ]),
        html.Div(className="carousel-inner", children=[
            html.Div(className="carousel-item active" if i ==0 else "carousel-item", children=[
                html.Img(className="d-block w-100",
                         src=filestore.get_service_img_link(service.id, MAJOR_IMG),
                         alt="Second slide")
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
    print("cards")
    club_services = app_controller.get_club_service_list(CLUB_NAME)
    if not club_services:
        return html.Div()
    cards = html.Div(className="card-deck", children=[
        html.Div(className="card", children=[
            html.Img(className="card-img-top",
                     src=filestore.get_service_img_link(service.id, MAJOR_IMG),
                     alt=service.name),
            html.Div(className="card-body", children=[
                html.H5(service.name, className="card-title"),
                html.P(service.description, className="card-text")
            ]),
            html.Div(className="card-footer", children=[
                html.Small(service.last_update_time, className="text-muted")
            ])
        ]) for service in club_services
    ])
    return cards


def layout():
    return  html.Div(children=[
        html.Hr(),
        generate_carousel(),
        generate_cards()
    ])
