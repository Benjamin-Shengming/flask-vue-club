#!/usr/bin/python3
from collections import OrderedDict
from uuid import uuid1
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Event, State, Input, Output
from pprint import pprint
from app import app


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
                html.Img(id="major-img",src=""),
            ]),
    ]),
    html.Hr()
])


@app.callback(Output('major-img', 'src'),
              [Input('upload', 'contents')])
def preview_major(contents):
    if contents is not None:
        content_type, content_string = contents.split(',')
        if 'image' in content_type:
            return contents
        else:
            return ""
