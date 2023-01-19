from flask import render_template, Blueprint
from flask import request
from weatherapp.main import weather_queries
from weatherapp.users.forms import CityForm
from flask_login import current_user
import pycountry


main = Blueprint('main', __name__)

@main.route('/', methods=['GET', 'POST'])
def home():
    weather = []
    if current_user.is_authenticated:
        country = current_user.country
        form = CityForm(country=country)
    else:
        form = CityForm(country='PL')
    if request.method == 'POST':
        if form.validate_on_submit():
            if current_user.is_authenticated and form.city.data:
                weather_queries.add_weather(form.city.data, current_user, form.country.data,)
                weather = weather_queries.get_weathers(current_user)
                return render_template('home.html', form=form, weather=weather)
            elif request.form.get('id'):
                weather_queries.delete_weather(int(request.form['id']))
                weather = weather_queries.get_weathers(current_user)
                return render_template('home.html', form=form, weather=weather)
            elif form.city.data:
                weather.append(weather_queries.get_weather(form.city.data))
                if weather:
                    return render_template('home.html', form=form, weather=weather)
    elif request.method == 'GET':
        if current_user.is_authenticated:
            weather = weather_queries.get_weathers(current_user)
            return render_template('home.html', form=form, weather=weather)
                        
    return render_template('home.html', form=form)
    """
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
            """