#!/usr/bin/python3
from collections import OrderedDict
from uuid import uuid1
import base64
import dash
import json
import dash_core_components as dcc
import dash_html_components as html
from dash.exceptions import PreventUpdate
from dash.dependencies import Event, State, Input, Output
from pprint import pprint
from app import app
from app import app_controller
import filestore
from magic_defines import *
import local_storage

import coloredlogs, logging
logger = logging.getLogger(__name__)
coloredlogs.install(level='DEBUG', logger=logger)

'''
<div class="container">
	<div class="row">
		<h2>Create your snippet's HTML, CSS and Javascript in the editor tabs</h2>


       <div class="col-md-7 ">

<div class="panel panel-default">
  <div class="panel-heading">  <h4 >User Profile</h4></div>
   <div class="panel-body">

    <div class="box box-info">

            <div class="box-body">
                     <div class="col-sm-6">
                     <div  align="center"> <img alt="User Pic" src="https://x1.xingassets.com/assets/frontend_minified/img/users/nobody_m.original.jpg" id="profile-image1" class="img-circle img-responsive">

                <input id="profile-image-upload" class="hidden" type="file">
<div style="color:#999;" >click here to change profile image</div>
                <!--Upload Image Js And Css-->







                     </div>

              <br>

              <!-- /input-group -->
            </div>
            <div class="col-sm-6">
            <h4 style="color:#00b1b1;">Prasad Shankar Huddedar </h4></span>
              <span><p>Aspirant</p></span>
            </div>
            <div class="clearfix"></div>
            <hr style="margin:5px 0 5px 0;">


<div class="col-sm-5 col-xs-6 tital " >First Name:</div><div class="col-sm-7 col-xs-6 ">Prasad</div>
     <div class="clearfix"></div>
<div class="bot-border"></div>

<div class="col-sm-5 col-xs-6 tital " >Middle Name:</div><div class="col-sm-7"> Shankar</div>
  <div class="clearfix"></div>
<div class="bot-border"></div>

<div class="col-sm-5 col-xs-6 tital " >Last Name:</div><div class="col-sm-7"> Huddedar</div>
  <div class="clearfix"></div>
<div class="bot-border"></div>

<div class="col-sm-5 col-xs-6 tital " >Date Of Joining:</div><div class="col-sm-7">15 Jun 2016</div>

  <div class="clearfix"></div>
<div class="bot-border"></div>

<div class="col-sm-5 col-xs-6 tital " >Date Of Birth:</div><div class="col-sm-7">11 Jun 1998</div>

  <div class="clearfix"></div>
<div class="bot-border"></div>

<div class="col-sm-5 col-xs-6 tital " >Place Of Birth:</div><div class="col-sm-7">Shirdi</div>

 <div class="clearfix"></div>
<div class="bot-border"></div>

<div class="col-sm-5 col-xs-6 tital " >Nationality:</div><div class="col-sm-7">Indian</div>

 <div class="clearfix"></div>
<div class="bot-border"></div>

<div class="col-sm-5 col-xs-6 tital " >Relition:</div><div class="col-sm-7">Hindu</div>


            <!-- /.box-body -->
          </div>
          <!-- /.box -->

        </div>


    </div>
    </div>
</div>
'''

profile_title_row = html.Div(className="row", children=[
                html.Div(className="col-md-3"),
                html.Div(className="col-md-6", children=[
                    html.H2("User details"),
                    html.Hr()
                ])
            ])

email_row = html.Div(className="row", children=[
                html.Div(className="col-md-3 field-label-responsive", children=[
                    html.Label("E-Mail Address", htmlFor="email")
                ]),
                html.Div(className="col-md-6", children=[
                    html.Div(className="form-group", children=[
                        html.Div(className="input-group mb-2 mr-sm-2 mb-sm-0", children=[
                            html.Div(className="input-group-addon", style={"width": "2.6rem"}, children=[
                                html.I(className="fa fa-at")
                            ]),
                            dcc.Input(type="text", name="email",className="form-control",id="register-email", placeholder="you@example.com",required="true", autofocus="true")
                        ])
                    ])
                ]),
                html.Div(className="col-md-3", children=[
                    html.Div(className="form-control-feedback", children=[
                        html.Span(className="text-danger align-middle")
                    ])
                ])
            ])


def layout():
    logger.debug("profile layout")
    return html.Div(className="container", children=[
        profile_title_row,
        email_row
    ])

