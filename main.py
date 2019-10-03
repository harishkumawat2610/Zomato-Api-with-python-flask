from flask import Flask, render_template, request, session, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json
import requests
import os

with open('config.json', 'r') as c:
    params = json.load(c)['params']

application = Flask(__name__)
application.config['UPLOAD_FOLDER'] = params['upload_location']
application.secret_key = os.urandom(24)
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
application.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/python_task'
img_dir = "//home//kuma//Music//bootstrap//static//img"
vid_dir = "//home//kuma//Music//bootstrap//static//up_image"

db = SQLAlchemy(application)

class User(db.Model):
    s_no = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(180), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

@application.route("/register", methods=['POST', 'GET'])
def register():
    sign_error = None;
    cate = None;
    if request.method == 'POST':
        """Add entry"""
        user = request.form.get("register_name")
        email = request.form.get("register_email")
        password = request.form.get("register_password")
        test_name = User.query.filter_by(email=email).first()
        if test_name is None:
            entry = User(name=user, email=email, password=password)
            db.session.add(entry)
            db.session.commit()
            flash("Account Successfully Created", "alert-success")
            return render_template('index.html')
        elif test_name.email == email:
            flash("Email is Aready Exits", "alert-danger")
            return render_template('index.html')
    return render_template('/index.html')


@application.route("/", methods=['POST', 'GET'])
@application.route("/home", methods=['POST', 'GET'])
def login():
    if 'user' in session and session['user'] == "xxxccc":
        return redirect(url_for('city'))

    error = None
    if request.method == 'POST':
        uname = request.form.get('login_email')
        upass = request.form.get('login_pass')
        test_name = User.query.filter_by(email=uname).first()
        print(test_name)
        if test_name is None:
            error = "Invalid password and email"
            return render_template('index.html', error=error)
        elif test_name.email == uname and test_name.password == upass:
            session['user'] = "xxxccc"
            return redirect(url_for('city'))
        else:
            error = "Invalid password and email"
            return render_template('index.html', error=error)

    return render_template('index.html', error=error)

@application.route('/city')
def city():
    return render_template('city.html')

@application.route('/cityname/<string:name>')
def city_name(name):
    zomato_api = 'e65691ccb8423e9e8fc81b784b4135ac'

    def get_location_details(query):
        headers = {
            'Accept': 'application/json',
            'user-key': zomato_api,
        }
        params = (
            ('query', query),
        )

        response = requests.get('https://developers.zomato.com/api/v2.1/locations', headers=headers, params=params)
        data = response.json()

        for loc in data['location_suggestions']:
            loc_id = loc['entity_id']
            loc_type = loc['entity_type']

        return loc_id, loc_type

    def get_restaurants(ent_id, ent_type):
        headers = {
            'Accept': 'application/json',
            'user-key': zomato_api,
        }

        params = (
            ('entity_id', ent_id),
            ('entity_type', ent_type),
        )

        response = requests.get('https://developers.zomato.com/api/v2.1/search', headers=headers, params=params)
        # print (help(response))

        return response.json()
    if name == 'ajmer':
        q = 'ajmer'
    if name == 'bangalore':
        q = 'bangalore'
    if name == 'bikaner':
        q = 'bikaner'
    if name == 'jaipur':
        q = 'jaipur'
    if name == 'jodhpur':
        q = 'jodhpur'
    entity_id, entity_type = get_location_details(q)
    data = get_restaurants(entity_id, entity_type)

    return render_template('rest.html',data=data,q=q)



application.run(debug=True)
