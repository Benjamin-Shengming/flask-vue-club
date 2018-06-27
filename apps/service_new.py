#!/usr/bin/python3
from collections import OrderedDict
from uuid import uuid1
import dash
import json
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Event, State, Input, Output
from pprint import pprint
from app import app

MAX_IMG_TXT = 10


def generate_id(index):
    section_id = "img_section_{}".format(index)
    upload_id ='service_new_upload_{}'.format(index)
    img_id ="service_new_img_{}".format(index)
    txt_id = "service_new_txt_{}".format(index)
    return section_id, upload_id, img_id, txt_id

def generate_new_img(index):
    section_id, upload_id, img_id, txt_id = generate_id(index)
    img_section = html.Div(id = section_id, children=[
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
    return img_section

def generate_new_txt(index):
    pass


layout = html.Div(children=[
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
                    id='upload',
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
                html.Img(id="major-img",src="", className="img-fluid"),
            ]),
    ]),
    html.Div(className="row", children=[
            html.Div(className="col-sm-6", children=[
                dcc.Checklist(
                    options=[
                        {'label': 'online', 'value': 'online'},
                    ],
                    values=['online']
                )
            ]),
            html.Div(className="col-sm-6", children=[
                dcc.Checklist(
                    options=[
                        {'label': 'headline', 'value': 'headline'},
                    ],
                    values=['headline']
                )
            ]),
    ]),
    html.Div(id="service_new_imgs_and_texts", children=[
        generate_new_img(i) for i in range(MAX_IMG_TXT)
    ]),
    html.Div(className="row", children=[
        html.Div(className="col-sm-12", children=[
            html.Label(id="service_new_label_message", children=[""])
        ])
    ]),
    html.Hr(),
    html.A(className="float", children=[
        html.Button("Submit",
                    id="service_new_button_submit",
                    n_clicks=0,
                    className="btn btn-outline-primary")
    ])
])


# callbacks setup
def preview_img(contents):
    if contents is not None:
        content_type, content_string = contents.split(',')
        if 'image' in content_type:
            return contents
        else:
            return ""

@app.callback(Output('service_new_label_message', 'children'),
              [Input('service_new_button_submit', 'n_clicks')],
              [State('service_new_imgs_and_texts', 'children')])
def create_new_service(n_clicks, imgs_texts_children):
    if n_clicks <= 0:
        return ""

    for item in imgs_texts_children:
        print(json.dumps(item, indent=2))
    return len(imgs_texts_children)


for i in range(MAX_IMG_TXT):
    section_id, upload_id, img_id, txt_id = generate_id(i)
    app.callback(Output(img_id, 'src'),
                [Input(upload_id, 'contents')])(preview_img)

app.callback(Output('major-img', 'src'),
             [Input('upload', 'contents')])(preview_img)


