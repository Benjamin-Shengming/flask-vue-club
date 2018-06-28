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


headline_services = app_controller.get_club_headline_service(CLUB_NAME)

club_services = app_controller.get_club_service_list(CLUB_NAME)

carousel = html.Div(**{"data-ride":"carousel"}, id="carouselExampleIndicators", className="carousel slide", children=[
    html.Ol(className="carousel-indicators", children=[
        html.Li(**{"data-target":"#carouselExampleIndicators", "data-slide-to":"0"}, className="active"),
        html.Li(**{"data-target":"#carouselExampleIndicators", "data-slide-to":"1"}),
        html.Li(**{"data-target":"#carouselExampleIndicators", "data-slide-to":"2"}),
    ]),
    html.Div(className="carousel-inner", children=[
        html.Div(className="carousel-item active", children=[
            html.Img(className="d-block w-100", src="/assets/img/fall-autumn-red-season.jpg?auto=yes&bg=666&fg=444&text=First slide", alt="First slide")
        ]),
        html.Div(className="carousel-item", children=[
            html.Img(className="d-block w-100", src="/assets/img/pexels-photo-248797.jpeg?auto=yes&bg=666&fg=444&text=Second slide", alt="Second slide")
        ]),
        html.Div(className="carousel-item", children=[
            html.Img(className="d-block w-100", src="/assets/img/pexels-photo-257360.jpeg?auto=yes&bg=555&fg=333&text=Third slide", alt="Third slide")
        ]),
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
cards = html.Div(className="card-deck", children=[
  html.Div(className="card", children=[
    html.Img(className="card-img-top", src="/assets/img/pexels-photo-302804.jpeg",alt="Card image cap"),
    html.Div(className="card-body", children=[
      html.H5("Card title", className="card-title"),
      html.P("This is a wider card with supporting text below as a natural lead-in to additional content. This content is a little bit longer.", className="card-text")
    ]),
    html.Div(className="card-footer", children=[
      html.Small("Last updated 3 mins ago", className="text-muted")
    ])
  ]),
  html.Div(className="card", children=[
    html.Img(className="card-img-top", src="/assets/img/pexels-photo-459225.jpeg",alt="Card image cap"),
    html.Div(className="card-body", children=[
      html.H5("Card title", className="card-title"),
      html.P("This is a wider card with supporting text below as a natural lead-in to additional content. This content is a little bit longer.",className="card-text")
    ]),
    html.Div(className="card-footer", children=[
      html.Small("Last updated 3 mins ago", className="text-muted")
    ])
  ]),
  html.Div(className="card", children=[
    html.Img(className="card-img-top", src="/assets/img/pexels-photo-459225.jpeg",alt="Card image cap"),
    html.Div(className="card-body", children=[
      html.H5("Card title", className="card-title"),
      html.P("This is a wider card with supporting text below as a natural lead-in to additional content. This content is a little bit longer.",className="card-text")
    ]),
    html.Div(className="card-footer", children=[
      html.Small("Last updated 3 mins ago", className="text-muted")
    ])
  ]),
  html.Div(className="card", children=[
    html.Img(className="card-img-top", src="/assets/img/pexels-photo-459225.jpeg",alt="Card image cap"),
    html.Div(className="card-body", children=[
      html.H5("Card title", className="card-title"),
      html.P("This is a wider card with supporting text below as a natural lead-in to additional content. This content is a little bit longer.",className="card-text")
    ]),
    html.Div(className="card-footer", children=[
      html.Small("Last updated 3 mins ago", className="text-muted")
    ])
  ]),
  html.Div(className="card", children=[
    html.Img(className="card-img-top", src="/assets/img/pexels-photo-459225.jpeg",alt="Card image cap"),
    html.Div(className="card-body", children=[
      html.H5("Card title", className="card-title"),
      html.P("This is a wider card with supporting text below as a natural lead-in to additional content. This content is a little bit longer.",className="card-text")
    ]),
    html.Div(className="card-footer", children=[
      html.Small("Last updated 3 mins ago", className="text-muted")
    ])
  ])
])

layout = html.Div(children=[
    html.Hr(),
    carousel,
    cards
])

