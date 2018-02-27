
#!/usr/bin/python
import os
import datetime
from sqlalchemy import UniqueConstraint, ForeignKey, create_engine, Column, Integer, String, Table, DateTime, Boolean
from sqlalchemy.orm import relationship, scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flask_babel import lazy_gettext as _
from utils import *
import coloredlogs, logging



logger = logging.getLogger(__name__)
coloredlogs.install(level='DEBUG', logger=logger)

FILE_STORE = os.path.join(os.path.dirname(__file__), 'filestore')
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

class User(Base, BaseMixin, UserMixin):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=False)
    tel = Column(String, unique=False)
    password_hash = Column(String, nullable=False)
    club_id = Column(Integer, ForeignKey('club.id', ondelete='CASCADE'), nullable=False)
    __table_args__ = (UniqueConstraint('email', 'club_id'),)
    roles = relationship("Role", 
                         secondary=association_user_role,
                         back_populates="users")


class Club(Base, BaseMixin):
    __tablename__ = 'club'
    id = Column(Integer, primary_key=True) 
    name = Column(String, unique=True)
    description= Column(String)
    # relationship
    users = relationship("User", backref="club")
    roles = relationship("Role", backref="club")
    services = relationship("Service", backref="club", order_by="desc(Service.last_update_time)")

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
    pic_and_text = Column(String)# a list of text and image files
    last_update_time = Column(DateTime, default=datetime.datetime.utcnow)
    major_pic = Column(String) # major picture of this service
    sub_services = Column(String) # a list of sub services
    active = Column(Boolean, default=True) #onine or offline
    slide = Column(Boolean, default=False)  # show on slding headline

    # link to club
    club_id = Column(Integer, ForeignKey("club.id", ondelete='CASCADE'), nullable=False)
    __table_args__ = (UniqueConstraint('name', 'club_id'),)


class ShoppingCart(Base, BaseMixin):
    __tablename__ = 'shoppingcart'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id', ondelete='CASCADE'))
    service_id = Column(Integer, ForeignKey('service.id', ondelete='CASCADE' ))

class Order(Base, BaseMixin):
    __tablename__ = 'order'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    club_name = Column(String)
    user_email = Column(String, unique=False)
    user_tel = Column(String, unique=False)
    total_price = Column(Integer)
    paid = Column(Integer)
    time = Column(DateTime)
    details = relationship("OrderDetail",cascade="all, delete",backref="order")

class OrderDetail(Base, BaseMixin):
    __tablename__ = 'orderdetail'
    id = Column(Integer, primary_key=True)
    service_id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    discount = Column(Integer, nullable=False, default=20)
    last_update_time = Column(DateTime)
    major_pic = Column(String) # major picture of this service
    description = Column(String) # msxing picture path and text descriptions 

    # relation to the order
    order_id = Column(Integer, ForeignKey('order.id'), nullable=False)

class AppModel(object):
    def __init__(self, db_session=db_session):
        self.db_session = db_session 
        self.file_store = FILE_STORE 
        if not os.path.exists(self.file_store):
            os.makedirs(self.file_store)

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

    def get_club_user_by_email(self, club_name, email):
        club = self._find_club_and_error(club_name)
        user = User.query.filter_by(email=email, club_id=club.id).first()
        return user

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
        #check password
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

    # file related 
    def get_filestore_dir(self):
        return self.file_store

    def get_filestore_service(self, club_name, id):
        service_path = self.file_store + "/{}/service/{}".format(club_name, id)
        if not os.path.exists(service_path):
            os.makedirs(service_path)
        return service_path

    # service related functions
    def create_club_service(self, club_name, service_data):
        club = self._find_club_and_error(club_name)
        new_service = Service(**service_data)
        new_service.club_id = club.id 
        self._add_commit(new_service)

    def get_club_service_list(self, club_name):
        club = self._find_club_and_error(club_name)
        return club.services

    def get_club_headline_service(self, club_name):
        club = self._find_club_and_error(club_name)
        return [item for item in club.services if item.slide]

    def get_club_service_paginate_date(self, club_name, start, numbers=20):
        club = self._find_club_and_error(club_name)
        total = len(club.services)
        return club.services[start : min(start+numbers, total)]

def init_all():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine) 
    m = AppModel()
    haoduoyu = m.create_club({'name': 'haoduoyu', 'description':"haoduoyu club"})
    haoduomao = m.create_club({'name': 'haoduomao', 'description':"haoduomao club"})
    role_user1 = m.create_club_role(haoduoyu.name, {'name':'user', 'description':"normal usr"})
    role_user2 = m.create_club_role(haoduomao.name, {'name':'user', 'description':"normal usr"})
    user1 = User()
    user1.club_id = haoduoyu.id
    user1.email = "abc@abc.com"
    user1.tel = '13311111'
    user1.password_hash = "abc"
    user1.roles.append(role_user1) 

    user2 = User()
    user2.club_id = haoduomao.id
    user2.email = "123@abc.com"
    user2.tel = '13311111'
    user2.password_hash = "123"
    user2.roles = [role_user2]
    user2.roles.append(role_user2)
    m._add(haoduoyu)
    m._add(haoduomao)
    m._add(role_user1)
    m._add(role_user2)
    m._add(user1)
    m._add(user2)
    m._commit()