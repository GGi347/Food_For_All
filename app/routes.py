from app import app
from app.models import User, db, Restaurant, ngo, Message, Donation, Item, Menu, UserOrder
from app.forms import LoginForm
from flask_login import current_user, login_user
from flask import request, jsonify, url_for, Response, send_file
from werkzeug.http import HTTP_STATUS_CODES
import json
from flask import render_template, flash, redirect

@app.route('/loginadmin', methods=['GET', 'POST'])
def loginadmin():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('customer'))
    return render_template('login.html', title='Sign In', form=form)

@app.route('/editCustomer', methods=['GET', 'POST'])
def editCustomer():
    user = User.query.all()
    posts = [ 

        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    return render_template('customer.html', user=user, posts=posts)

@app.route('/editRestaurant', methods=['GET', 'POST'])
def editRestaurant():
    user = Restaurant.query.all()
    posts = [ 

        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    return render_template('restaurant.html', user=user, posts=posts)

@app.route('/editNgo', methods=['GET', 'POST'])
def editNgo():
    user = ngo.query.all()
    posts = [ 

        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    return render_template('ngo.html', user=user, posts=posts)

@app.route('/logoutadmin', methods=['GET', 'POST'])
def logoutadmin():
    return redirect('/loginadmin')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return jsonify({"Welcome again"})
    data = request.get_json() or {}
    
    if 'email' not in data or 'password' not in data:
        return jsonify({'error': "Must include all credentials"})
    user = User.query.filter_by(email=data['email']).first()
    if user is None or not user.check_password(data['password']):       
        return jsonify({'error': "User not found"})
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
        return jsonify({'error': "Must include all credentials"})
    user = Restaurant.query.filter_by(email=data['email']).first()
    if user is None or not user.check_password(data['password']):       
        return jsonify({'error': "User not found"})
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
    
@app.route('/sendPhoto', methods=['GET', 'POST'])
def sendPhoto():
    data = request.get_json() or {}
    strid = str(data['id'])
    return send_file('static/rest_logo/restaurant'+strid+'.jpg', as_attachment=True)

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
        return jsonify({"Welcome again"})
    data = request.get_json() or {}
    if 'email' not in data or 'password' not in data:
        mydict = {}
        mydict["r"] = ngo.query.all()
        return mydict
    user = ngo.query.filter_by(email=data['email']).first()
    if user is None or not user.check_password(data['password']):
        return jsonify({'error': "NGO not found"})
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
    if 'item' not in data or 'menu_category' not in data:
        return "Fill all the fields"
    item_name =  item.query.filter_by(item=data['item']).first()
    if item_name is not None:
        send_data = {'id': item_name.id}
        return jsonify(send_data)
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

@app.route('/getMenu', methods = ['GET', 'POST'])
def getMenu():
    data = request.get_json() or {}
    menu = Menu()
    query = []
    rest_names =  menu.query.filter_by(restaurant=data['restaurant']).all()
    if rest_names is not None:
        for rest_name in rest_names:
            send_data = {'id': rest_name.item, 'price': rest_name.price, 'discount_in_percent': rest_name.discount_in_percent }
            query.append(send_data)
        return getItem(query)
    else:
        return jsonify({'error': "Menu Not Found"})

def getItem(query):
    item = Item()
    items = []
    for data in query:
        if item.query.filter_by(id=data['id']).all() is not None:
            send_data = {'menu_category': item.menu_category, 'price': data['price']}
            items.append(send_data)
        return Response(json.dumps(items), mimetype="application/json")
    else:
        return jsonify({'error': "Item not found"})

@app.route('/getMessage', methods=['GET', 'POST'])
def getMessage():
    data = request.get_json() or {}
    message = Message()
    #query = user.()
    #return Response(json.dumps(query), mimetype="application/json")

@app.route('/getSearchResult', methods=['GET', 'POST'])
def getSearchResult():
    data = request.get_json() or {}
    restaurant = Restaurant()
    resultone = restaurant.query.filter_by(cuisine=data['searchTxt']).all()
    if resultone is None:
        resulttwo = restaurant.query.filter_by(restaurantname=data['searchTxt']).all()
        if resulttwo is None:
            return jsonify({'error': "NGO not found"})
        else:
            query = restaurant.searchOrder(resulttwo)
            return Response(json.dumps(query), mimetype="application/json")
    else:
        query = restaurant.searchOrder(resultone)
        return Response(json.dumps(query), mimetype="application/json")
    
@app.route('/addOrder', methods=['GET', 'POST'])
def addOrder():
    data = request.get_json() or {}
    order = UserOrder()
    order.from_dict(data)
    db.session.add(order)
    db.session.commit()
    return "Order added"


