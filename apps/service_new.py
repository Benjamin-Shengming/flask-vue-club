#!/usr/bin/python3
from collections import OrderedDict
from uuid import uuid1
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Event, State, Input, Output
from pprint import pprint



layout = html.Div(className="row", children=[
        html.Div(className="col-sm-2", children=[
            html.Label("Service Title:")
        ]),
        html.Div(className="col-sm-10", children=[
            dcc.Input(id=str(uuid1()),
                       placeholder="Please input title",
                       className="form-control form-control-lg")
        ])
])



@app.callback(
    Output('root', 'children'),
    events=[Event('add-div', 'click')],
)



