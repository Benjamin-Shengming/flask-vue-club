#!/usr/bin/python

import os 
import sys
from flask import render_template, redirect, request, abort, Response, url_for, send_from_directory
from flask_login import login_user, login_required, logout_user, current_user 
#from flask_restplus import Namespace, Resource, fields 
from .forms import *
from utils import caller_info 
from flask_bootstrap import Bootstrap
from flask_babel import Babel, lazy_gettext as _ 

import coloredlogs, logging
from .. import app_controller 
from .. import login_manager
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

logger = logging.getLogger(__name__)
coloredlogs.install(level='DEBUG', logger=logger)

def page_resp(page):
    resp = Response(page, mimetype='text/html')
    return resp

view_pages= Namespace('view_pages', description='auth pages')

@login_manager.user_loader
def load_user(id):
    return app_controller.get_user_by_id(id)

@view_pages.route('<club_name>/signup')
class SignUpPage(Resource):
    def get(self, club_name):
        logger.debug(caller_info())
        logger.debug(current_user)
        club = app_controller.get_club_by_name(club_name)
        if not current_user.is_anonymous:
            return redirect('{}/index'.format(club_name))

        form = RegisterForm()
        flash(_("Please input email and password!"))
        page = render_template('signup.html', form=form, club=club)
        return page_resp(page)

    def post(self, club_name):
        form = LoginForm()
        form = RegisterForm()
        user = app_controller.get_club_user_by_email(club_name, form.data['email'])
        club = app_controller.get_club_by_name(club_name)
        # there is a user has the same email
        if user:
            page = render_template('signup.html', form=form, club=club)
            return page_resp(page)

        user = app_controller.create_club_user(club_name, form.data)
        login_user(user, remember=True)
        return redirect('{}/index'.format(club_name))

@view_pages.route('<club_name>/logout')
class LogoutPage(Resource):
    @view_pages.doc("Logout club")
    def get(self, club_name):
        logger.debug(caller_info())
        logout_user()
        logger.debug(current_user)
        return redirect('{}/index'.format(club_name))

    def post(self, club_name):
        logger.debug(caller_info())
        logout_user()
        logger.debug(current_user)
        return redirect('{}/index'.format(club_name))

@view_pages.route('<club_name>/login')
class LoginPage(Resource):
    def get(self, club_name):
        logger.debug(caller_info())
        logger.debug(current_user)
        club = app_controller.get_club_by_name(club_name)
        if not current_user.is_anonymous:
            return redirect('/{}/index'.format(club_name))

        form = LoginForm()
        resp = Response(render_template('login.html',form=form, club=club), mimetype='text/html')
        return resp

    def post(self, club_name):
        form = LoginForm()
        club = app_controller.get_club_by_name(club_name)
        user = app_controller.verify_club_user(club_name, form.data)
        if user:
            login_user(user, remember=True)
            return redirect('/{}/index'.format(club_name))
        else:
            page = render_template('login.html', form=form, club_name=club)
            return page_resp(page)

@view_pages.route('<club_name>/admin')
class AdminPage(Resource):
    def _return_render_page(self, club_name):
        logger.debug(current_user)
        club = app_controller.get_club_by_name(club_name)
        page = render_template('admin.html', club=club, user=current_user)
        return page_resp(page) 

    def get(self, club_name):
        logger.debug(caller_info())
        return self._return_render_page(club_name)

    def post(self, club_name):
        logger.debug(caller_info())
        return self._return_render_page(club_name)

@view_pages.route('<club_name>/admin/<sub_page>')
class AdminSubPage(Resource):
    def _return_render_page(self, club_name, sub_page):
        logger.debug(current_user)
        club = app_controller.get_club_by_name(club_name)
        page = render_template('admin-subpages/{}'.format(sub_page), club=club, user=current_user)
        return page_resp(page) 

    def get(self, club_name, sub_page):
        logger.debug(caller_info())
        return self._return_render_page(club_name, sub_page)

    def post(self, club_name, sub_page):
        logger.debug(caller_info())
        return self._return_render_page(club_name, sub_page)

