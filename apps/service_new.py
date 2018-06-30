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
    section_id = "img_section_{}".format(index)
    upload_id ='service_new_upload_{}'.format(index)
    img_id ="service_new_img_{}".format(index)
    txt_id = "service_new_txt_{}".format(index)
    return section_id, upload_id, img_id, txt_id


def generate_img_id(index):
    _, _, img_id, _ = generate_id(index)
    return img_id


def generate_txt_id(index):
    _, _, _, txt_id = generate_id(index)
    return txt_id


def generate_new_img_txt(index):
    section_id, upload_id, img_id, txt_id = generate_id(index)
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
                             src="",
                             className="img-fluid"),
                ]),
        ]),
        html.Div(className="row", children=[
                html.Div(className="col-sm-12", children=[
                    dcc.Textarea(id=txt_id,
                            placeholder="Please input picture description",
                            style={'width':'100%'},
                            className="form-control form-control-lg")
                ]),
        ]),
        html.Hr()
    ])
    return img_txt_section


layout = html.Div(children=[
    html.Label( # service uuid
        title=str(uuid1()),
        id="service_new_uuid",
        style={"display": 'none'}
    ),
    html.Div(className="row", children=[
            html.Div(className="col-sm-12", children=[
                html.Label("Title:")
            ]),
    ]),
    html.Div(className="row", children=[
            html.Div(className="col-sm-12", children=[
                dcc.Input(id="service_new_title",
                        placeholder="Please input title",
                        className="form-control form-control-lg")
            ])
    ]),
    html.Div(className="row", children=[
            html.Div(className="col-sm-12", children=[
                html.Label("Description:")
            ]),
    ]),
    html.Div(className="row", children=[
            html.Div(className="col-sm-12", children=[
                dcc.Textarea(id="service_new_description",
                        placeholder="Please input service description",
                        style={'width':'100%'},
                        className="form-control form-control-lg")
            ])
    ]),
    html.Div(className="row", children=[
            html.Div(className="col-sm-12", children=[
                html.Label("Price:")
            ]),
    ]),
    html.Div(className="row", children=[
            html.Div(className="col-sm-12", children=[
                dcc.Input(id="service_new_price",
                        placeholder="Please input service price",
                        style={'width':'100%'},
                        type="number",
                        value=500,
                        step=1,
                        className="form-control form-control-lg")
            ])
    ]),
    html.Div(className="row", children=[
            html.Div(className="col-sm-12", children=[
                html.Label("discount:")
            ]),
    ]),
    html.Div(className="row", children=[
            html.Div(className="col-sm-12", children=[
                dcc.Input(id="service_new_discount",
                        placeholder="Please input service price",
                        style={'width':'100%'},
                        type="number",
                        value=80,
                        min=0,
                        max=100,
                        step=1,
                        className="form-control form-control-lg")
            ])
    ]),
    html.Div(className="row", children=[
            html.Div(className="col-sm-12", children=[
                html.Label("major picture:")
            ]),
    ]),
    html.Div(className="row", children=[
            html.Div(className="col-sm-12", children=[
                dcc.Upload(
                    id='service_new_upload_major',
                    children=html.Div([
                        'Drag and Drop or ',
                        html.A('Select a File'),
                    ]),
                    style={
                        'width': '100%',
                        'height': '60px',
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
                html.Img(id="service_new_img_major",src="", className="img-fluid"),
            ]),
    ]),
    html.Div(className="row", children=[
            html.Div(className="col-sm-6", children=[
                dcc.Checklist(
                    id="service_new_checklist_online",
                    options=[
                        {'label': 'online', 'value': 'online'},
                    ],
                    values=['online']
                )
            ]),
            html.Div(className="col-sm-6", children=[
                dcc.Checklist(
                    id="service_new_checklist_headline",
                    options=[
                        {'label': 'headline', 'value': 'headline'},
                    ],
                    values=['headline']
                )
            ]),
    ]),
    html.Div(id="service_new_imgs_and_texts", children=[
        generate_new_img_txt(i) for i in range(MAX_IMG_TXT)
    ]),
    html.Hr(),
    html.A(className="topfloat", children=[
        html.Label(id="service_new_msg", children=["mesage show here"])
    ]),
    html.A(className="float", children=[
        html.Button("Submit",
                    id="service_new_button_submit",
                    n_clicks=0,
                    className="btn btn-outline-primary")
    ]),
])


# callbacks setup
def preview_img(contents):
    if contents is not None:
        content_type, content_string = contents.split(',')
        if 'image' in content_type:
            return contents
        else:
            return ""

state_list = [
               State('service_new_uuid', 'title'),
               State('service_new_title', 'value'),
               State('service_new_description', 'value'),
               State('service_new_price', 'value'),
               State('service_new_discount', 'value'),
               State('service_new_img_major', 'src'),
               State('service_new_checklist_online', 'values'),
               State('service_new_checklist_headline', 'values'),
               ]
state_list.extend([State(generate_img_id(i), 'src') for i in range(MAX_IMG_TXT)])
state_list.extend([State(generate_txt_id(i), 'value') for i in range(MAX_IMG_TXT)])


@app.callback(Output('service_new_msg', 'children'),
              [Input('service_new_button_submit', 'n_clicks')],
              state_list
              )
def create_new_service(n_clicks,
                       service_id,
                       title,
                       description,
                       price,
                       discount,
                       img_major_src,
                       online,
                       headline,
                       *img_txt):
    if n_clicks <= 0:
        return ""
    assert(service_id)
    if not title:
        return "Please input title"
    if not description:
        return "Please input description"

    print(price)
    print(discount)
    print(online)
    print(headline)
    #save image and txt to files
    img_list = img_txt[:10]
    txt_list = img_txt[10:]
    # save img to file
    # save major img
    filestore.save_service_img(service_id, "major", img_major_src)
    # save all other imgs
    for i, img_content in enumerate(img_list):
        filestore.save_service_img(service_id, i, img_content)

    # save txt to file
    for i, txt_content in enumerate(txt_list):
        filestore.save_service_txt(service_id, i, txt_content)
    return title


for i in range(MAX_IMG_TXT):
    section_id, upload_id, img_id, txt_id = generate_id(i)
    app.callback(Output(img_id, 'src'),
                [Input(upload_id, 'contents')])(preview_img)

app.callback(Output('service_new_img_major', 'src'),
             [Input('service_new_upload_major', 'contents')])(preview_img)


