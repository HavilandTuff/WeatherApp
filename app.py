import json
from flask import Flask
from flask import render_template
from flask import request
import requests
import sys
import os

app = Flask(__name__)
API_KEY = os.getenv('WEATHER_API_KEY')


def get_location_cordinates(location):
    lat = None
    lon = None
    city = None
    r = requests.get(f"http://api.openweathermap.org/geo/1.0/direct?q={location},PL&appid={API_KEY}")
    location_data = json.loads(r.text)
    lon = location_data[0]['lon']
    lat = location_data[0]['lat']
    city = location_data[0]['local_names']['en']
    return (lat, lon, city)
    

def get_weather(location=None):
    weather = None
    lat, lon, name = get_location_cordinates(location)
    r = requests.get(f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric')
    weather_json = r.text
    weather_data = json.loads(weather_json)
    if weather_data['cod'] == 200:
        weather = {'name': name, 'state': weather_data['weather'][0]['description'], 'temp': weather_data['main']['temp']}
    return weather


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':        
        weather = get_weather(request.form['city_name'])
        if weather:
            return render_template('index.html', weather=weather)
        return render_template('index.html', weather='Not Found')
    elif request.method == 'GET':
        return render_template('index.html')
# don't change the following way to run flask:


if __name__ == '__main__':
    if len(sys.argv) > 1:
        arg_host, arg_port = sys.argv[1].split(':')
        app.run(host=arg_host, port=arg_port)
    else:
        app.run()
