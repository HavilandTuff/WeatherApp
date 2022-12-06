from flask import render_template, flash, redirect, url_for
from flask import request
from weatherapp import app, api_queries, bcrypt, db
from weatherapp.forms import RegistrationForm, LoginForm
from weatherapp.models import User, Weather
from flask_login import login_user  


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('home'))
        else:
            flash('Login unsuccessful!', 'danger')
    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        password_hash = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=password_hash)
        db.session.add(user)
        db.session.commit()
        flash(f'Your account has been created!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':        
        weather = api_queries.get_weather(request.form['city_name'])
        if weather:
            return render_template('home.html', weather=weather)
        return render_template('home.html', weather='Not Found')
    elif request.method == 'GET':
        return render_template('home.html')