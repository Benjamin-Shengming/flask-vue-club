#!/usr/bin/python3
from collections import OrderedDict
from uuid import uuid1
import base64
import dash
import json
import dash_core_components as dcc
import dash_html_components as html
import sd_material_ui
from dash.dependencies import Event, State, Input, Output
from pprint import pprint
from app import app
from app import app_controller
import filestore
from magic_defines import *


def generate_id(index):
    section_id = "service_book_img_section_{}".format(index)
    upload_id ='service_book_upload_{}'.format(index)
    img_id ="service_book_img_{}".format(index)
    txt_id = "service_book_txt_{}".format(index)
    return section_id, upload_id, img_id, txt_id


def generate_img_id(index):
    _, _, img_id, _ = generate_id(index)
    return img_id


def generate_txt_id(index):
    _, _, _, txt_id = generate_id(index)
    return txt_id


def generate_img_txt(service_id, index):
    section_id, upload_id, img_id, txt_id = generate_id(index)
    img_src = filestore.get_service_img_link(service_id, index)
    print(img_src)
    txt_content = filestore.get_service_txt_content(service_id, index)
    img_txt_section = html.Div(id = section_id, children=[
        html.Div(className="row", children=[
                html.Div(className="col-sm-12", children=[
                    html.Img(id=img_id,
                             src=img_src,
                             className="img-fluid"),
                ]),
        ]) if img_src else "",
        html.Div(className="row", children=[
                html.Div(className="col-sm-12", children=[
                    html.P(txt_content)
                ]),
        ]) if txt_content else ""
    ])
    return img_txt_section


def layout(service_id):
    service = app_controller.get_club_service(CLUB_NAME, service_id)
    major_img_link = filestore.get_service_img_link(service_id, MAJOR_IMG)
    print(major_img_link)
    return html.Div(children=[
        html.Label( # service uuid
            title=service.id,
            id="service_book_uuid",
            style={"display": 'none'}
        ),
        html.Div(className="row", children=[
                html.Div(className="col-sm-12", children=[
                    html.H1(service.name)
                ])
        ]),
        html.Div(className="row", children=[
                html.Div(className="col-sm-12", children=[
                    html.P(service.description)
                ])
        ]),
        html.Div(className="row", children=[
                html.Div(className="col-sm-12", children=[
                    html.Label("Price: {}".format(service.price))
                ])
        ]),
        html.Div(className="row", children=[
                html.Div(className="col-sm-12", children=[
                    html.Label("Discount:{}".format(service.discount))
                ])
        ]),
        html.Div(className="row", children=[
            html.Div(className="col-sm-12", children=[
                html.Img(id="service_book_img_major",
                         src=filestore.get_service_img_link(service_id, MAJOR_IMG),
                         className="img-fluid"),
            ]),
        ]),
        html.Div(id="service_book_imgs_and_texts", children=[
            generate_img_txt(service_id, i) for i in range(MAX_IMG_TXT)
        ]),
        html.Hr(),
        dcc.Link(className="float", href= "/shopping/cart/{}".format(service_id), children=[
            html.Label("Book", className="btn btn-primary")
        ])
    ])

