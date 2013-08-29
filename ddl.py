from flask import Flask
from sqlalchemy import Column, Integer, Numeric, Unicode, UnicodeText, DateTime, Binary
from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.ext.declarative import declared_attr
import flask.ext.sqlalchemy
from application import app


# Create base class with default table name and id
class Base(object):
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()
    id = Column(Integer, primary_key=True)


# Overwrite default model
flask.ext.sqlalchemy.Model = Base
from flask.ext.sqlalchemy import SQLAlchemy
db = SQLAlchemy(app)

class MetadataMixin(object):
    @declared_attr
    def events(cls):
        joinstr = '{0}.id == foreign(Event.table_id) and Event.type == "{1}"'.format(cls.__name__, cls.__tablename__)
        return db.relationship('Event', primaryjoin=joinstr, backref=cls.__name__.lower())

    @declared_attr
    def notes(cls):
        joinstr = '{0}.id == foreign(Note.table_id) and Note.type == "{1}"'.format(cls.__name__, cls.__tablename__)
        return relationship('Note', primaryjoin=joinstr, backref=cls.__name__.lower())

    @declared_attr
    def attachments(cls):
        joinstr = '{0}.id == foreign(Attachment.table_id) and Attachment.type == "{1}"'.format(cls.__name__, cls.__tablename__)
        return db.relationship('Attachment', primaryjoin=joinstr, backref=cls.__name__.lower())

user_permission = db.Table('user_permission', db.metadata,
     Column('user_id', Integer, ForeignKey('user.id')),
     Column('permission_id', Integer, ForeignKey('permission.id'))
     )

class Event(Base):

    type = Column(Unicode(50), nullable=False, index=True)
    table_id = Column(Integer, nullable=False, index=True)

    user_id = Column(Integer, ForeignKey('user.id'), nullable=False, index=True)
    user = db.relationship('User', backref=db.backref('events', order_by='Event.date'))

    date = Column(DateTime, nullable=False, index=True)
    attr = Column(Unicode(50), nullable=False)
    old = Column(Unicode(50), nullable=False)
    new = Column(Unicode(50), nullable=False)

    def __repr__(self):
        return '<Event({0},{1})>'.format(self.user,self.date)

class Note(Base):

    type = Column(Unicode(50), nullable=False, index=True)
    table_id = Column(Integer, nullable=False, index=True)

    user_id = Column(Integer, ForeignKey('user.id'), nullable=False, index=True)
    user = db.relationship('User', backref=db.backref('notes', order_by='Note.date'))

    date = Column(DateTime, nullable=False, index=True)
    text = Column(UnicodeText, nullable=False)

    def __repr__(self):
        return '<Note({0},{1})>'.format(self.user,self.date)

class Attachment(Base):

    type = Column(Unicode(50), nullable=False, index=True)
    table_id = Column(Integer, nullable=False, index=True)

    user_id = Column(Integer, ForeignKey('user.id'), nullable=False, index=True)
    user = db.relationship('User', backref=db.backref('attachments', order_by='Attachment.id'))

    name = Column(Unicode(50), nullable=False)
    sha256hash = Column(Binary, nullable=False)

    def __repr__(self):
        return '<Attachment({0})>'.format(self.name)

class Permission(Base):

    codename = Column(Unicode(50), nullable=False, index=True)
    longname = Column(Unicode(50), nullable=False)

    def __repr__(self):
        return '<Permission({0})>'.format(self.username)

class User(Base):

    username = Column(Unicode(50), nullable=False, unique=True, index=True)
    name = Column(Unicode(50), nullable=False, index=True)

    permissions = db.relationship('Permission', secondary=user_permission, backref='users')

    def __repr__(self):
        return '<User({0})>'.format(self.username)

class Device_Type(Base):

    manufacturer = Column(Unicode(50), nullable=False)
    model = Column(Unicode(50), nullable=False)

    __table_args__ = (UniqueConstraint('manufacturer','model'),)

    def __repr__(self):
        return '<Device_Type({0},{1})>'.format(self.manufacturer,self.model)

class Device(MetadataMixin, Base):

    inventory_number = Column(Unicode(50), unique=True, nullable=False, index=True)
    serial_number = Column(Unicode(50), index=True)
    bag_tag = Column(Unicode(50), index=True)

    user_id = Column(Integer, ForeignKey('user.id'), nullable=False, index=True)
    user = db.relationship('User', backref=db.backref('devices', order_by='Device.id'))

    device_type_id = Column(Integer, ForeignKey('device_type.id'), nullable=False, index=True)
    device_type = db.relationship('Device_Type', backref=db.backref('devices', order_by='Device.id'))

    def __repr__(self):
        return '<Device({0})>'.format(self.inventory_number)

class Charge(MetadataMixin, Base):

    user_id = Column(Integer, ForeignKey('user.id'), nullable=False, index=True)
    user = db.relationship('User', backref=db.backref('charges', order_by='Charge.id'))

    device_id = Column(Integer, ForeignKey('device.id'), nullable=False, index=True)
    device = db.relationship('Device', backref=db.backref('charges', order_by='Charge.id'))

    reason = Column(UnicodeText, nullable=False)
    amount = Column(Numeric(19,4), nullable=False)

    def __repr__(self):
        return '<Charge({0})>'.format(self.inventory_number)

class Payment(MetadataMixin, Base):

    charge_id = Column(Integer, ForeignKey('charge.id'), nullable=False, index=True)
    charge = db.relationship('Charge', backref=db.backref('payments', order_by='Payment.id'))

    amount = Column(Numeric(19,4), nullable=False)

    @property
    def user(self):
        return self.charge.user

    @property
    def device(self):
        return self.charge.device

    def __repr__(self):
        return '<Payment({0})>'.format(self.inventory_number)

