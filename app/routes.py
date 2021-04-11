from app import app
from app.models import User, db, Restaurant
from flask_login import current_user, login_user
from flask import request, jsonify, url_for, Response
from werkzeug.http import HTTP_STATUS_CODES


@app.route('/login', methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return "welcome again"
	data = request.get_json() or {}
	print(data['email'])
	print(data['password'])
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
	response.headers['Location'] = url_for('get_user')
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
	return query

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
	response.headers['Location'] = url_for('get_user')
	return response

@app.route('/moreRestInfo/<int:id>', methods=['GET', 'POST'])
def moreRestInfo(id):
	if Restaurant.query.filter_by(id=id).first():
		return 'No such restaurant'
	rest = Restaurant()
	response = jsonify(rest.to_dict_more_data())
	return response
