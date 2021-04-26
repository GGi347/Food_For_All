from app import db
import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login
from sqlalchemy import desc, DateTime
from flask import url_for
from collections import defaultdict
from datetime import datetime, timezone
from sqlalchemy.sql import func

class Admin(UserMixin, db.Model):
    id = db.Column(db.Integer,  primary_key=True)
    email = db.Column(db.String(120), index=True, unique=True, nullable = False)
    password_hash = db.Column(db.String(128), nullable = False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True, nullable = False)
    email = db.Column(db.String(120), index=True, unique=True, nullable = False)
    contact_number = db.Column(db.String(15), nullable = False)
    password_hash = db.Column(db.String(128), nullable = False)
    points = db.Column(db.Integer)
    booking = db.relationship('Booking', backref='author', lazy='dynamic')
    user_order = db.relationship('UserOrder', backref='user_order', lazy='dynamic')
    user_pref = db.relationship('UserPreference', backref='user_preference', lazy='dynamic')
    user_donation = db.relationship('Donation', backref='user_donation', lazy='dynamic')

    def from_dict(self, data, new_user=False):
        for field in ['username', 'email', 'contact_number']:
            if field in data:
                setattr(self, field, data[field])
        if new_user and 'password' in data:
            self.set_password(data['password'])

    def edit_points(self, data):
        for field in ['id']:
            if field in data:
                setattr(self, field, data[field])

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self, include_email=False):
        data = {
            'id': self.id,
            'username': self.username,
            
        }
        if include_email:
            data['email'] = self.email
        return data

    def __repr__(self):
        return '<User {}>'.format(self.username)  

@login.user_loader
def load_user(id):
    return User.query.get(int(id))  

class Restaurant(UserMixin, db.Model):
    id = db.Column(db.Integer,  primary_key=True)
    restaurantname = db.Column(db.String(64), index=True, unique=True,nullable=False)
    email = db.Column(db.String(120), index=True, unique=True, nullable = False)
    contact_number = db.Column(db.String(15))
    password_hash = db.Column(db.String(128), nullable = False)
    points = db.Column(db.Integer, index=True)
    cuisine = db.Column(db.String(45))
    about = db.Column(db.String(200))
    address_id = db.Column(db.Integer, db.ForeignKey('address.id'))
    menu = db.relationship('Menu', backref='rest_menu', lazy='dynamic')
    booking = db.relationship('Booking', backref='rest_booking', lazy='dynamic')
    #rest_order = db.relationship('UserOrder', backref='rest_order', lazy='dynamic')
    rest_donation = db.relationship('Donation', backref='rest_donation', lazy='dynamic')

    def order(self):
        #query = Restaurant.query.filter(Restaurant.points >= -1).order_by(Restaurant.points.desc()).all()
        a_list = []
        query = Restaurant.query.order_by(Restaurant.points.desc()).limit(5)
        for q in query:
 
            data = {"id": q.id, "name": q.restaurantname, "cuisine": q.cuisine, "points": q.points}
            datacopy = data.copy()
            a_list.append(datacopy)
        mydict = {}
        mydict["Restaurants"] = a_list
        return a_list

    def searchOrder(self, result):
        #query = Restaurant.query.filter(Restaurant.points >= -1).order_by(Restaurant.points.desc()).all()
        a_list = []
    
        for q in result:
 
            data = {"id": q.id, "name": q.restaurantname, "cuisine": q.cuisine, "points": q.points}
            datacopy = data.copy()
            a_list.append(datacopy)
        mydict = {}
        mydict["Restaurants"] = a_list
        return a_list

    def from_dict(self, data, new_user=False):
        for field in ['restaurantname', 'email', 'contact_number', 'cuisine', 'points', 'about']:
            if field in data:
                setattr(self, field, data[field])
        if new_user and 'password' in data:
            self.set_password(data['password'])

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self, include_email=False):
        data = { 'id' : self.id, 'restaurantname': self.restaurantname, 'cuisine': self.cuisine, 'points':self.points}
        if include_email:
            data['email'] = self.email
        return data


    def to_dict_more_data(self, include_email=False):
        data = {
      
            'restaurantname': self.restaurantname,
            'cuisine': self.cuisine,
            'id': self.id
        }
        if include_email:
            data['email'] = self.email
        return data




    '''def __repr__(self):
        return '<Restaurant {}>'.format(self.restaurantname)'''
