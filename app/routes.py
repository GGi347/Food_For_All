from app import app
from app.models import User, db, Restaurant, ngo, Message, Donation, Item, Menu
from flask_login import current_user, login_user
from flask import request, jsonify, url_for, Response, send_file
from werkzeug.http import HTTP_STATUS_CODES
import json

@app.route('/login', methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return "welcome again"
	data = request.get_json() or {}
	
	if 'email' not in data or 'password' not in data:
		return 'error: must include all credentials'
	user = User.query.filter_by(email=data['email']).first()
	if user is None or not user.check_password(data['password']):		
		return "error: user not present"
	else:
		login_user(user)
		response = jsonify(user.to_dict())
		response.status_code = 201
		return response

@app.route('/logout')
def logout():
	logout_user()

@app.route('/')
def home():
	return 'connected'

@app.route('/users', methods=['GET'])
def get_users():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = User.to_collection_dict(User.query, page, per_page, 'api.get_users')
    return jsonify(data)

@app.route('/register', methods=['GET', 'POST'])
def register():
	data = request.get_json() or {}
	if 'username' not in data or 'email' not in data or 'password' not in data or 'contact_number' not in data:
		return 'Please fill all the fields correctly'
	if User.query.filter_by(username=data['username']).first():
		return 'please use a different username'
	if User.query.filter_by(email=data['email']).first():
		return 'please use a different email'
	user = User()
	user.from_dict(data, new_user=True)
	db.session.add(user)
	db.session.commit()
	response = jsonify(user.to_dict())
	response.status_code = 201
	#response.headers['Location'] = url_for('get_user')
	return response

'''@app.route('/topRestaurants', methods=['GET'])
def topRestaurants():
	user = User()
	response = jsonify(user.to_dict_top_rest())
	response.status_code = 201
	return response'''
	
@app.route('/test', methods=['GET'])   
def test():
	restaurant = Restaurant()
	query = restaurant.order()
	return Response(json.dumps(query), mimetype="application/json")

@app.route('/registerRest', methods=['GET', 'POST'])
def registerRest():
	data = request.get_json() or {}
	if 'restaurantname' not in data or 'email' not in data or 'password' not in data or 'contact_number' not in data:
		return 'Please fill all the fields correctly'
	if Restaurant.query.filter_by(restaurantname=data['restaurantname']).first():
		return 'Restaurant name is already registered'
	if Restaurant.query.filter_by(email=data['email']).first():
		return 'Please use a different email'
	if Restaurant.query.filter_by(contact_number=data['contact_number']).first():
		return 'Please use a different contact number'
	restaurant = Restaurant()
	restaurant.from_dict(data, new_user=True)
	db.session.add(restaurant)
	db.session.commit()
	response = jsonify(restaurant.to_dict())
	response.status_code = 201
	#response.headers['Location'] = url_for('get_user')
	return response

@app.route('/loginRestaurant', methods=['GET', 'POST'])
def loginRestaurant():
	if current_user.is_authenticated:
		return "welcome again"
	data = request.get_json() or {}
	
	if 'email' not in data or 'password' not in data:
		return 'error: must include all credentials'
	user = Restaurant.query.filter_by(email=data['email']).first()
	if user is None or not user.check_password(data['password']):		
		return "error: user not present"
	else:
		login_user(user)
		response = jsonify(user.to_dict())
		response.status_code = 201
		return response

@app.route('/moreRestInfo/<int:id>', methods=['GET', 'POST'])
def moreRestInfo(id):
	if Restaurant.query.filter_by(id=id).first():
		return 'No such restaurant'
	rest = Restaurant()
	response = jsonify(rest.to_dict_more_data())
	return response
	
@app.route('/sendPhoto<int:id>', methods=['GET', 'POST'])
def sendPhoto(id):
    return send_file('static/rest_logo/restaurant'+id+'.jpg', as_attachment=True)

@app.route('/registerngo', methods=['GET', 'POST'])
def registerNgo():
	data = request.get_json() or {}
	if 'ngoName' not in data or 'email' not in data or 'password' not in data or 'contact_number' not in data:
		return 'Please fill all the fields correctly'
	if ngo.query.filter_by(ngoName=data['ngoName']).first():
		return 'ngo name is already registered'
	if ngo.query.filter_by(email=data['email']).first():
		return 'Please use a different email'
	if ngo.query.filter_by(contact_number=data['contact_number']).first():
		return 'Please use a different contact number'
	user = ngo()
	user.from_dict(data, new_user=True)
	db.session.add(user)
	db.session.commit()
	response = jsonify(user.to_dict())
	response.status_code = 201
	#response.headers['Location'] = url_for('get_user')
	return response
@app.route('/loginNgo', methods=['GET', 'POST'])
def loginNgo():
	if current_user.is_authenticated:
		return "welcome again"
	data = request.get_json() or {}
	if 'email' not in data or 'password' not in data:
		mydict = {}
		mydict["r"] = ngo.query.all()
		return mydict
	user = ngo.query.filter_by(email=data['email']).first()
	if user is None or not user.check_password(data['password']):
		return "error: user not present"
	else:
		login_user(user)
		response = jsonify(user.to_dict())
		response.status_code = 201
		return response
#get a list of ngos for donars to choose from
@app.route('/getNgo', methods=['GET', 'POST'])
def getNgo():
	user = ngo()
	query = user.all_ngo()
	return Response(json.dumps(query), mimetype="application/json")

@app.route('/sendMessage', methods=['GET', 'POST'])
def sendMessage():
	data = request.get_json() or {}
	if 'sender' not in data or 'messageType' not in data or 'message' not in data or 'receiver' not in data:
		message = Message()
		response = jsonify(message.to_dict())
		return response
	else:
		message = Message()
		message.from_dict(data)
		db.session.add(message)
		db.session.commit()
		response = jsonify(message.to_dict())
		response.status_code = 201 
		return response

@app.route('/addDonation', methods=['GET', 'POST'])
def addDonation():
	data = request.get_json() or {}
	if 'donatedBy' not in data or 'donatedTo' not in data or 'donatedItems' not in data or 'donationRestaurant' not in data:
		return "Please Fill out all the fields"
	else:
		donation = Donation()
		donation.from_dict(data)
		db.session.add(donation)
		db.session.commit()
		response = "Donation has been added" 
		return response

@app.route('/getDonation', methods = ['GET', 'POST'])
def getDonation():
	data = request.get_json() or {}
	donation = Donation()
	response = jsonify(donation.get_donation(data))
	response.status_code = 201
	return response

@app.route('/verifyDonation', methods = ['GET', 'POST'])
def verifyDonation():
	data = request.get_json() or {}
	donation = Donation()
	response = donation.verify_donation(data)
	return response

@app.route('/addToItem', methods = ['GET', 'POST'])
def addToItem():
	data = request.get_json() or {}
	item = Item()
	
	if item.query.filter_by(item=data['item']).first():
		return jsonify(item.get_id(data))
	else:
		item.from_dict(data)
		db.session.add(item)
		db.session.commit()
		return jsonify(item.get_id(data))
	
@app.route('/addToMenu', methods = ['GET', 'POST'])
def addToMenu():
	data = request.get_json() or {}
	menu = Menu()
	if 'restaurant' not in data or 'item' not in data or 'availability' not in data or 'price' not in data:
		return "Fill all the fields"
	
	if menu.query.filter_by(item=data['item']).all():
		if menu.query.filter_by(restaurant=data['restaurant']).all():
			return "Item already present in the menu"
	else:
		menu.from_dict(data)
		db.session.add(menu)
		db.session.commit()
		return "Item Added To Menu"


