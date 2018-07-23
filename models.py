#!/usr/bin/python
import os
import shutil
import datetime
from sqlalchemy import UniqueConstraint, ForeignKey, create_engine, Column, Integer, String, Table, DateTime, Boolean
from sqlalchemy.orm import relationship, scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flask_babel import lazy_gettext as _
from utils import *
import coloredlogs, logging
import filestore
from uuid import uuid1
from magic_defines import *

logger = logging.getLogger(__name__)
coloredlogs.install(level='DEBUG', logger=logger)

engine = create_engine('sqlite:////home/ubuntu/test.db', convert_unicode=True)

db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()

association_user_role = Table('user_role', Base.metadata,
    Column('user_id', Integer, ForeignKey("user.id", ondelete='CASCADE')),
    Column('role_id', Integer, ForeignKey("role.id", ondelete='CASCADE'))
)

class BaseMixin(object):
    #this method update fileds values from dict
    def from_dict(self, dict_value):
        logger.debug(dict_value)
        for key, value in dict_value.items():
            slot_attr = getattr(self, key)
            if slot_attr:
                setattr(self, key, value)

    def to_dict(self):
        dict_value = {}
        logger.debug(self.__table__.columns)
        for key in self.__table__.columns.keys():
            # remove table name
            col_name = key.split(".")[-1]
            dict_value[key] = getattr(self, col_name)
        return dict_value

    def columns(self):
        return self.__table__.columns

class User(Base, BaseMixin, UserMixin):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=False)
    tel = Column(String, unique=False)
    password_hash = Column(String, nullable=False)
    email_confirmed = Column(Boolean, default=False)
    tel_confirmed = Column(Boolean, default=False)
    activate_code = Column(String)
    last_active_time = Column(DateTime, default=datetime.datetime.utcnow)

    club_id = Column(Integer, ForeignKey('club.id', ondelete='CASCADE'), nullable=False)
    __table_args__ = (UniqueConstraint('email', 'club_id'),)
    roles = relationship("Role",
                         secondary=association_user_role,
                         back_populates="users")
    orders = relationship("Order", backref="user", cascade="all, delete", order_by="desc(Order.time)")

    def total_order_value(self):
        total = 0
        for o in self.orders:
            total +=  o.total_price()
        return total

    def is_active(self):
        return False if self.activate_code else True

    def activate(self, code):
        if code == self.activate_code:
            self.activate_code = ""

    def update_active_time(self):
        self.last_active_time = datetime.datetime.now()


class Club(Base, BaseMixin):
    __tablename__ = 'club'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    description = Column(String)
    smtp_server = Column(String)
    smtp_port = Column(String)
    smtp_encryption = Column(String)
    email = Column(String, unique=False)
    email_pwd = Column(String, unique=False)
    tel = Column(String, unique=False)
    # relationship
    users = relationship("User", backref="club")
    roles = relationship("Role", backref="club")
    services = relationship("Service", backref="club", order_by="desc(Service.last_update_time)")
    orders = relationship("Order", backref='club', order_by="desc(Order.time)")

class HistoryActivity(Base, BaseMixin):
    __tablename__ = 'historyactivity'
    id = Column(Integer, primary_key=True)
    label = Column(String, unique=False, nullable=False)
    value = Column(String, nullable=False)
    time = Column(DateTime, default=datetime.datetime.utcnow)

    def increase_value_as_int(self):
        self.value = int(self.value) + 1
        self.time = datetime.datetime.now()

    def change_value(self, new_value):
        self.value = new_value
        self.time = datetime.datetime.now()
    def utc_time(self):
        return self.time

    def local_time(self):
        return utc_2_local(self.time)

class Role(Base, BaseMixin):
    __tablename__ = 'role'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=False)
    description = Column(String, nullable=False)
    club_id = Column(Integer, ForeignKey('club.id'), nullable=False)
    __table_args__ = (UniqueConstraint('name', 'club_id'),)
    users = relationship(
        "User",
        secondary=association_user_role,
        back_populates="roles"
    )