class Address(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    address_code = db.Column(db.Integer)
    locality = db.Column(db.String)
    sub_locality = db.Column(db.String)
    restaurants = db.relationship('Restaurant', backref='add_rest', lazy='dynamic')

    def from_dict(self, data):
        for field in ['address_code', 'locality', 'sub_locality']:
            if field in data:
                setattr(self, field, data[field])


    def to_dict(self):
        data = { 'id' : self.id,  'address_code': self.address_code, 'locality': self.locality, 'sub_locality': self.sub_locality}
        return data 

class Booking(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bookedBy = db.Column(db.Integer, db.ForeignKey('user.id'))
    bookedOn = db.Column(db.DateTime, nullable=False)
    bookingFor = db.Column(db.String(255))
    num_of_seats = db.Column(db.Integer, nullable = False)
    restaurant = db.Column(db.Integer, db.ForeignKey('restaurant.id'))
    

'''class MenuCategory(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    menu_category = db.Column(db.String(100),nullable=False)
    items = db.relationship('Item', backref='author', lazy='dynamic')'''

class Item(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    #menu_category = db.Column(db.Integer, db.ForeignKey('menuCategory.id'))
    menu_category = db.Column(db.String, nullable=False)
    menu_item = db.Column(db.String(100), nullable = False)
    menu = db.relationship('Menu', backref='item_menu', lazy='dynamic')

    def get_id(self, data):
        for field in ['item', 'menu_category']:
            send_data = {'id': self.id}
            return send_data

    def from_dict(self, data):
        for field in ['item', 'menu_category']:
            if field in data:
                setattr(self, field, data[field])
                

class Menu(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    restaurant = db.Column(db.Integer, db.ForeignKey('restaurant.id'))
    item = db.Column(db.Integer, db.ForeignKey('item.id'))
    price = db.Column(db.Integer, nullable=False)
    discount_in_percent = db.Column(db.Integer)

    def from_dict(self, data):
        for field in ['restaurant', 'item', 'price', 'availablility', 'discount_in_percent']:
            if field in data:
                setattr(self, field, data[field])
            

class ngo(UserMixin, db.Model):
    id = db.Column(db.Integer,  primary_key=True)
    ngoName = db.Column(db.String(64), index=True, unique=True,nullable=False)
    email = db.Column(db.String(120), index=True, unique=True, nullable = False)
    contact_number = db.Column(db.String(15))
    password_hash = db.Column(db.String(128), nullable = False)
    about = db.Column(db.String(300), nullable=False)
    message = db.relationship('Message', backref='ngo_message', lazy='dynamic')
    ngo_donation = db.relationship('Donation', backref='ngo_donation', lazy='dynamic')

    def from_dict(self, data, new_user=False):
        for field in ['ngoName', 'email', 'contact_number', 'about']:
            if field in data:
                setattr(self, field, data[field])
        if new_user and 'password' in data:
            self.set_password(data['password'])

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        data = { 'id' : self.id, 'ngoName': self.ngoName, 'email': self.email, 'about': self.about}
        return data

    def all_ngo(self):
        #query = Restaurant.query.filter(Restaurant.points >= -1).order_by(Restaurant.points.desc()).all()
        a_list = []
        query = ngo.query.all()
        for q in query:
 
            data = {"id": q.id, "ngoName": q.ngoName, "email": q.email, "about": q.about}
            datacopy = data.copy()
            a_list.append(datacopy)
        return a_list

class Message(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender = db.Column(db.Integer, db.ForeignKey('ngo.id'))
    receiver = db.Column(db.String(120), index=True, nullable=False)
    messageType = db.Column(db.String(120), nullable=False)
    message = db.Column(db.String(300), nullable=False)

    def from_dict(self, data):
        for field in ['sender', 'receiver', 'messageType', 'message']:
            if field in data:
                setattr(self, field, data[field])
        


    def to_dict(self):
        data = { 'sender': self.sender, 'messageType': self.messageType}
        return data
    
    def order(self):
        #query = Restaurant.query.filter(Restaurant.points >= -1).order_by(Restaurant.points.desc()).all()
        a_list = []
        query = Message.query.all()
        for q in query:
 
            data = {"sender": q.sender, "messageType": q.messageType, "message": q.message}
            datacopy = data.copy()
            a_list.append(datacopy)
        return a_list

class Donation(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    donatedByUser = db.Column(db.Integer, db.ForeignKey('user.id'))
    donatedByRest = db.Column(db.Integer, db.ForeignKey('restaurant.id'))
    donatedTo = db.Column(db.Integer, db.ForeignKey('ngo.id')) 
    donatedItems = db.Column(db.String(200))
    donationRestaurant = db.Column(db.Integer)
    donated = db.Column(db.Boolean, unique=False, default=True)
    donationDate = db.Column(db.DateTime, default=datetime.now())
    

    def from_dict(self, data):
        for field in ['donatedByRest', 'donatedTo', 'donatedItems', 'donationRestaurant']:
            if field in data:
                setattr(self, field, data[field])

    def from_dict_user(self, data):
        for field in ['donatedByUser', 'donatedTo', 'donatedItems', 'donationRestaurant']:
            if field in data:
                setattr(self, field, data[field])
                
        
    def verify_donation(self, data):
        #id is donation id
        #donatedTo is ngo id
        for field in ['donatedTo', 'id']:
            if field in data:
                self.donated = data['donated']
                return "Success: Verified"
            else:
                return "Error: Not Verified"


    def get_donation(self, data):
        for field in ['donatedTo']:
            if field in data:
                send_data = {'donatedBy': self.donatedBy, 'donatedItems': self.donatedItems, 'donationDate':self.donationDate, 'donationRestaurant':self.donationRestaurant}
                return send_data
            else:
                return "Error: Donation not found"

class UserPreference(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userID = db.Column(db.Integer, db.ForeignKey('user.id'))
    cuisine = db.Column(db.Integer) 

class UserOrder(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userID = db.Column(db.Integer, db.ForeignKey('user.id'))
    restID= db.Column(db.Integer, db.ForeignKey('restaurant.id'))
    item = db.Column(db.String)
    orderDate = db.Column(db.DateTime, default=datetime.now())

    def from_dict(self, data):
        for field in ['userID', 'restID', 'item']:
            if field in data:
                setattr(self, field, data[field])
                
    
