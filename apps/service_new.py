#!/usr/bin/python3
from collections import OrderedDict
from uuid import uuid1
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Event, State, Input, Output
from pprint import pprint
from app import app

MAX_IMG_TXT = 10


def generate_id(index):
    section_id = "img_section_{}".format(index)
    delete_button_id = "service_new_del_{}".format(index)
    upload_id ='service_new_upload_{}'.format(index)
    img_id ="service_new_img_{}".format(index)
    return section_id, delete_button_id, upload_id, img_id

def generate_new_img(index):
    section_id, delete_button_id, upload_id, img_id, = generate_id(index)
    img_section = html.Div(id = section_id, children=[
        html.Div(className="row align-items-center", children=[
            html.Div(className="col-sm-2", children=[
                html.Button("Delete",
                            id=delete_button_id,
                            className="btn btn-outline-danger")
            ]),
            html.Div(className="col-sm-10", children=[
                dcc.Upload(
                    id=upload_id,
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
                    html.Img(id=img_id,
                             src="",
                             className="img-fluid"),
                ]),
        ]),
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
                dcc.Input(id="service-title",
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
                dcc.Textarea(id="service-descption",
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
                dcc.Input(id="service-price",
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
                dcc.Input(id="service-discount",
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
    html.Div(className="row align-items-center", children=[
            html.Div(className="col-sm-4", children=[
                html.Button("Add Text",
                            id= "service_new_button_add_text",
                            className="btn btn-outline-primary")
            ]),
            html.Div(className="col-sm-4", children=[
                html.Button("Add Image",
                            id= "service_new_button_add_image",
                            className="btn btn-outline-primary")
            ]),
            html.Div(className="col-sm-4", children=[
                html.Button("Submit",
                            id= "service_new_button_submit",
                            className="btn btn-outline-primary")
            ]),
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

def delete_img(n_clicks, children):
    if n_clicks <= 0:
        return children
    '''
    children = img_text_children
    delete_children = []
    for child in children:
        print(child)
        row0 = child.children[0]
        del_button = row0.children[0].children[0]
        #upload_ctl = row0.children[1].children[0]
        #row1 = child.children[1]
        #img_ctrl = row1.children[0].children[0]
        if del_button.id == delete_button_id:
            delete_children.append(child)
    for item in delete_children:
        print(item)
    '''
    print(delete_button_id)
    return []
@app.callback(Output('service_new_label_message', 'children'),
              [Input('service_new_button_submit', 'n_clicks')],
              [State('service_new_imgs_and_texts', 'children')])
def create_new_service(submit_btn, imgs_texts_children):
    for item in imgs_texts_children:
        #print(item)
        pass
    return len(imgs_texts_children)


for i in range(MAX_IMG_TXT):
    section_id, delete_button_id, upload_id, img_id, = generate_id(i)
    app.callback(Output(section_id, 'children'),
                [Input(delete_button_id, 'n_clicks')],
                [State(section_id, 'children')])(delete_img)
    app.callback(Output(img_id, 'src'),
                [Input(upload_id, 'contents')])(preview_img)

app.callback(Output('major-img', 'src'),
             [Input('upload', 'contents')])(preview_img)




