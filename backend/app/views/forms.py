#!/usr/bin/python

from wtforms import StringField, PasswordField, BooleanField, Label
from flask_wtf import FlaskForm 
from wtforms.validators import InputRequired, Email, Length, EqualTo
from . import app_controller
from flask import flash
from flask_babel import lazy_gettext as _
class LoginForm(FlaskForm):
    email = StringField(_('Email'), validators=[InputRequired(), Length(min=2, max=200), Email("Invalide email!")])
    password = PasswordField(_('Password'), validators=[InputRequired(), Length(min=8, max=80)])

class RegisterForm(FlaskForm):
    email = StringField(_('email'), 
                         validators=[InputRequired(), 
                                     Email(message=_('Invalid email')), 
                                     Length(min=2, max=50)])
    tel = StringField(_('telphone'), 
                        validators=[InputRequired(), 
                                    Length(min=8, max=15)])
    password = PasswordField(_('password'), 
                            validators=[InputRequired(), 
                                        Length(min=8, max=80),
                                        EqualTo(_('confirm_password'), message=_("Passwords must match"))
                                        ])
    confirm_password = PasswordField(_('confirm'), 
                                      validators=[InputRequired(), 
                                                  Length(min=8, max=80)])
