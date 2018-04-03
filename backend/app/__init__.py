#!/usr/bin/python
import os 
import sys
from flask import Flask
from werkzeug.contrib.fixers import ProxyFix
from flask_bootstrap import Bootstrap
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_babel import Babel 
from flask_cors import CORS
from flask_apispec import FlaskApiSpec
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)
from magic_defines import * 

app = Flask(__name__,
            static_folder = "../../dist/static",
            template_folder = "../../dist")
app.wsgi_app = ProxyFix(app.wsgi_app)

app.config['SECRET_KEY'] = SECRET_KEY 
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER 
app.config['JWT_SECRET_KEY'] = JWT_SECRET_KEY  

app.config['BABEL_DEFAULT_LOCALE'] = 'zh_Hans_CN'

babel = Babel(app)
cors =CORS(app)
docs = FlaskApiSpec(app)

# create jwt 
jwt = JWTManager(app)

# create controller object, the central point 
from .controller import AppController
app_controller = AppController()

from . import api