class Service(Base, BaseMixin):
    __tablename__ = 'service'
    id = Column(String, primary_key=True) # service uuid
    name = Column(String, nullable=False) # title of a service
    description = Column(String) #  summary text of service
    price = Column(Integer, nullable=False)
    discount = Column(Integer, nullable=False, default=20)
    last_update_time = Column(DateTime, default=datetime.datetime.utcnow)
    sub_services = Column(String) # a list of sub services
    active = Column(Boolean, default=True) #onine or offline
    slide = Column(Boolean, default=False)  # show on slding headline
    user_view = Column(Integer, default=0)
    user_view_time = Column(DateTime, default=datetime.datetime.utcnow)

    # link to club
    club_id = Column(Integer, ForeignKey("club.id", ondelete='CASCADE'), nullable=False)
    __table_args__ = (UniqueConstraint('name', 'club_id'),)

    def discount_percent_str(self):
        return "{}%".format(self.discount)

    def final_price(self):
        return int(self.price * self.discount / 100)

    def calc_price(self, quantity):
        return self.final_price() * quantity

    def is_active(self):
        return self.active

    def get_img_link(self, index):
        return filestore.get_service_img_link(self.id, index)

    def increase_user_view_times(self):
        self.user_view += 1
        self.user_view_time = datetime.datetime.utcnow()

class Order(Base, BaseMixin):
    __tablename__ = 'order'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    club_id = Column(Integer, ForeignKey('club.id'), nullable=False)
    paid = Column(Integer)
    time = Column(DateTime, default=datetime.datetime.utcnow)  # when this order generated
    details = relationship("OrderDetail",cascade="all, delete",backref="order")

    def total_price(self):
        total = 0
        for item in self.details:
            total += item.calc_price()
        return total

    def between_time(self, start_time=None, end_time=None): # inclusive start utc time
        ret = True
        if start_time:
            ret = ret and (self.time >= start_time)
        if end_time:
            ret = ret and (self.time < end_time)
        return ret


class OrderDetail(Base, BaseMixin): # this just copy the content of Service include images
    __tablename__ = 'orderdetail'
    id = Column(String, primary_key=True) # order/service uuid
    name = Column(String, nullable=False) # title of a service
    description = Column(String) #  summary text of service
    price = Column(Integer, nullable=False)
    discount = Column(Integer, nullable=False, default=20)
    quantity = Column(Integer)
    # relation to the order
    order_id = Column(Integer, ForeignKey('order.id'), nullable=False)

    def calc_price(self):
        return self.final_price() * self.quantity

    def discount_percent_str(self):
        return "{}%".format(self.discount)

    def final_price(self):
        return int(self.price * self.discount / 100)

    def get_img_link(self, index):
        return filestore.get_service_img_link(self.id, index)

    def get_txt_content(self, index):
        return filestore.get_service_txt_content(self.id, index)


