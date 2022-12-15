from flask import render_template, Blueprint
from flask import request
from weatherapp.main import weather_queries
from flask_login import current_user


main = Blueprint('main', __name__)



@main.route('/', methods=['GET', 'POST'])
def home():
    weather = []
    if request.method == 'POST':
        if current_user.is_authenticated and request.form.get('city_name'):
            weather_queries.add_weather(request.form['city_name'], current_user)
            weather = weather_queries.get_weathers(current_user)
            return render_template('home.html', weather=weather)
        elif request.form.get('id'):
            weather_queries.delete_weather(int(request.form['id']))
            weather = weather_queries.get_weathers(current_user)
            return render_template('home.html', weather=weather)
        elif request.form.get('city_name'):    
            weather.append(weather_queries.get_weather(request.form['city_name']))
            if weather:
                return render_template('home.html', weather=weather)
            return render_template('home.html')
        else:
            return render_template('home.html')
    elif request.method == 'GET':
        if current_user.is_authenticated:
            weather = weather_queries.get_weathers(current_user)
            return render_template('home.html', weather=weather)
        else:
            return render_template('home.html')