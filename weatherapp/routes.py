from flask import render_template
from flask import request
from weatherapp import app, api_queries

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':        
        weather = api_queries.get_weather(request.form['city_name'])
        if weather:
            return render_template('home.html', weather=weather)
        return render_template('home.html', weather='Not Found')
    elif request.method == 'GET':
        return render_template('home.html')