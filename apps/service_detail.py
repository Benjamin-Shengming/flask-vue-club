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
from autolink import Redirect
from utils import *

import coloredlogs, logging
logger = logging.getLogger(__name__)
coloredlogs.install(level='DEBUG', logger=logger)


import gettext
zh = gettext.translation("service_detail", locale_d(), languages=["zh_CN"])
zh.install(True)
_ = zh.gettext


def gen_id(name):
    return g_id(__name__, name)

def generate_id(index):
    section_id = "service_detail_img_section_{}".format(index)
    upload_id ='service_detial_upload_{}'.format(index)
    img_id ="service_detail_img_{}".format(index)
    txt_id = "service_detail_txt_{}".format(index)
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
        html.Div(className="row align-items-center", children=[
            html.Div(className="col-sm-12", children=[
                dcc.Upload(
                    id=upload_id,
                    children=html.Div([
                        'Drag and Drop or ',
                        html.A('Select a File'),
                    ]),
                    style={
                        'width': '100%',
                        'height': '100%',
                        'borderWidth': '1px',
                        'borderStyle': 'dashed',
                        'borderRadius': '5px',
                        'textAlign': 'center',
                    }
                ),
            ])
        ]),
        html.Div(className="row", children=[
                html.Div(className="col-sm-12", children=[
                    html.Img(id=img_id,
                             src=img_src,
                             className="img-fluid"),
                ]),
        ]),
        html.Div(className="row", children=[
                html.Div(className="col-sm-12", children=[
                    dcc.Textarea(id=txt_id,
                            placeholder=_("Please input picture description"),
                            style={'width':'100%'},
                            value=txt_content if txt_content else "",
                            className="form-control form-control-lg")
                ]),
        ]),
        html.Hr()
    ])
    return img_txt_section

float_msg = html.A(className="topfloat", children=[
            html.Label(id="service_detail_msg", children=[_("mesage show here")])
        ])
float_button = html.A(className="float", children=[
            html.Button(_("Submit"),
                        id="service_detail_button_submit",
                        n_clicks=0,
                        className="btn btn-outline-primary")
        ])
float_button_del = html.A(className="secondfloat", children=[
            html.Button(_("Delete"),
                        id=gen_id("button-del"),
                        n_clicks=0,
                        className="btn btn-outline-danger")
        ])
auto_link = Redirect(id=gen_id("redirect-to-list"), href="")

def layout(service_id):
    service = app_controller.get_club_service(CLUB_NAME, service_id)
    major_img_link = filestore.get_service_img_link(service_id, MAJOR_IMG)
    print(major_img_link)
    return html.Div(children=[
        html.Label( # service uuid
            title=service.id,
            id="service_detail_uuid",
            style={"display": 'none'}
        ),
        html.Div(className="row", children=[
                html.Div(className="col-sm-12", children=[
                    html.Label(_("Title:"))
                ]),
        ]),
        html.Div(className="row", children=[
                html.Div(className="col-sm-12", children=[
                    dcc.Input(id="service_detail_title",
                            placeholder=_("Please input title"),
                            value=service.name,
                            className="form-control form-control-lg")
                ])
        ]),
        html.Div(className="row", children=[
                html.Div(className="col-sm-12", children=[
                    html.Label(_("Description:"))
                ]),
        ]),
        html.Div(className="row", children=[
                html.Div(className="col-sm-12", children=[
                    dcc.Textarea(id="service_detail_description",
                            placeholder=_("Please input service description"),
                            value=service.description,
                            style={'width':'100%'},
                            className="form-control form-control-lg")
                ])
        ]),
        html.Div(className="row", children=[
                html.Div(className="col-sm-12", children=[
                    html.Label(_("Price:"))
                ]),
        ]),
        html.Div(className="row", children=[
                html.Div(className="col-sm-12", children=[
                    dcc.Input(id="service_detail_price",
                            placeholder=_("Please input service price"),
                            style={'width':'100%'},
                            type="number",
                            value=service.price,
                            step=1,
                            className="form-control form-control-lg")
                ])
        ]),
        html.Div(className="row", children=[
                html.Div(className="col-sm-12", children=[
                    html.Label(_("discount:"))
                ]),
        ]),
        html.Div(className="row", children=[
                html.Div(className="col-sm-12", children=[
                    dcc.Input(id="service_detail_discount",
                            placeholder=_("Please input service price"),
                            style={'width':'100%'},
                            type="number",
                            value=service.discount,
                            min=0,
                            max=100,
                            step=1,
                            className="form-control form-control-lg")
                ])
        ]),
        html.Div(className="row", children=[
                html.Div(className="col-sm-12", children=[
                    html.Label(_("major picture:"))
                ]),
        ]),
        html.Div(className="row", children=[
                html.Div(className="col-sm-12", children=[
                    dcc.Upload(
                        id='service_detail_upload_major',
                        children=html.Div([
                            'Drag and Drop or ',
                            html.A('Select a File'), ]), style={ 'width': '100%', 'height': '60px',
                            'lineHeight': '60px',
                            'borderWidth': '1px',
                            'borderStyle': 'dashed',
                            'borderRadius': '5px',
                            'textAlign': 'center',
                            'margin': '10px'
                        }
                    ),
                ])
        ]),
        html.Div(className="row", children=[
            html.Div(className="col-sm-12", children=[
                html.Img(id="service_detail_img_major",
                         src=filestore.get_service_img_link(service_id, MAJOR_IMG),
                         className="img-fluid"),
            ]),
        ]),
        html.Div(className="row", children=[
                html.Div(className="col-sm-6", children=[
                    dcc.Checklist(
                        id="service_detail_checklist_online",
                        options=[
                            {'label': 'online', 'value': 'online'},
                        ],
                        values= ['online'] if service.active else []
                    )
                ]),
                html.Div(className="col-sm-6", children=[
                    dcc.Checklist(
                        id="service_detail_checklist_headline",
                        options=[
                            {'label': 'headline', 'value': 'headline'},
                        ],
                        values=['headline'] if service.slide else []
                    )
                ]),
        ]),
        html.Div(id="service_detail_imgs_and_texts", children=[
            generate_img_txt(service_id, i) for i in range(MAX_IMG_TXT)
        ]),
        html.Hr(),
        float_msg,
        float_button,
        float_button_del,
        auto_link
    ])


