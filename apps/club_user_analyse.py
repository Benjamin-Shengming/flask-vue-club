#!/usr/bin/python3
import json
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import State, Input, Output
from app import app_controller, app
import coloredlogs, logging
import gettext

from magic_defines import *
from utils import *

logger = logging.getLogger(__name__)
coloredlogs.install(level='DEBUG', logger=logger)



zh = gettext.translation("club_user_analyse", locale_d(), languages=["zh_cn"])
zh.install(True)
_ = zh.gettext


MONEY_PIE = "money-pie"
QUAN_PIE = "quantity-pie"

def gen_id(name):
    # user module as name prefix
    s_id = g_id(__name__, name)
    return s_id

def get_user_quantity_and_value():
    all_users = app_controller.get_club_user_list(CLUB_NAME)
    label=[]
    quantity = []
    value = []
    for user in all_users:
        label.append(user.email)
        quantity.append(len(user.orders))
        value.append(user.total_order_value())

    return label, quantity, value


def generate_client_card(user):
  return html.Div(className="card", children=[
        html.Div(str(user.id), className="card-header"),
        html.Div(className="card-body", children=[
            html.Div(_("Email:") + str(user.email) if user.email else _("Email:")),
            html.Div(_("Tel:") + str(user.tel) if user.tel else _("Tel")),
            html.Div(_("Activate code:") + str(user.activate_code) if user.activate_code else _("Activate Code")),
        ]),
        html.Hr()
     ])



def generate_layout():
    labels, quantities, values = get_user_quantity_and_value()
    data_quantity = [
        {
            'labels':labels,
            'values': quantities,
            'type': 'pie',
        },
    ]

    data_value = [{
        'labels':labels,
        'values': values,
        'type': 'pie',
        }]

    return html.Div([
        html.Div(style={"display": "none"}, children=[
        ]),
        html.Div(_("service value percentage")),
        dcc.Graph(id=gen_id(MONEY_PIE),
                  figure={
                    'data': data_value,
                    'layout': {
                        'margin': {
                            'l': 30,
                            'r': 0,
                            'b': 30,
                            't': 0
                        }
                    }
                    }
                  ),
        html.Div(id=gen_id("view-user-money"), children=[""]),
        html.Hr(),
        html.Div(_("service quantity percentage")),
        dcc.Graph(id=gen_id(QUAN_PIE),
                  figure={
                    'data': data_quantity,
                    'layout': {
                        'margin': {
                            'l': 30,
                            'r': 0,
                            'b': 30,
                            't': 0
                        }
                    },
                  }),
        html.Div(id=gen_id("view-user-quantity"), children=[""]),
        html.Hr(),
    ])

def layout():
    return generate_layout()



def show_chart_selected(clickData):
    logger.debug(clickData)
    if not clickData or not clickData['points']:
        return [""]

    tel_or_email = clickData['points'][0]['label']
    logger.debug(tel_or_email)
    user = app_controller.get_club_user_by_email_or_tel(CLUB_NAME, tel_or_email)
    if not user:
        return [""]
    return [generate_client_card(user)]

@app.callback(Output(gen_id("view-user-money"), 'children'),
              [Input(gen_id(MONEY_PIE), 'clickData')])
def show_money_select(clickData):
    return show_chart_selected(clickData)

@app.callback(Output(gen_id("view-user-quantity"), 'children'),
              [Input(gen_id(QUAN_PIE), 'clickData')])
def show_quantity_select(clickData):
    return show_chart_selected(clickData)