class AppModel(object):
    def __init__(self, db_session=db_session):
        self.db_session = db_session

    def _add(self, ob):
        self.db_session.add(ob)

    def _commit(self):
        self.db_session.commit()

    def _add_commit(self, ob):
        self._add(ob)
        try:
            self._commit()
        except Exception as e:
            logger.debug(str(e))
            self.db_session.rollback()
            raise e

    def save(self, obj):
        self._add_commit(obj)

    def _find_club_and_error(self, club_name):
        club = Club.query.filter_by(name=club_name).first()
        if not club:
            raise NotFound(_("could not find the club {}").format(club_name))
        return club

    # club related functions
    def get_club_list(self):
        return Club.query.all()

    def create_club(self, club_data):
        new_club = Club(**club_data)
        self._add_commit(new_club)
        return new_club

    def delete_club_by_name(self, club_name):
        Club.query.filter_by(name=club_name).delete()
        self._commit()

    def get_club_by_name(self, club_name):
        club = Club.query.filter_by(name=club_name).first()
        return club

    def update_club(self, club_name, club_data):
        old_club = self._find_club_and_error(club_name)
        old_club.from_dict(club_data)
        #logger.debug(old_club.to_dict())
        self._add_commit(old_club)
        logger.debug(old_club.to_dict())
        return old_club

    # user related functions
    def get_user_by_id(self, user_id):
        return User.query.filter_by(id=user_id).first()

    def get_club_user_list(self, club_name):
        club = self._find_club_and_error(club_name)
        user_list = User.query.filter_by(club_id=club.id).all()
        logger.debug(user_list)
        return user_list

    def get_club_user_by_id(self, club_name, user_id):
        logger.debug("get user by id")
        club = self._find_club_and_error(club_name)
        logger.debug(club.name)
        logger.debug("search id: " + str(user_id))
        user = User.query.filter_by(id=user_id, club_id=club.id).first()
        return user

    def get_club_user_by_email(self, club_name, email):
        logger.debug("get user by email")
        club = self._find_club_and_error(club_name)
        logger.debug(club.name)
        logger.debug("search email: " + email)
        user = User.query.filter_by(email=email, club_id=club.id).first()
        # logger.debug(user.email)
        return user

    def get_club_user_by_tel(self, club_name, tel):
        club = self._find_club_and_error(club_name)
        user = User.query.filter_by(tel=tel, club_id=club.id).first()
        return user

    def get_club_user_by_email_or_tel(self, club_name, tel_or_email):
        if "@" in tel_or_email:
            return self.get_club_user_by_email(club_name, tel_or_email)
        else:
            return self.get_club_user_by_tel(club_name, tel_or_email)



    def verify_club_user(self, club_name, user_data):
        club = self._find_club_and_error(club_name)
        email = user_data['email']
        if not user_data['password']:
            raise RespExcept(404, _("Please provide password!"))

        user = self.get_club_user_by_email(club_name, email)
        if not user:
            logger.debug("Can't find user!")
            return None
        # check passwd hash
        hashed_password = user_data['password']
        if user.password_hash != hashed_password:
            logger.debug("password does not match!")
            return None
        return user

    def create_club_user(self, club_name, user_dict):
        club = self._find_club_and_error(club_name)
        if user_dict['email']:
            # check whether user already exist or email, tel has been used
            user = self.get_club_user_by_email(club_name, user_dict['email'])
            if user:
                logger.debug(user.email)
                logger.debug(user.id)
                raise AlreadyExist(_("Your email address already has been used!"))
        # check password
        if not user_dict['password']:
            raise RespExcept(404, _("Please provide password!"))
        # check roles
        if not user_dict['roles']:
            raise RespExcept(404, _("Did not assign the user role"))
        role_list = []
        for role_name in user_dict['roles']:
            role = self.get_club_role_by_name(club_name, role_name)
            if role:
                role_list.append(role)
        if not role_list:
            raise RespExcept(404, _("Can't find the user roles{} in {}").format(user_dict['roles'], club_name))
        hashed_password = user_dict['password']
        new_user = User(email=user_dict['email'],
                        tel= user_dict['tel'],
                        password_hash=hashed_password)
        new_user.club = club
        new_user.roles = role_list
        self._add_commit(new_user)
        return new_user

    def update_club_user(self, club_name, user_email, user_dict):
        club = self._find_club_and_error(club_name)
        user = User.query.filter_by(club_id=club.id, email=user_email).first()
        user.from_dict(user_dict)
        self._add_commit(user)
        return user

    def delete_club_user(self, club_name, user_email):
        club = self.get_club_by_name(club_name)
        if not club:
            raise NotFound(_("Could not find the club {}").format(club_name))
        User.query.filter_by(email=user_email, club_id=club.id).delete()
        self._commit()

    def _delete_all_club_users(self, club_name):
        club = self.get_club_by_name(club_name)
        if not club:
            raise NotFound(_("Could not find the club {}").format(club_name))
        User.query.filter_by(club_id=club.id).delete()
        self._commit()

    # role related functions
    def get_club_role_list(self, club_name):
        club = self._find_club_and_error(club_name)
        return Role.query.filter_by(club_id=club.id).all()

    def create_club_role(self, club_name ,role_data):
        club = self._find_club_and_error(club_name)
        new_role = Role(**role_data)
        new_role.club_id = club.id
        self._add_commit(new_role)
        return new_role

    def update_club_role(self, club_name, role_name, role_data):
        club = self._find_club_and_error(club_name)
        role = Role.query.filter_by(name=role_name, club_id=club.id).first()
        role.from_dict(role_data)
        self._add_commit(role)
        return role

    def get_club_role_by_name(self, club_name, role_name):
        club = self._find_club_and_error(club_name)
        return Role.query.filter_by(club_id=club.id, name=role_name).first()

    def delete_club_role_by_name(self, club_name, role_name):
        club = self._find_club_and_error(club_name)
        Role.query.filter_by(club_id=club.id, name=role_name).delete()
        self._commit()

    # service related functions
    def create_club_service(self, club_name, service_data):
        club = self._find_club_and_error(club_name)
        new_service = Service(**service_data)
        new_service.club_id = club.id
        self._add_commit(new_service)

    def _create_club_order_detail(self, service, quantity):
        if not quantity:
            return
        order_detail = OrderDetail()
        order_detail.id = str(uuid1())
        order_detail.name = service.name
        order_detail.description = service.description
        order_detail.price = service.price
        order_detail.discount = service.discount
        order_detail.quantity = quantity
        filestore.copy_service_to_order_detail(service.id,
                                               order_detail.id)
        return order_detail

    def create_club_user_order(self, club_name, user, quantity_services):
        if len(quantity_services) <= 0:
            return
        order_details = []
        for item in quantity_services:
            quantity, service = item
            detail = self._create_club_order_detail(service, quantity)
            order_details.append(detail)
        if not order_details:
            return
        order = Order()
        order.user_id = user.id
        order.club_id = user.club.id
        order.paid = 0
        order.details = order_details
        return order

    def get_club_service_list(self, club_name):
        club = self._find_club_and_error(club_name)
        return club.services

    def get_club_service_by_name(self, club_name, service_name):
        club= self._find_club_and_error(club_name)
        service = Service.query.filter_by(name=service_name).first()
        return service

    def get_club_headline_service(self, club_name):
        club = self._find_club_and_error(club_name)
        return [item for item in club.services if item.slide]

    def get_club_service_paginate_date(self, club_name, start, numbers=20):
        club = self._find_club_and_error(club_name);
        total = len(club.services)
        return club.services[start : min(start+numbers, total)]

    def delete_club_service(self, club_name, service_id):
        club= self._find_club_and_error(club_name)
        Service.query.filter_by(id=service_id).delete()
        self._commit()

    def update_club_service(self, club_name, service_id, service_data):
        club= self._find_club_and_error(club_name)
        service = Service.query.filter_by(id=service_id).first()
        logger.debug("data used to update service")
        logger.debug(service_data)
        logger.debug("service before upated")
        logger.debug(service.to_dict())

        logger.debug("starting update service")
        service.from_dict(service_data)
        logger.debug("after update service ")
        logger.debug(service.to_dict())
        logger.debug("start commiting")
        self._add_commit(service)
        logger.debug("after commit update service ")
        logger.debug(service.to_dict())

    def get_club_service(self, club_name, service_id):
        club= self._find_club_and_error(club_name)
        service = Service.query.filter_by(id=service_id).first()
        return service

    def get_club_order_list(self, club_name):
        club = self._find_club_and_error(club_name)
        return club.orders

    def get_order_by_id(self, order_id):
       order = Order.query.filter_by(id=order_id).first()
       return order

    def create_new_history_activity(self, key, value):
        history_item = HistoryActivity()
        history_item.label= key
        history_item.value = value
        self._add_commit(history_item)

    def search_history_activity(self, k):
        return HistoryActivity.query.filter_by(label=k).all()

    def create_ip_activity(self, addr):
        self.create_new_history_activity("IP", addr)

    def search_ip_activity(self):
        return self.search_history_activity("IP")





def del_all_users():
    Base.metadata.create_all(bind=engine)
    m = AppModel()
    m._delete_all_club_users(CLUB_NAME)

def init_all():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    m = AppModel()
    haoduoyu = m.create_club({'name': CLUB_NAME,
                              'description':"haoduoyu club",
                              'smtp_server':'smtp-mail.outlook.com',
                              'smtp_port':'587',
                              'smtp_encryption': 'starttls',
                              'email':"haoduoyutest@hotmail.com",
                              'email_pwd':"test1232018",
                              'tel':'13379506333'
                            })
    role_user1 = m.create_club_role(haoduoyu.name,
                                    {'name':'user', 'description':"normal usr"})
    m._add(haoduoyu)
    m._commit()