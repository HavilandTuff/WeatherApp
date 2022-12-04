from flask import render_template
from flask import request
from weatherapp import app, api_queries
from weatherapp.forms import RegistrationForm, LoginForm

@app.route('/login')
def login():
    form = LoginForm()
    return render_template('login.html', form=form)


@app.route('/register')
def register():
    form = RegistrationForm()
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