# callbacks setup
def preview_img(contents):
    if not contents:
        raise PreventUpdate()
    content_type, content_string = contents.split(',')
    if 'image' in content_type:
        return contents
    else:
        return ""




def update_service(n_clicks,
                       service_id,
                       title,
                       description,
                       price,
                       discount,
                       img_major_src,
                       online,
                       headline,
                       *img_txt):
    logger.debug("update service " + service_id)
    if n_clicks <= 0:
        return ""
    assert(service_id)
    print(title)
    if not title:
        return html.Label(_("please input title"))
    print(description)
    if not description:
        return html.Label(_("please input description"))
    if not img_major_src:
        return html.Label(_("please choose major image"))
    #save image and txt to files
    img_list = img_txt[:10]
    txt_list = img_txt[10:]
    # save img to file
    # save major img
    logger.debug("update service update major image")
    filestore.save_service_img(service_id, "major", img_major_src)
    # save all other imgs
    logger.debug("update service save all other images")
    for i, img_content in enumerate(img_list):
        filestore.save_service_img(service_id, i, img_content)

    # save txt to file
    logger.debug("save text file")
    for i, txt_content in enumerate(txt_list):
        filestore.save_service_txt(service_id, i, txt_content)
    return html.Label(_("service updated successfully"))

state_list = [
            State('service_detail_uuid', 'title'),
            State('service_detail_title', 'value'),
            State('service_detail_description', 'value'),
            State('service_detail_price', 'value'),
            State('service_detail_discount', 'value'),
            State('service_detail_img_major', 'src'),
            State('service_detail_checklist_online', 'values'),
            State('service_detail_checklist_headline', 'values'),
            ]
state_list.extend([State(generate_img_id(i), 'src') for i in range(MAX_IMG_TXT)])
state_list.extend([State(generate_txt_id(i), 'value') for i in range(MAX_IMG_TXT)])

for i in range(MAX_IMG_TXT):
    section_id, upload_id, img_id, txt_id = generate_id(i)
    app.callback(Output(img_id, 'src'),
                [Input(upload_id, 'contents')])(preview_img)

app.callback(Output('service_detail_img_major', 'src'),
            [Input('service_detail_upload_major', 'contents')])(preview_img)
app.callback(Output('service_detail_msg', 'children'),
            [Input('service_detail_button_submit', 'n_clicks')],
            state_list)(update_service)

@app.callback(Output(gen_id("redirect-to-list"), 'href'),
            [Input(gen_id('button-del'), 'n_clicks')],
            [State('service_detail_uuid', 'title')])
def del_service(n_clicks, uuid):
    logger.debug("delete service " + uuid)
    assert_button_clicks(n_clicks)
    assert_has_value(uuid)
    app_controller.delete_club_service(CLUB_NAME, uuid)
    service = app_controller.get_club_service(CLUB_NAME, uuid)
    if not service:
        filestore.del_service(uuid)
        return "/service/list"

    raise PreventUpdate()
