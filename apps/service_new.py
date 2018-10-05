#!/usr/bin/python3
from uuid import uuid1
import dash_core_components as dcc
import dash_html_components as html
from dash.exceptions import PreventUpdate
from dash.dependencies import State, Input, Output
import gettext
from app import app
from app import app_controller
from magic_defines import (MAX_IMG_TXT, REDIRECT, SNACK_BAR,
                           CLUB_NAME, locale_d
                           )
from sd_material_ui import Snackbar
from utils import g_id
from autolink import Redirect

zh = gettext.translation("service_new", locale_d(), languages=["zh_CN"])
zh.install(True)
_ = zh.gettext


SUCCESS_CREATE = _("service created successfully")


def gen_id(name):
    # user module as name prefix
    s_id = g_id(__name__, name)
    return s_id


def generate_id(index):
    section_id = "service_new_img_section_{}".format(index)
    upload_id = 'service_new_upload_{}'.format(index)
    img_id = "service_new_img_{}".format(index)
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
    img_txt_section = html.Div(id=section_id, children=[
        html.Div(className="row align-items-center", children=[
            html.Div(className="col-sm-12", children=[
                dcc.Upload(
                    id=upload_id,
                    children=html.Div([
                        _("Drag and Drop or "),
                        html.A(_("Select a File")),
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
                             placeholder=_("Please input picture description"),
                             style={'width': '100%'},
                             className="form-control form-control-lg")
            ]),
        ]),
        html.Hr()
    ])
    return img_txt_section


snack_bar = Snackbar(id=gen_id(SNACK_BAR),
                     open=False,
                     message=_("message show here"))
auto_link = Redirect(id=gen_id(REDIRECT), href="")


def layout():
    return html.Div(children=[
        html.Label(  # service uuid
            title=str(uuid1()),
            id="service_new_uuid",
            style={"display": 'none'}
        ),
        html.Div(className="row", children=[
            html.Div(className="col-sm-12", children=[
                html.Label(_("Title:"))
            ]),
        ]),
        html.Div(className="row", children=[
            html.Div(className="col-sm-12", children=[
                dcc.Input(id="service_new_title",
                          placeholder=_("Please input title"),
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
                dcc.Textarea(id="service_new_description",
                             placeholder=_("Please input service description"),
                             style={'width': '100%'},
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
                dcc.Input(id="service_new_price",
                          placeholder=_("Please input service price"),
                          style={'width': '100%'},
                          type="number",
                          value=500,
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
                dcc.Input(id="service_new_discount",
                          placeholder=_("Please input service price"),
                          style={'width': '100%'},
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
                html.Label(_("major picture:"))
            ]),
        ]),
        html.Div(className="row", children=[
            html.Div(className="col-sm-12", children=[
                dcc.Upload(
                    id='service_new_upload_major',
                    children=html.Div([
                        _("Drag and Drop or "),
                        html.A(_("Select a File")),
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
                html.Img(id="service_new_img_major",
                         src="",
                         className="img-fluid"),
            ]),
        ]),
        html.Div(className="row", children=[
            html.Div(className="col-sm-6", children=[
                dcc.Checklist(
                    id="service_new_checklist_online",
                    options=[
                        {'label': _("online"), 'value': 'online'},
                    ],
                    values=['online']
                )
            ]),
            html.Div(className="col-sm-6", children=[
                dcc.Checklist(
                    id="service_new_checklist_headline",
                    options=[
                        {'label': _("headline"), 'value': 'headline'},
                    ],
                    values=['headline']
                )
            ]),
        ]),
        html.Div(id="service_new_imgs_and_texts", children=[
            generate_new_img_txt(i) for i in range(MAX_IMG_TXT)
        ]),
        html.Hr(),
        snack_bar,
        auto_link,
        html.A(className="float", children=[
            html.Button(_("Submit"),
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
state_list.extend([State(generate_img_id(i), 'src')
                   for i in range(MAX_IMG_TXT)])
state_list.extend([State(generate_txt_id(i), 'value')
                   for i in range(MAX_IMG_TXT)])


@app.callback(Output(gen_id(REDIRECT), 'href'),
              [Input(gen_id(SNACK_BAR), 'message')],
              [State(gen_id(SNACK_BAR), 'open')])
def redirect_to_list(msg, open_snack_bar):
    if msg == SUCCESS_CREATE and open_snack_bar is False:
        return "/service/list"
    raise PreventUpdate()


@app.callback(Output(gen_id(SNACK_BAR), 'open'),
              [Input(gen_id(SNACK_BAR), 'message')])
def show_message(msg):
    if msg:
        return True
    else:
        return False


@app.callback(Output(gen_id(SNACK_BAR), 'message'),
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
        raise PreventUpdate()

    assert(service_id)
    if not title:
        return _("please input title")

    if not description:
        return _("please input description")

    if not img_major_src:
        return _("please choose major image")

    # save image and txt to files
    img_list = img_txt[:MAX_IMG_TXT]
    txt_list = img_txt[MAX_IMG_TXT:]
    service_dict = {
        "id": service_id,
        "name": title,
        "description": description,
        "price": price,
        "discount": discount,
        "sub_services": "",
        "active": bool(online),
        "slide": bool(headline)
    }
    app_controller.create_club_service(CLUB_NAME,
                                       service_dict,
                                       img_major_src,
                                       img_list,
                                       txt_list)
    return _("service created successfully")


for i in range(MAX_IMG_TXT):
    section_id, upload_id, img_id, txt_id = generate_id(i)
    app.callback(Output(img_id, 'src'),
                 [Input(upload_id, 'contents')])(preview_img)

app.callback(Output('service_new_img_major', 'src'),
             [Input('service_new_upload_major', 'contents')])(preview_img)
