import json
import requests
from datetime import datetime
from weatherapp import API_KEY, db
from weatherapp.models import Weather

def get_location_cordinates(location, country=None):
    lat = None
    lon = None
    city = None
    if not country:
        country = 'PL'
    r = requests.get(f"http://api.openweathermap.org/geo/1.0/direct?q={location},{country}&appid={API_KEY}")
    location_data = json.loads(r.text)
    if location_data:
        lon = location_data[0]['lon']
        lat = location_data[0]['lat']
        city = location_data[0]['name']
    return (lat, lon, city)
    

def get_weather(location=None, country=None):
    weather = None
    lat, lon, name = get_location_cordinates(location, country)
    r = requests.get(f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric')
    weather_json = r.text
    weather_data = json.loads(weather_json)
    if weather_data['cod'] == 200:
        weather = {'city': name, 'weather': weather_data['weather'][0]['description'], 'temp': weather_data['main']['temp']}
    return weather


def get_weathers(user):
    weathers = None
    weathers = Weather.query.filter_by(owner_id=user.id).all()
    return weathers


def add_weather(location, user, country=None):
    weather = get_weather(location, country)
    if weather:
        weather_update = Weather.query.filter_by(city=weather['city'], owner_id=user.id).first()
        if weather_update:
            weather_update.temp = weather['temp']
            weather_update.weather = weather['weather']
            weather_update.last_update = datetime.utcnow()
            db.session.commit()
        else:
            new_weather = Weather(city=weather['city'], 
                                weather=weather['weather'], 
                                temp=weather['temp'], 
                                owner_id=user.id, 
                                country=country)
            db.session.add(new_weather)
            db.session.commit()

def delete_weather(weather_id):
    del_weath = Weather.query.filter_by(id=weather_id).first()
    db.session.delete(del_weath)
    db.session.commit()
    
            


