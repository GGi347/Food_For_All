from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login
from sqlalchemy import desc
from flask import url_for
from collections import defaultdict

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True, nullable = False)
    email = db.Column(db.String(120), index=True, unique=True, nullable = False)
    contact_number = db.Column(db.String(15), nullable = False)
    password_hash = db.Column(db.String(128), nullable = False)
    booking = db.relationship('Booking', backref='author', lazy='dynamic')

    def from_dict(self, data, new_user=False):
        for field in ['username', 'email', 'contact_number']:
            if field in data:
                setattr(self, field, data[field])
        if new_user and 'password' in data:
            self.set_password(data['password'])

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
    id = db.Column(db.Integer, primary_key=True)
    restaurantname = db.Column(db.String(64), index=True, unique=True,nullable=False)
    email = db.Column(db.String(120), index=True, unique=True, nullable = False)
    contact_number = db.Column(db.String(15))
    password_hash = db.Column(db.String(128), nullable = False)
    points = db.Column(db.Integer, index=True)
    cuisine = db.Column(db.String(45))
    weekdays = db.Column(db.String(10))
    weekends = db.Column(db.String(10))
    about = db.Column(db.String(10))
    address_id = db.Column(db.Integer, db.ForeignKey('address.id'))
    available_seats = db.Column(db.Integer)
    menu = db.relationship('Menu', backref='rest_menu', lazy='dynamic')
    booking = db.relationship('Booking', backref='rest_booking', lazy='dynamic')
    '''def from_dict(self, data, new_user=False):
        for field in ['username', 'email', 'contact_number']:
            if field in data:
                setattr(self, field, data[field])
        if new_user and 'password' in data:
            self.set_password(data['password'])

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)'''

    '''def to_dict(query):
    	for 
        data = {
            'id': self.id,
            'username': self.username,
            
        }
        
        return data'''

    def order(self):
    	query = Restaurant.query.filter(Restaurant.points > 0).order_by(Restaurant.points.desc()).all()
    	a_list = []
    	for q in range(0,1):
    		data = {"id": query[0].id, "name": query[0].restaurantname, "cuisine": query[0].cuisine, "points": query[0].points}
    		datacopy = data.copy()
    		a_list.append(datacopy)
    	mydict = {}
    	mydict["Restaurants"] = a_list
    	return mydict

    def from_dict(self, data, new_user=False):
        for field in ['restaurantname', 'email', 'contact_number', 'weekends', 'weekdays', 'cuisine', 'points', 'about']:
            if field in data:
                setattr(self, field, data[field])
        if new_user and 'password' in data:
            self.set_password(data['password'])

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self, include_email=False):
    	data = { 'id' : self.id, 'restaurantname': self.restaurantname, 'cuisine': self.cuisine}
    	if include_email:
    		data['email'] = self.email
    	return data


    def to_dict_more_data(self, include_email=False):
        data = {
      
            'restaurantname': self.restaurantname,
            'cuisine': self.cuisine
            
        }
        if include_email:
            data['email'] = self.email
        return data


    '''def __repr__(self):
    	return '<Restaurant {}>'.format(self.restaurantname)'''
class Address(UserMixin, db.Model):
	id = db.Column(db.Integer, primary_key=True)
	address_code = db.Column(db.Integer)
	latitude = db.Column(db.String(5))
	restaurants = db.relationship('Restaurant', backref='add_rest', lazy='dynamic')
	name = db.Column(db.String(100), nullable=False)
	longitude = db.Column(db.String(5))
      

class Booking(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bookedBy = db.Column(db.Integer, db.ForeignKey('user.id'))
    bookedOn = db.Column(db.DateTime, nullable=False)
    bookingOn = db.Column(db.DateTime, nullable=False)
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
	item = db.Column(db.String(100), nullable = False)
	menu = db.relationship('Menu', backref='item_menu', lazy='dynamic')

class Menu(UserMixin, db.Model):
	id = db.Column(db.Integer, primary_key=True)
	restaurant = db.Column(db.Integer, db.ForeignKey('restaurant.id'))
	item = db.Column(db.Integer, db.ForeignKey('item.id'))
	price = db.Column(db.Integer, nullable=False)
	availablility = db.Column(db.String(11))



   