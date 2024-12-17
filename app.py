from flask import Flask, render_template, request
import os
from dotenv import load_dotenv
from weather import main as get_weather

load_dotenv()
API_key = os.getenv('API_KEY')

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():

    weather_data = None
    city = None
    icon_url = None

    if request.method == 'POST':
        city = request.form.get('city_name')
        if city:
            weather_data = get_weather(city)
            icon_url = f"https://openweathermap.org/img/wn/{weather_data.icon}.png"

    return render_template('index.html', weather_data=weather_data, city=city, icon=icon_url)



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)