#!/usr/bin/python
import os
from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from random import randint
from models import AppModel
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimestampSigner, Serializer, URLSafeSerializer, URLSafeTimedSerializer
from json import loads
from magic_defines import *
import coloredlogs, logging
from datetime import datetime, timedelta
import jwt
from utils import caller_info, RespExcept, CodeNotMatch
from email_smtp import EmailClientSMTP
from flask_apispec import ResourceMeta, Ref, doc, marshal_with, use_kwargs
logger = logging.getLogger(__name__)
coloredlogs.install(level='DEBUG', logger=logger)
from marshmallow import fields, Schema
class ServiceSchema(Schema):
    class Meta:
        fields = ['id',
                  'name',
                  'description',
                  'price',
                  'discount',
                  'major_pic',
                  'pic_and_text',
                  'active',
                  'slide']

class AppController(object):
    def __init__(self):
        self.db_model = AppModel()

    def save(self, obj):
        self.db_model.save(obj)

    # club related functions
    def get_club_list(self):
        user_list = self.db_model.get_club_list()
        return user_list

    def create_club(self, club_data):
        club = self.db_model.create_club(club_data)
        return club

    def delete_club_by_name(self, club_name):
        return self.db_model.delete_club_by_name(club_name)

    def update_club(self, club_name, club_data):
        club = self.db_model.update_club(club_name, club_data)
        return club

    def get_club_by_name(self, club_name):
        return self.db_model.get_club_by_name(club_name)

    # user related functions
    def get_user_by_id(self, user_id):
        return self.db_model.get_user_by_id(user_id)


    def get_club_user_list(self, club_name):
        user_list = self.db_model.get_club_user_list(club_name)
        return user_list

    def _decode_user_jwt(self, encoded_jwt):
        payload = jwt.decode(encoded_jwt, JWT_SECRET_KEY, JWT_ALGORITHM)
        return payload

    def get_club_user_by_jwt(self, club_name, encoded_jwt):
        u = None
        try:
            user_dict = self._decode_user_jwt(encoded_jwt)
            u = self.get_club_user_by_id(club_name, user_dict['user_id'])
        except:
            pass
        return u

    def generate_user_jwt(self, club_name, user):
        payload = {
            'user_id': user.id,
            'club_name': club_name,
            'exp':datetime.utcnow() + timedelta(hours=JWT_EXP_DELTA_HOURS)
        }
        jwt_token = jwt.encode(payload, JWT_SECRET_KEY, JWT_ALGORITHM)
        return jwt_token


    def activate_club_user_by_jwt(self, club_name, encoded_jwt, code):
        user = self.get_club_user_by_jwt(club_name, encoded_jwt)
        if not user:
            raise LoginExpireMsg()
        user.activate_code(code)
        self.db_model.save(user)


    def activate_club_user_by_email(self, club_name, email, activate_code):
        '''
        confirm_serializer = URLSafeTimedSerializer(SECRET_KEY)
        email = confirm_serializer.loads(token, salt=EMAIL_SALT, max_age=36000)
        '''
        user = self.get_club_user_by_email(club_name, email)
        if user.activate_code == activate_code:
            user.email_confirmed = True
            self.db_model._add_commit(user)
        else:
            raise RespExcept("Activation code is not right!")
        return user

    def resend_active_code_by_email(self, club_name, email_address):
        logger.debug("resend link")
        logger.debug("club_name")
        logger.debug(email_address)
        user = self.db_model.get_club_user_by_email(club_name, email_address)
        if not user:
            raise RespExcept("User does not exist")
        if user.email_confirmed:
            raise RespExcept("user already activated!")
        code = self.generate_club_user_activate_code(club_name, user)
        club = user.club
        EmailClientSMTP(club.smtp_server,
                        club.smtp_port,
                        club.smtp_encryption,
                        club.email,
                        club.email_pwd).send_email(
                            user.email,
                            subject="activate account",
                            body=code)

    def generate_club_user_activate_code(self, club_name, user):
        code = ""
        length = 5
        for i in range(0, length):
            code += str(randint(0, 9))
        logger.debug(code)
        user.activate_code = code
        self.db_model._add_commit(user)
        return code
        '''
        confirm_serializer = URLSafeTimedSerializer(SECRET_KEY)
        token = confirm_serializer.dumps(user.email, salt=EMAIL_SALT)
        return ("/{}/email/activate/{}".format(club_name, token))
        '''
    def create_club_user(self, club_name, user_data):
        logger.debug(user_data)
        if not user_data.get('roles', None):
            # by default, the role is user
            user_data['roles'] = ['user']
        new_user = self.db_model.create_club_user(club_name ,user_data)
        return new_user

    def get_club_user_by_id(self, club_name, user_id):
        user = self.db_model.get_club_user_by_id(club_name, user_id);
        return user

    def get_club_user_by_email(self, club_name, user_email):
        user = self.db_model.get_club_user_by_email(club_name, user_email)
        return  user

    def verify_club_user(self, club_name, user_data):
        user = self.db_model.verify_club_user(club_name, user_data)
        return  user

    def delete_club_user_by_email(self, club_name, user_email):
        return self.db_model.delete_club_user(club_name, user_email)

    def update_club_user(self, club_name, user_email, user_data):
        return self.update_club_user(club_name, user_email, user_data)

    # role realted functions
    def get_club_role_list(self, club_name):
        return self.db_model.get_club_role_list(club_name)

    def get_club_role(self, club_name, role_name):
        return self.db_model.get_club_role_by_name(club_name, role_name)

    def create_club_role(self, club_name, role_data):
        return self.db_model.create_club_role(club_name, role_data)

    def update_club_role(self, club_name, role_name, role_data):
        return self.db_model.update_club_role(club_name, role_name, role_data)

    def delete_club_role_by_name(self, club_name, role_name):
        return self.db_model.delete_club_role_by_name(club_name, role_name)


    def allow_file(self, filename):
      allow_ext = set(['txt','png', 'jpg', 'jpeg', 'gif'])
      return '.' in filename and filename.rsplit('.', 1)[1] in allow_ext

    # service related functions
    def create_club_service(self, club_name, service_data):
        logger.debug(service_data)
        return self.db_model.create_club_service(club_name, service_data)

    def update_club_service(self, club_name, service_id, service_data):
        return self.db_model.update_club_service(club_name, service_id, service_data)

    def get_club_service_list(self, club_name):
        logger.debug(club_name)
        return self.db_model.get_club_service_list(club_name)

    def get_club_service(self, club_name, service_id):
        return self.db_model.get_club_service(club_name, service_id)

    def get_club_headline_service(self, club_name):
        return self.db_model.get_club_headline_service(club_name)

    def get_club_service_paginate_date(self, club_name, start, numbers=20):
        return self.db_model.get_club_service_paginate_date(club_name, start, numbers)

    def delete_club_service(self, club_name, service_id):
        return self.db_model.delete_club_service(club_name, service_id)

    def create_club_user_order(self, club_name, jwt, quantity_service):
        if len(quantity_service)<=0:
            return
        user = self.get_club_user_by_jwt(club_name, jwt)
        order = self.db_model.create_club_user_order(club_name,
                                                     user,
                                                     quantity_service)
        if order:
            self.save(order)
        return order

    def get_club_order_by_id(self, order_id):
        return self.db_model.get_order_by_id(order_id)


    # check one service has special keywords
    def _service_has_keyword(self, service, key_words):
        #check name
        for key in key_words:
            if key in service.name:
                return True
        #check description
        for key in key_words:
            if key in service.description:
                return True
        return False
    def service_to_article(self, service, club_name):
        article = {}
        article['title'] = service.name
        article['description'] = service.description
        article['url'] = "/{}".format(club_name)
        article['image'] = "/filestore/{}/service/{}/{}".format(club_name, service.id, service.major_pic)
        return article
    # given a set of keywords and search the service contains the key word
    # if keyword is empty, just return most important
    def search_club_service_article(self, club_name, key_words):
        services = self.get_club_service_list(club_name)
        ret = [item for item in services if self._service_has_keyword(item , key_words)]
        return [self.service_to_article(item, club_name) for item in ret]

