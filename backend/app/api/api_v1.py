#!/usr/bin/python
import os
import six 
import coloredlogs, logging
from marshmallow import fields, Schema
from flask_apispec import ResourceMeta, Ref, doc, marshal_with, use_kwargs
from flask import abort, request, send_from_directory , Response, Blueprint
from werkzeug import secure_filename
from utils import *
from flask_cors import CORS 

from . import app_controller
from .. import app 
from .. import docs 

logger = logging.getLogger(__name__)
coloredlogs.install(level='DEBUG', logger=logger)

API_NAME = 'api_v1'
API_PREFIX = '/' + API_NAME
api_v1_blueprint = Blueprint(API_NAME, API_NAME)
api = api_v1_blueprint

CORS(api_v1_blueprint)

class UrlSchema(Schema):
    class Meta:
        fields = ['url']

@api.route('/filestore/<club_name>/service/<id>/<filename>')
def get_service_file(club_name, id, filename):
    return send_from_directory(app_controller.get_filestore_service(id), filename)

@api.route('/filestore/<club_name>/service/<service_id>', methods=['POST'])
@doc(params={'club_name': {'description': 'club name which provide the service'}})
@doc(params={'service_id': {'description': 'unique id for service'}})
@marshal_with(UrlSchema(many=True))
def post_service_file(club_name, service_id):
    logger.debug("called service upload files: "+ str(service_id))
    # Get the name of the uploaded files
    logger.debug(request.files)
    uploaded_files = request.files
    logger.debug(uploaded_files)
    filenames = []
    for key, value in uploaded_files.items():
        logger.debug(key)
        logger.debug(value)
        if (not app_controller.allow_file(value.filename)):
            continue
        # Make the filename safe, remove unsupported chars
        filename = secure_filename(value.filename)
        # Move the file form the temporal folder to the upload
        # folder we setup
        file_path = os.path.join(app_controller.get_filestore_service(club_name, service_id), filename)
        value.save(file_path)
        # Save the filename into a list, we'll use it later
        filenames.append({'url': "/filestore/service/" + service_id + "/" + filename})
    return filenames


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

@api.route('/<club_name>/service', methods=['GET', 'POST'])
@marshal_with(ServiceSchema(many=True))
def service_op(club_name): 
    if request.method == 'GET':
        return app_controller.get_club_service_list(club_name)
    elif request.method == 'POST':
        logger.debug("calling create an new service")
        logger.debug(request.get_json())
        return app_controller.create_club_service(club_name, request.get_json())
        

# register api and doc
app.register_blueprint(api_v1_blueprint, url_prefix=API_PREFIX)
docs.register(get_service_file, blueprint='api_v1')
docs.register(post_service_file, blueprint='api_v1')

'''
api = Namespace('api_v1', description='API version 1')

def get_payload():
    return api.apis[0].payload

def raise_error(resp_except):
    abort(resp_except.http_code, resp_except.message)


user_model = api.model('User', {
    'email': fields.String(required=True, description="user's email"),
    'tel': fields.String(description="user's telephone number"),
    'roles':fields.List(fields.String, description="user roles"),
    'password':fields.String(required=False, description= "user's password")
})

@api.route('/<club_name>/user')
class UserList(Resource):
    @api.doc('List all users')
    @api.marshal_list_with(user_model)
    def get(self, club_name):
        try:
            return app_controller.get_club_user_list(club_name)
        except RespExcept as e:
            raise_error(e)

    @api.expect(user_model)
    @api.marshal_with(user_model)
    def post(self, club_name):
        try:
            return app_controller.create_club_user(club_name, get_payload())
        except RespExcept as e:
            raise_error(e)

@api.route('/<club_name>/user/<user_email>')
@api.param('club_name', 'the name of a club')
@api.param('user_email', "The user email")
@api.response(404, 'user not found')
class User(Resource):
    @api.doc('get one user information')
    @api.marshal_with(user_model)
    def get(self, club_name, user_email):
        return app_controller.get_club_user_by_email(club_name, user_email)

    @api.expect(user_model)
    @api.marshal_with(user_model)
    def put(self, club_name, user_email):
        return app_controller.update_user(club_name, user_email, get_payload())

    def delete(self, club_name, user_email):
        return app_controller.delete_club_user_by_email(club_name, user_email)

club_model = api.model('club', {
    'name': fields.String(required=True, description="user's email"),
    'description': fields.String(required=True, description="user's email"),
})

@api.route('/club')
class ClubList(Resource):
    @api.doc('List all clubs')
    @api.marshal_list_with(club_model)
    def get(self):
        try:
            return app_controller.get_club_list()
        except RespExcept as e:
            raise_error(e)

    @api.expect(club_model)
    @api.marshal_with(club_model)
    def post(self):
        try:
            return app_controller.create_club(get_payload())
        except RespExcept as e:
            raise_error(e)

@api.route('/club/<club_name>')
@api.param('club_name', 'the name of a club')
@api.response(404, 'club not found')
class Club(Resource):
    @api.doc('get one club information')
    @api.marshal_with(club_model)
    def get(self, club_name):
        try:
            return app_controller.get_club_by_name(club_name)
        except RespExcept as e:
            raise_error(e)

    def delete(self, club_name):
        try:
            return app_controller.delete_club_by_name(club_name)
        except RespExcept as e:
            raise_error(e)

    @api.expect(club_model)
    @api.marshal_with(club_model)
    def put(self, club_name):
        try:
            return app_controller.update_club(club_name, get_payload())
        except RespExcept as e:
            raise_error(e)

role_model = api.model('role', {
    'name': fields.String(required=True, description="user's email"),
    'description': fields.String(description="descripion of a role"),
})
@api.route('/<club_name>/role')
class RoleList(Resource):
    @api.doc('List all roles')
    @api.marshal_list_with(role_model)
    def get(self, club_name):
        return app_controller.get_club_role_list(club_name)

    @api.expect(role_model)
    @api.marshal_with(role_model)
    def post(self, club_name):
        return app_controller.create_club_role(club_name, get_payload())

@api.route('/<club_name>/role/<role_name>')
@api.param('club_name', 'the name of a club')
@api.response(404, 'club not found')
class Role(Resource):
    @api.doc('get one role')
    @api.marshal_with(role_model)
    def get(self, club_name, role_name):
        return app_controller.get_club_role_by_name(club_name, role_name)

    def delete(self, club_name, role_name):
        return app_controller.delete_club_role_by_name(club_name, role_name)
    
    @api.expect(club_model)
    @api.marshal_with(club_model)
    def put(self, club_name, role_name):
        return app_controller.update_club_role(club_name, role_name, get_payload())




'''