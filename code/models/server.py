import sqlite3
from db import db

class ServerModel(db.Model):

    __tablename__ = 'items'
    
    id = db.Column(db.Integer, primary_key=True)
    srv_name = db.Column(db.String(80))
    srv_owner
    srv_note
    srv_reg_datetime
    
    ilo_ip = db.Column(db.String(80))
    ilo_hostname 
    ilo_macaddress
    ilo_status

    price = db.Column(db.Float(precision=2))

    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))
    store = db.relationship('StoreModel')

    def __init__(self, name, price, store_id):
        self.name = name
        self.price = price
        self.store_id = store_id

    def json(self):
        return {'name': self.name, 'price': self.price}

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()